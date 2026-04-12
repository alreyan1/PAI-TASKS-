import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print("=== Dataset Info ===")
print(train.shape)
print(train.head())
print("\nMissing Values:")
print(train.isnull().sum())

train.drop(columns=["PassengerId", "Name", "Cabin"], inplace=True)
test_ids = test["PassengerId"]
test.drop(columns=["PassengerId", "Name", "Cabin"], inplace=True)

num_cols = ["Age", "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
for col in num_cols:
    train[col].fillna(train[col].mean(), inplace=True)
    test[col].fillna(test[col].mean(), inplace=True)

cat_cols = ["HomePlanet", "CryoSleep", "Destination", "VIP"]
le = LabelEncoder()
for col in cat_cols:
    train[col].fillna("Unknown", inplace=True)
    test[col].fillna("Unknown", inplace=True)
    combined = list(train[col]) + list(test[col])
    le.fit(combined)
    train[col] = le.transform(train[col])
    test[col] = le.transform(test[col])

train["Transported"] = train["Transported"].astype(int)

X = train.drop(columns=["Transported"])
y = train["Transported"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n=== Naive Bayes ===")
nb = GaussianNB()
nb.fit(X_train, y_train)
nb_preds = nb.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, nb_preds) * 100, 2), "%")

print("\n=== Decision Tree ===")
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
dt_preds = dt.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, dt_preds) * 100, 2), "%")

if accuracy_score(y_test, nb_preds) >= accuracy_score(y_test, dt_preds):
    best_model = nb
    print("\nBest Model: Naive Bayes")
else:
    best_model = dt
    print("\nBest Model: Decision Tree")

final_preds = best_model.predict(test)
final_preds_bool = ["True" if p == 1 else "False" for p in final_preds]

submission = pd.DataFrame({
    "PassengerId": test_ids,
    "Transported": final_preds_bool
})
submission.to_csv("submission.csv", index=False)
print("\nsubmission.csv saved!")
print(submission.head())
