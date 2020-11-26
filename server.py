from flask import Flask, render_template, request, Response
from PIL import Image

import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from tensorflow.keras import Input, Model

from image_preprocess import crop, preprocessing
from srgan import apply_srgan

app = Flask(__name__, template_folder="./templates/", static_url_path="/images", static_folder="images")

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/healthz", methods=["GET"])
def healthCheck():
   return "", 200

@app.route("/image", methods = ['POST'])
def get_result():
    if request.method == "POST":
        try:
        # ===================================================================
        #       SRGAN project 1-2
        #         - bicubic vs srgan
        # ===================================================================
    
            lr = Image.open(request.files['source'])
            lr = np.array(asarray(lr))

            srgan_hr = apply_srgan(lr)

            result = srgan_hr

        except Exception as e:
            print("error : %s" % e)
            return Response("fail", status=400)
        print("yes!")
    return srgan_hr

if __name__ == '__main__':
   app.run(host='0.0.0.0', port='80', debug=True)