# Flask Firebase Web application with Python

## Getting started

- Clone this repo 
- Install requirements
- Run the script
- Check http://localhost:5000
- Done! :tada:


## Local Installation

### Clone the repo
```shell
git clone https://github.com/JanMarcelKezmann/python-flask-firebase-web-application.git
```

### Install requirements

```shell
pip install -r requirements.txt
```

Make sure you have the following installed:
- tensorflow
- keras
- flask
- pillow
- h5py
- gevent
- flask_dropzone
- pyrebase
- numpy
- stripe
- paypalrestsdk
- werkzeug

### Run with Python (3.6)

Python 3.6 is supported and tested.

#### For Linux & Windows
```shell
python app.py
```

### Try it out!

Open http://localhost:5000 or http://127.0.0.1:5000 and have fun. :smiley:

## Accuracy Information

<p>Training the model with a on the imagenet dataset pretrained InceptionV3 model gives the follwing scores:</p>

- Accuracy: 0.831
- F1 Score: 0.8456
- Precision Score: 0.925
- Recall Score: 0.7786

<p>The Confusion Matrix of the Model evaluated on 2000 images</p>
<p align="left">
  <img src="https://user-images.githubusercontent.com/50111329/66696879-30f18c80-ecd0-11e9-9a94-5f6faadca9b3.png" width="400px" alt="">
</p>
