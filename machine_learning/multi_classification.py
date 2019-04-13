from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
import sys
sys.path.append('../')

from machine_learning.feature_selection import FeatureSelection


class MultiClassifier:
    def __init__(self, target_num=5):
        # KNN classifier
        self.knn = KNeighborsClassifier(n_neighbors=target_num)
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.data = pd.read_csv(os.path.join(self.data_dir, 'pandas_cleaned.csv'))

        selection = FeatureSelection()
        self.top_important_factors = selection.correlation()

        self.training_target = None
        self.test_target = None
        self.training_data = None
        self.test_data = None

        self.model = None

    def train_test_splitter(self, ratio, random_seed=1000):
        train_data = self.data.sample(frac=ratio, random_state=random_seed)
        test_data = self.data.drop(train_data.index)
        self.training_target = train_data.filter(['target'])
        self.test_target = test_data.filter(['target'])

        selected_train = train_data.filter(self.top_important_factors)
        select_test = test_data.filter(self.top_important_factors)

        # Minmax normalization
        self.training_data = (selected_train - selected_train.min()) / (selected_train.max() - selected_train.min())
        self.test_data = (select_test - select_test.min()) / (select_test.max() - select_test.min())

    def model_fitting(self):
        data = [_ for _ in self.training_data.values.tolist()]
        target = [int(_[0]) for _ in self.training_target.values.tolist()]
        self.knn.fit(data, target)

    def accuracy(self):
        test_result = self.knn.predict(self.test_data)
        test_target = [int(_[0]) for _ in self.test_target.values.tolist()]
        accurate_count = 0
        for i in range(len(test_result)):
            if test_result[i] == test_target[i]:
                accurate_count += 1
        accuracy = accurate_count / len(test_target)
        print('Accuracy: ', accuracy)
        return accuracy

    def run(self):
        percentage_list = list()
        accuracy_list = list()
        for i in range(10, 90):
            self.train_test_splitter(i / 100)
            self.model_fitting()
            percentage_list.append(i)
            accuracy_list.append(self.accuracy())
        plt.plot(percentage_list, accuracy_list)
        plt.title('KNN Multi Classifier')
        plt.xlabel('Percentages of training data %')
        plt.ylabel('Accuracy')
        plt.text(percentage_list[-1], accuracy_list[-1], accuracy_list[-1], ha='right', va='bottom', fontsize=12)
        plt.savefig(os.path.join(self.data_dir, 'KNN.png'))
        plt.show()

        # Dump the model
        with open(os.path.join(os.path.dirname(__file__), 'multiModel.pickle'), 'wb') as model:
            pickle.dump(self.knn, model)

    def predict(self, input_data):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'multiModel.pickle')):
            self.run()
        df = pd.DataFrame(input_data, index=[0])

        with open(os.path.join(os.path.dirname(__file__), 'multiModel.pickle'), 'rb') as file:
            model = pickle.load(file)
            return model.predict(df)[0]


if __name__ == "__main__":
    classifier = MultiClassifier()
    classifier.run()
    test = {"ca": 2,
            "oldpeak": 2.6,
            "thalach": 8,
            "cp": 3,
            "exang": 4}
    print(classifier.predict(test))