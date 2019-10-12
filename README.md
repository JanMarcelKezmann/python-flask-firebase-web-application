# Flask Firebase Web application with Python
<p>The International Skin Imaging Collaboration: Melanoma Project is an academia and industry partnership designed to facilitate the application of digital skin imaging to help reduce melanoma mortality. When recognized and treated in its earliest stages, melanoma is readily curable. Based on the <a href="https://www.isic-archive.com/#!/onlyHeaderTop/gallery">ISIC Detection Dataset</a> with over 23.000 images of skin lesions, labeled as 'benign' or 'malignant', the web application provides a Hands on API for uploading and classifiying and image easily.</p>
<p>Included in the WebApp is a SignUp and Login functionality as well as a database provided for user account information all based onto firebase. In addition to it a paywall is added with two options: Paypal and Stripe. So all potential users should be able to handle a payment for a fast and accurate diagnosis.</p>

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

## Some insights
<p align="center">
  <img src="https://user-images.githubusercontent.com/50111329/66697454-11f5f900-ecd6-11e9-9895-e1e243105a1d.png" width="800px" alt="">
</p>

<p></p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/50111329/66697537-c001a300-ecd6-11e9-810c-958e35f76d7a.png" width="800px" alt="">
</p>

## References
- <a href="https://www.isic-archive.com/#!/topWithHeader/tightContentTop/about/isicArchive">ISIC-Archive.com</a>
