# -*- coding: utf-8 -*-#
'''
# Name:         main
# Description:  
# Author:       neu
# Date:         2020/7/30
'''
from PIL import Image
import base64

import numpy as np
from flask import render_template, Flask, request

from keras.models import load_model

import tensorflow as tf
graph = tf.get_default_graph()

model = load_model('model.h5')

def data_process(data):
    data = np.array(data)
    data = data.reshape((1, 28, 28, 1))
    data = data.astype('float64')/255
    return data

app = Flask(__name__)
@app.route('/predict', methods=['POST', 'GET'])
def predict_data():
    t = request.form['file']
    t = t[23:]
    image = base64.b64decode(t)
    path = "test.jpeg"
    file = open(path, 'wb')
    file.write(image)
    file.close()
    # image = request.files.get('file')
    # print(image)
    # file_path = image.filename
    # image.save(file_path)

    # read image and convert to gray
    # data = Image.open(file_path).convert('L')
    data = Image.open(path).convert('L')
    data = data.resize((28,28))
    data = np.array(data, 'f')



    data = data_process(data)
    print(data.shape)
    # global graph
    # with graph.as_default():
    model.predict(np.zeros((1, 28, 28, 1)))
    # model.predict(data)
    result = model.predict(data)  # 修改的代码。。。。。。

    # print("res", result)
    return str(result.argmax())

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run("127.0.0.1", port=5001)