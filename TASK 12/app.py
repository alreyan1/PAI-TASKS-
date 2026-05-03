import re
import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, render_template

DATA_PATH  = "admission_qna.csv"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "admission_faiss.index"
DF_PATH    = "admission_df.pkl"

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def build_index():
    """Load CSV → clean → embed → FAISS index → save"""
    print("[1/4] Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    df['cleaned_question'] = df['question'].apply(clean_text)

    print("[2/4] Loading MiniLM model...")
    model = SentenceTransformer(MODEL_NAME)

    print("[3/4] Encoding questions...")
    embeddings = np.array(model.encode(df['cleaned_question'].values,
                                        show_progress_bar=True))
    np.save("admission_embeddings.npy", embeddings)

    print("[4/4] Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    df.to_pickle(DF_PATH)
    print(f"Done! {len(df)} Q&A pairs indexed.")
    return model, index, df

def load_index():
    """Load saved index + model"""
    model = SentenceTransformer(MODEL_NAME)
    index = faiss.read_index(INDEX_PATH)
    df    = pd.read_pickle(DF_PATH)
    return model, index, df

def search(query: str, model, index, df, top_k=3):
    """Embed query → FAISS search → return top answers"""
    q_emb = model.encode([clean_text(query)])
    distances, indices = index.search(np.array(q_emb), top_k)
    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        results.append({
            "rank"    : rank + 1,
            "question": df['question'].iloc[idx],
            "answer"  : df['answer'].iloc[idx],
            "score"   : round(float(dist), 4),
        })
    return results

app = Flask(__name__)

import os
if os.path.exists(INDEX_PATH):
    print("Loading existing index...")
    model, faiss_index, qa_df = load_index()
else:
    print("Building index from scratch...")
    model, faiss_index, qa_df = build_index()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data  = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Empty query'}), 400
    results = search(query, model, faiss_index, qa_df, top_k=3)
    return jsonify({'results': results})

if __name__ == '__main__':
    print("Starting University Admission Chatbot on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
