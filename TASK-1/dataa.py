import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print("=== Dataset Info ===")
print("Shape:", train.shape)
print(train.head())
print("\nMissing Values:")
print(train.isnull().sum()[train.isnull().sum() > 0])

test_ids = test["Id"]
train.drop(columns=["Id"], inplace=True)
test.drop(columns=["Id"], inplace=True)

y = train["SalePrice"]
train.drop(columns=["SalePrice"], inplace=True)

cat_cols = [col for col in train.columns if train[col].dtype == "object"]
num_cols = [col for col in train.columns if train[col].dtype != "object"]

for col in num_cols:
    train[col].fillna(train[col].mean(), inplace=True)
    test[col].fillna(test[col].mean(), inplace=True)

le = LabelEncoder()
for col in cat_cols:
    train[col].fillna("Unknown", inplace=True)
    test[col].fillna("Unknown", inplace=True)
    combined = list(train[col]) + list(test[col])
    le.fit(combined)
    train[col] = le.transform(train[col])
    test[col] = le.transform(test[col])

X_train, X_test, y_train, y_test = train_test_split(train, y, test_size=0.2, random_state=42)

print("\n=== Decision Tree Regressor ===")
dt = DecisionTreeRegressor(random_state=42)
dt.fit(X_train, y_train)
dt_preds = dt.predict(X_test)
dt_mae = mean_absolute_error(y_test, dt_preds)
print("Mean Absolute Error:", round(dt_mae, 2))

print("\n=== Decision Tree (max_depth=5) ===")
dt2 = DecisionTreeRegressor(max_depth=5, random_state=42)
dt2.fit(X_train, y_train)
dt2_preds = dt2.predict(X_test)
dt2_mae = mean_absolute_error(y_test, dt2_preds)
print("Mean Absolute Error:", round(dt2_mae, 2))

if dt_mae <= dt2_mae:
    best_model = dt
    print("\nBest Model: Decision Tree (full)")
else:
    best_model = dt2
    print("\nBest Model: Decision Tree (max_depth=5)")

final_preds = best_model.predict(test)

submission = pd.DataFrame({
    "Id": test_ids,
    "SalePrice": final_preds
})
submission.to_csv("submission.csv", index=False)
print("\nsubmission.csv saved!")
print(submission.head())