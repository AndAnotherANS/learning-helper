import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC, SVR


def load_data(path):
    df = pd.read_csv(path).dropna()
    x = df.loc[:, ['horizontal_ratio', 'vertical_ratio']].values
    y1 = df.loc[:, "position_x"].values
    y2 = df.loc[:, "position_y"].values
    return x, y1, y2

def train_model():
    x_train, y1_train, y2_train = load_data("calibration_data.csv")
    x_test, y1_test, y2_test = load_data("calibration_data_val.csv")

    model1 = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model2 = make_pipeline(PolynomialFeatures(3), LinearRegression())

    model1.fit(x_train, y1_train)
    model2.fit(x_train, y2_train)

    print(model1.score(x_test, y1_test))
    print(model2.score(x_test, y2_test))
    return model1, model2

if __name__ == '__main__':
    train_model()