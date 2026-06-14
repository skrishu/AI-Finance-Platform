from models.expense_classifier import ExpenseClassifier
from models.training_data import descriptions, categories


model = ExpenseClassifier()


model.train(
    descriptions,
    categories
)


tests = [
    "I ordered food from Swiggy",
    "Netflix monthly payment",
    "Uber ride to office",
    "Bought a shirt online",
    "Paid electricity bill"
]


for text in tests:

    result = model.predict(text)

    print(
        f"{text} --> {result}"
    )