from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class ExpenseClassifier:


    def __init__(self):

        self.vectorizer = TfidfVectorizer()

        self.model = LogisticRegression(
            max_iter=1000
        )

        self.is_trained = False



    def train(self, descriptions, categories):

        X = self.vectorizer.fit_transform(
            descriptions
        )

        self.model.fit(
            X,
            categories
        )

        self.is_trained = True



    def predict(self, description):

        if not self.is_trained:
            return "Other"


        X = self.vectorizer.transform(
            [description]
        )

        prediction = self.model.predict(
            X
        )

        return prediction[0]