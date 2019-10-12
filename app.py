from __future__ import division, print_function

import warnings
warnings.filterwarnings('ignore')

from functools import wraps
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import re
import sys
# coming from pyrebase4
import pyrebase
import numpy as np
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR) # suppress keep_dims warnings


# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model, Sequential
from keras.preprocessing import image
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D

# Flask
from flask_dropzone import Dropzone
from flask import Flask, render_template, jsonify, redirect, request, url_for, session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Stripe for payment
import stripe
import paypalrestsdk

#firebase config
config = {
  "apiKey": "AIzaSyBFODsG2_9uQuWF1d7DdbNO5Y3d4nZulsA",
  "authDomain": "my-free-ai-classifier.firebaseapp.com",
  "databaseURL": "https://my-free-ai-classifier.firebaseio.com",
  "projectId": "my-free-ai-classifier",
  "storageBucket": "my-free-ai-classifier.appspot.com",
  "messagingSenderId": "627427593802",
  "appId": "1:627427593802:web:afd77103dbb9bf6ff8e0b3",
  "measurementId": "G-EM8S80GF9Z"
}

#init firebase
firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#real time database instance
db = firebase.database();
#storage
storage = firebase.storage()

basedir = os.path.abspath(os.path.dirname(__file__))
#new instance of Flask
app = Flask(__name__)
#secret key for the session
app.secret_key = os.urandom(24)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=1,
    DROPZONE_MAX_FILES=1,
    DROPZONE_UPLOAD_ON_CLICK=True
)

pub_key = "pk_test_tqCJtQ9f6ouxRfOkIUPDCvmO00q8KBcx76"
secret_key = 'sk_test_EdDZTBF0gjSY7BSRpxJyoVc100SlEO9YWZ'
stripe.api_key = secret_key

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ASF4dbyuop0frtNbQ6OcL9SYKWVc8SapXAd_bs2bwUVa848ukQ7L6h-Rc0tHtGn-UnaS-09jdPtQzseA",
  "client_secret": "EDl_r9g1frB4FYspNONTI-pEtc93RuSJWyIkTxFZqCYbB8eE07nnd7NBjUVu445bOonZqPVcaTIA7aYD"
  })


dropzone = Dropzone(app)

# Initializing Model for image classification
model = Sequential()
model.add(Conv2D(32, (3, 3), activation = 'relu', padding = 'same', input_shape = (32, 32, 3)))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.load_weights("ISIC Detection Model.h5")

graph = tf.get_default_graph()

