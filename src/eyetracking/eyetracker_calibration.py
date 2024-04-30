import os
import random

import cv2
import numpy as np
import pandas as pd
from gaze_tracking import GazeTracking

from sklearn.compose import TransformedTargetRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


def collect_calibration_data():
    data = []

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    position = (250, 250)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    counter = 0

    resolution = (1080, 1920)

    while True:

        frame = np.ones((resolution[0], resolution[1], 3), np.uint8) * 255
        cv2.circle(frame, position, 10, (0,255,0) if counter < 10 else (0, 0, 0), -1)

        cv2.imshow('image', frame)

        _, cam_frame = webcam.read()
        gaze.refresh(cam_frame)

        counter += 1
        if counter > 10:
            if gaze.horizontal_ratio() is not None:
                data.append([gaze.horizontal_ratio(), gaze.vertical_ratio(),
                             gaze.pupil_left_coords()[0], gaze.pupil_left_coords()[1],
                             gaze.pupil_right_coords()[0], gaze.pupil_right_coords()[1],
                             position[0], position[1]])

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        if counter > 20:
            position = (random.randint(0, resolution[1]), random.randint(0, resolution[0]))
            counter = 0

    webcam.release()
    cv2.destroyAllWindows()

    data = pd.DataFrame(data, columns=['horizontal_ratio', 'vertical_ratio',
                                       'pupil_left_coords_x', 'pupil_left_coords_y',
                                       'pupil_right_coords_x', 'pupil_right_coords_y',
                                       'position_x', 'position_y'])

    data.dropna().to_csv(os.environ["PROJECT_DIR"] + '\\data\\calibration_data.csv')
    return data

def test_calibration(model):
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    position_history = [(250, 250) for i in range(10)]
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    resolution = (1080, 1920)

    def mean(tuple_li):
        return sum([x[0] for x in tuple_li])/len(tuple_li),\
            sum([x[1] for x in tuple_li]) / len(tuple_li)

    while True:
        _, cam_frame = webcam.read()
        gaze.refresh(cam_frame)

        if gaze.horizontal_ratio() is not None:
            data = np.array([gaze.horizontal_ratio(), gaze.vertical_ratio()]).reshape(1, -1)
            y = model.predict(data)
            position_history.append((y[:, 0], y[:, 1]))
            position_history.pop(0)

        frame = np.ones((resolution[0], resolution[1], 3), np.uint8) * 255
        cv2.circle(frame, mean(position_history), 10, (0, 0, 0), -1)

        cv2.imshow('image', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break


    webcam.release()
    cv2.destroyAllWindows()



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
    collect_calibration_data()
    model = train_model()
    test_calibration(model)
