import cv2
import numpy as np
import base64
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from keras.models import load_model
from detecthuman import *
import imutils

# from house3d_worker_demo import process_img

app = Flask(__name__)
CORS(app)

@app.route("/detectCNN", methods=["POST"])
def convert_img_color():
    # Doc anh gui len tu phia client
    print(request.files)
    filestr = request.files['image']
    # print(filestr)
    # Do anh duoc gui len co dang du lieu chuoi (string),
    # can duoc chuyen doi sang dang ma tran numpy
    # de tien thao tac ve sau
    npimg = np.fromfile(filestr, np.uint8)
    # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan

    img = cv2.imdecode(npimg, cv2.COLOR_BGR2RGB)
    # img=imutils.resize(img, width=64, height=128)
    print(img)
    cv2.imwrite('./images/test.jpg', img)

    _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    pos_filepath = './images/test.jpg'
    pos_img = human_objector_cnn(pos_filepath)
    _, im_arr = cv2.imencode('.jpg', pos_img)
    cv2.imwrite('./images/result.jpg', pos_img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)

    return im_b64

if __name__ == '__main__':
    cnn_model = load_model('./Model/model_cnn_wieghts.h5')
    human_objector_cnn = ObjectDetector(cnn_model=cnn_model)
    app.run(debug=True, host='localhost',  port=5500, use_reloader=True)
