# 🎓 University Admission Chatbot
## Lab Assignment — QnA Bot using MiniLM + FAISS + Flask

---

## Project Structure

```
uni_admission_chatbot/
├── app.py                    # Flask backend (Task 2)
├── admission_qna.csv         # 25 Q&A pairs dataset
├── UniAdmissionChatbot.ipynb # Full notebook (Task 1 + Task 2)
├── templates/
│   └── index.html            # Chat UI
└── README.md
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install flask sentence-transformers faiss-cpu pandas numpy
```

### 2. Run the chatbot
```bash
cd uni_admission_chatbot
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## Pipeline (Same as HadithBot)

| Step | HadithBot (Task 1) | Admission Bot (Task 2) |
|------|-------------------|----------------------|
| **Data** | LK Hadith Corpus CSV | 25 custom Q&A pairs |
| **Preprocess** | Lowercase, remove punctuation | Same clean_text() function |
| **Embed** | MiniLM-L6-v2 on hadith text | MiniLM-L6-v2 on questions |
| **Store** | FAISS IndexFlatL2 | FAISS IndexFlatL2 |
| **Search** | L2 distance similarity | L2 distance similarity |
| **UI** | Console output | Flask + HTML chat UI |

---

## Sample Questions to Ask
- What are the admission requirements?
- How do I apply for hostel?
- What scholarships are available?
- What is the fee for Computer Science?
- Can I transfer from another university?
- What is the last date to apply?
