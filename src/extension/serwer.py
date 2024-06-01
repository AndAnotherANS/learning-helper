from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path='/templates')
CORS(app) 

UPLOAD_FOLDER = 'extension/data/'
IMAGES_NR = 0


@app.route('/captureImages.js')
# the file path is relative to serwer.py 
def serve_js():
    return send_from_directory('.', 'captureImages.js')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/C2')
def C2():
    return render_template("C2.html")

@app.route('/B2')
def B2():
    return render_template("B2.html")

@app.route('/A2')
def A2():
    return render_template("A2.html")

@app.route('/scripts/<path:filename>')
def serve_script(filename):
    return send_from_directory('scripts', filename)

@app.route('/C2/load_extension', methods=["GET"])
def start_record():
    print("in serwer oad extension")
    # Simulate a successful response
    response_data = {'success': True}
    return jsonify(response_data)

@app.route('/C2/upload', methods=['POST'])
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
    app.run(host='127.0.0.1', port=5000)