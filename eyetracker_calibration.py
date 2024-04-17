import random

import cv2
import numpy as np
import pandas as pd
from gaze_tracking import GazeTracking

import linear_model


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
    return data

def test_calibration(model):
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    position_history = [(250, 250) for i in range(10)]
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    resolution = (1080, 1920)

    def mean(tuple_li):
        return sum([x[0] for x in position_history])/len(position_history),\
            sum([x[1] for x in position_history]) / len(position_history)

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


if __name__ == '__main__':

    model = linear_model.train_model()
    test_calibration(model)
    '''
    data = collect_calibration_data().dropna()
    data.to_csv('calibration_data_test.csv')
    print("ok")'''