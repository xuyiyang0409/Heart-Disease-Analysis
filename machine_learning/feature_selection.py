from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('../')

from backend.db_handler import DBHandler


class FeatureSelection:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.data = pd.read_csv(os.path.join(self.data_dir, 'pandas_cleaned.csv'))
        self.train_data = self.data.filter(['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
                                            'exang', 'oldpeak', 'slope', 'ca'])
        self.train_target = self.data.filter(['target'])
        self.db_controller = DBHandler()

    def l1_regularization(self, display=False):
        linear_svc = LinearSVC(C=0.01, penalty='l1', dual=False, max_iter=1000).\
            fit(self.train_data, [int(_[0]) for _ in self.train_target.values.tolist()])
        model = SelectFromModel(linear_svc, prefit=True)

        new_data = model.transform(self.train_data)
        indicator = model.get_support()
        column = self.db_controller.get_column_names('Rawdata')
        if display:
            for i in range(len(indicator)):
                if not indicator[i]:
                    print("[L1 Regularization] This feature is filtered: '{}'".format(column[i]))
        return new_data, self.train_target

    def correlation(self, display=False):
        correlation_matrix = self.data.corr(method='pearson')
        correlation_matrix = correlation_matrix.filter(['target'])[:-2]
        most_corr_list = sorted(correlation_matrix.to_dict()['target'].items(), key=lambda item: abs(item[1]),
                                reverse=True)
        if display:
            print("[Pearson Correlation] The correlation factors between attributes and target are following:")
            print(correlation_matrix)
            print('\n[Pearson Correlation] The top 5 most important factors are:')

        top_important_list = list()
        for i in range(5):
            if display:
                print(f"Top {i + 1}: '{most_corr_list[i][0]}'")
            top_important_list.append(most_corr_list[i][0])

        plt.barh([_[0] for _ in most_corr_list], [_[1] for _ in most_corr_list], color='red')
        plt.xlabel('Pearson correlation coefficients')
        plt.title('Feature Selection')
        plt.savefig(os.path.join(self.data_dir, 'FS.png'))
        plt.show()

        self.db_controller.database_controller('DELETE FROM Impfactor;')
        self.db_controller.database_controller("INSERT INTO Impfactor VALUES "
                                               "('{}', '{}', '{}', '{}', '{}');".
                                               format(most_corr_list[0][0], most_corr_list[1][0],
                                                      most_corr_list[2][0], most_corr_list[3][0],
                                                      most_corr_list[4][0]))
        return top_important_list


if __name__ == "__main__":
    selecter = FeatureSelection()
    print(selecter.correlation(display=True))
    print(selecter.l1_regularization(display=True))