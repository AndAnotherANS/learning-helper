import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


def load_data(path):
    df = pd.read_csv(path).dropna()
    x = df.loc[:, ['horizontal_ratio', 'vertical_ratio']].values
    y = df.loc[:, ["position_x", "position_y"]]
    return x, y

def train_model():
    x_train, y_train = load_data("calibration_data.csv")
    x_test, y_test = load_data("calibration_data_val.csv")



    model = make_pipeline(
        StandardScaler(),
        MultiOutputRegressor(
            TransformedTargetRegressor(regressor=SVR(C=1., gamma=0.2), transformer=StandardScaler())
        )
    )

    model.fit(x_train, y_train)

    print(model.score(x_test, y_test))
    return model


if __name__ == '__main__':
    train_model()