#decorator to protect routes
def isAuthenticated(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
      #check for the variable that pyrebase creates
      if not auth.current_user != None:
          return redirect(url_for('login'))
      return f(*args, **kwargs)
  return decorated_function

def model_predict(img_path, model):
  img = image.load_img(img_path, target_size=(32, 32))

  # Preprocessing the image
  x = image.img_to_array(img)
  # x = np.true_divide(x, 255)
  x = np.expand_dims(x, axis=0)

  preds = model.predict(x)
  if np.round(preds[0][0]).astype(int) == 0:
    preds = "Benign"
  else:
    preds = "Malignant"
  return preds

#index route / Main Page
@app.route("/", methods=["POST", "GET"])
def index():
  if auth.current_user != None:
    # if request.method == "POST":
    #   for key, f in request.files.items():
    #     if key.startswith("file"):
    #       f.save(os.path.join(app.config["UPLOADED_PATH"], f.filename))
    #       file_place = "uploads/" + f.filename
    #       storage.child(auth.current_user["localId"]).child("images").child(f.filename).put(file_place, auth.current_user["idToken"])
    session_username = db.child("users").child(auth.current_user["localId"]).child("username").get().val()
    creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
    return render_template("index.html", pub_key=pub_key, session_username=session_username, creditpoints=creditpoints)
  return render_template("index.html", user_not_authenticated=True)

#signup route
@app.route("/signup", methods=["GET", "POST"])
# @isNotLoggedIn
def signup():
  if request.method == "POST":
    #get the request form data
    email = request.form["email"]
    password = request.form["password"]
    username = request.form["username"]
    try:
      #create the user
      auth.create_user_with_email_and_password(email, password);
      #login the user right away
      user = auth.sign_in_with_email_and_password(email, password)   
      #session
      user_id = user['idToken']
      user_email = email
      session['usr'] = user_id
      session["email"] = user_email
      
      user_data = {"firstname": "", "lastname": "", "username": username, "creditpoints": 1}
      db.child("users").child(auth.current_user["localId"]).update(user_data)

      return redirect("/") 
    except:
      return render_template("signup.html", message="Email is already taken or password has less than 6 letters" )  

    return render_template("signup.html")
  return render_template("signup.html")


#login route
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    #get the request data
    email = request.form["email"]
    password = request.form["password"]
    try:
      #login the user
      user = auth.sign_in_with_email_and_password(email, password)
      #set the session
      user_id = user['idToken']
      user_email = email
      session['usr'] = user_id
      session["email"] = user_email

      return redirect("/")
    except:
      return render_template("login.html", message="Wrong Credentials")
  return render_template("login.html")

#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None

    session.clear()
    return redirect("/");

@app.route("/profile", methods=["POST", "GET"])
@isAuthenticated
def profile():
  user_data = db.child("users").child(auth.current_user["localId"]).get().val()
  creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()

  if request.method == "POST":
    #get the request form data
    # email = request.form["email"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]

    # Check if a change was made
    # If no (input field is empty) than overwrite the update info with the previous information
    # Do this for every asked information
    # if email == "":
    #   email = user_data["email"]
    # elif email != "":
    #   auth.setAccountInfo
    if firstname == "":
      firstname = user_data["firstname"]
    if lastname == "":
      lastname = user_data["lastname"]
    if username == "":
      username = user_data["username"]

    user_data = {"firstname": firstname, "lastname": lastname, "username": username, "creditpoints": 0}
    db.child("users").child(auth.current_user["localId"]).update(user_data)

    # next line could in theory be forgotten
    user_data = db.child("users").child(auth.current_user["localId"]).get().val()
    return render_template("profile.html", user_infos=user_data, session_username=username, creditpoints=creditpoints)
  return render_template("profile.html", user_infos=user_data, session_username=user_data["username"], creditpoints=creditpoints)

@app.route("/imageclassification", methods=["GET", "POST"])
@isAuthenticated
def imageclassification():
  creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
  session_username = db.child("users").child(auth.current_user["localId"]).child("username").get().val()
  # if creditpoints == 0:
  #   return render_template("image.html", pub_key=pub_key, creditpoints=creditpoints, session_username=session_username)
  
  return render_template("image.html", pub_key=pub_key, creditpoints=creditpoints, session_username=session_username)

@app.route("/pay", methods=["POST"])
@isAuthenticated
def pay():
  customer = stripe.Customer.create(email=request.form["stripeEmail"], source=request.form["stripeToken"])
  
  charge = stripe.Charge.create(
    customer=customer.id,
    amount=1697,
    currency="eur",
    description="diagnosis"
    )

  old_creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
  new_creditpoints = int(old_creditpoints) + 1
  db.child("users").child(auth.current_user["localId"]).update({"creditpoints": new_creditpoints})

  return redirect("/")

@app.route("/payment", methods=["GET", "POST"])
@isAuthenticated
def payment():

  payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
      "payment_method": "paypal"},
    "redirect_urls": {
      "return_url": "http://127.0.0.1:5000/payment/execute",
      "cancel_url": "http://127.0.0.1:5000/"},
    "transactions": [{
      "item_list": {
        "items": [{
          "name": "diagnosis",
          "sku": "11111",
          "price": "16.97",
          "currency": "EUR",
          "quantity": 1}]},
      "amount": {
        "total": "16.97",
        "currency": "EUR"},
      "description": "This is the payment transaction description."}]})

  if payment.create():
    print('Payment success!')
  else:
    print("here")
    print(payment.error)

  return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=["GET", 'POST'])
@isAuthenticated
def execute():
  success = False

  payment = paypalrestsdk.Payment.find(request.form['paymentID'])

  if payment.execute({'payer_id' : request.form['payerID']}):
    print('Execute success!')
    success = True
    old_creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
    new_creditpoints = int(old_creditpoints) + 1
    db.child("users").child(auth.current_user["localId"]).update({"creditpoints": new_creditpoints})
  else:
    print("there")
    print(payment.error)

  # return render_template("/image.html", creditpoints=new_creditpoints)
  return jsonify({'success' : success})


@app.route("/predict", methods=["GET", "POST"])
def upload():
  global graph
  with graph.as_default():
    if request.method == 'POST':
      # Get the file from post request
      f = request.files['image']

      # Save the file to ./uploads
      basepath = os.path.dirname(__file__)
      file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
      f.save(file_path)
      
      file_place = "uploads/" + f.filename
      storage.child(auth.current_user["localId"]).child("images").child(f.filename).put(file_place, auth.current_user["idToken"])

      # Make prediction
      preds = model_predict(file_path, model)

      # subtract one creditpoint
      old_creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()
      new_creditpoints = int(old_creditpoints) - 1
      db.child("users").child(auth.current_user["localId"]).update({"creditpoints": new_creditpoints})
      
      return preds
    return None

#run the main script
if __name__ == "__main__":
  # app.run(debug=True)
    # Serve the app with gevent
  http_server = WSGIServer(('0.0.0.0', 5000), app)
  http_server.serve_forever()
