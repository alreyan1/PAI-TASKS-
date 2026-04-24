from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def main() -> None:
    texts = [
        "Win a FREE iPhone now",
        "Claim your prize, click the link",
        "Limited-time offer! Buy 1 get 1 free",
        "Congratulations, you have been selected",
        "URGENT: update your account to avoid suspension",
        "Hey, are we still meeting at 6?",
        "Can you send me the homework notes?",
        "Lunch tomorrow sounds good",
        "Please review the report before Friday",
        "Happy birthday! Hope you have a great day",
        "Let’s reschedule the call to next week",
        "Your package has been delivered",
    ]

    labels = [
        "spam",
        "spam",
        "spam",
        "spam",
        "spam",
        "ham",
        "ham",
        "ham",
        "ham",
        "ham",
        "ham",
        "ham",
    ]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    new_texts = [
        "Free prize waiting for you, claim now",
        "Are you coming to class today?",
        "Buy now and get 50% off",
    ]

    X_new = vectorizer.transform(new_texts)
    predictions = model.predict(X_new)

    print("Predictions for new texts:")
    for text, pred in zip(new_texts, predictions):
        print(f"- {text!r} -> {pred}")


if __name__ == "__main__":
    main()
