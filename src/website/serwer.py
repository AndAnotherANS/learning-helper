from flask import Flask, request
app = Flask(__name__)

UPLOAD_FOLDER = '../data/'
IMAGES_NR = 0

@app.route('/')
def index():
    return 'Learning helper'

@app.route('/upload', methods=['POST'])
def upload_screenshot():
    global IMAGES_NR
    print("serwer")

    if 'screenshot' not in request.files or 'camera' not in request.files:
        return 'no screenshots'

    IMAGES_NR += 1
    screenshot = request.files['screenshot']
    screenshot.save(UPLOAD_FOLDER + 'screenshot/' + str(IMAGES_NR) + '.jpg')
    camera = request.files['camera']
    camera.save(UPLOAD_FOLDER + 'camera/' + str(IMAGES_NR) + '.jpg')

    return 'success from server'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')