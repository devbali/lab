from functools import wraps
import hashlib
import json
from flask import Flask,render_template, send_from_directory, request,Response
import jwt
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random

app = Flask(__name__, static_folder='client/build')
limiter = Limiter(app, key_func=get_remote_address)

def Hash (string):
    return hashlib.sha256(string).hexdigest()


def get_password (username):
    return Hash(Hash("Inquilaab Zindabaad") + Hash(username))

def get_jwt(username, password):
    return {
        "username": username,
        "access_token": Hash(Hash("Laal Salaam")+Hash(username)+Hash(password))
        }

def get_generic_data (username, frm, to):
    return [
        int(Hash(Hash("Jai Jawaan Jai Kisaan") + Hash(username) + str(i))[:4],16) 
        for i in range(frm, to+1)
        ]

def get_snackpass_receipt_id (username, total):
    iv = Hash(random.randbytes(16))
    # Different id each time but verifiable that the total was 0
    return iv + Hash(iv + Hash(username) + Hash(total))

def get_bereal_friend_id (username, id):
    userint = int(Hash(Hash("Satyameva Jayate") + Hash(username))[:4],16)
    # Only 0 is same for every user, can tell them to find a specific id corresponding to 0 in spec
    # Every other index depends on username
    return Hash(Hash("Satyameva Jayate") + Hash(str(userint * id)))

def generate_friends_map(n=1000): 
    rng = list(range(n))
    mp = []
    for i in range(n):
    # Choose arbitrary sample of upto half of the entire network to be any user's friend
        mp.append(random.sample(rng[:i]+rng[i+1:], random.choice(rng)//20))
    with open("mp.json","w") as f:
        json.dump({"map":mp},f)

with open("mp.json","r") as f:
    friend_map = json.load(f)["map"]

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        error_message = {"Error":'a valid token is missing'}, 403
        
        if 'x-access-token' in request.headers:
            try:
                token = jwt.decode(request.headers['x-access-token'])
            except:
                return error_message

            if "username" not in token or "access_token" not in token:
                return error_message

            if token["access_token"] != get_jwt(token["username"], get_password(token["username"]))["access_token"]:
                return error_message
        else:
            return error_message
 
        return f(token["username"], *args, **kwargs)
    return decorator

@app.route("/api/authenticate", methods=["POST"])
@limiter.limit("10/minute")
def authenticate():
    error_message = {"Error":'invalid credentials'}, 403
    cookies = request.cookies
    try:
        body = request.json
    except:
        body = {}
    if "username" in body and "password" in body:
        if get_password(body["username"]) != body["password"]:
            return error_message

    elif "jwt" in cookies:
            token = jwt.decode(cookies.get('jwt'))
            if "username" not in token:
                return error_message
    else:
        return error_message

    token = jwt.encode(get_jwt(token["username"], get_password(token["username"])))
    Response.set_cookie('jwt',token, httponly=True)

@token_required
@limiter.limit("10/minute")
@app.route("/api/data/from/:from/to/:to")
def data(username, frm, to):
    if abs(frm - to) > 100:
        return {"Error": "Too much data requested"}, 400

    return {
        "Index": [i for i in range(frm, to+1)],
        "Data": get_generic_data(username, frm, to)
    }

@token_required
@limiter.limit("10/minute")
@app.route("/api/snackpass/submit", method = ["POST"])
def snack_pass_receipt(username):
    try:
        body = request.json
    except:
        body = {}
    if "items" in body and body["items"]:
        price = 10
        if "coupon_code" in body and "price" in body:
            price = body["price"]
        return {"Message":"Success!", "Receipt_ID": get_snackpass_receipt_id (username, price)}, 200
    else:
        return {"Error": "No items in body"}, 400

@token_required
@limiter.limit("10/minute")
@app.route("/api/bereal/suggestion", method = ["GET"])
def bereal_friend_suggestion(username):
    ids = request.args.get("ids").split(",")
    for id in ids:
        if id != "":
            pass # TODO


@app.route("/api")
@limiter.limit("10/minute")
def helloworld():
  return "Hello World"

@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have exceeded your rate-limit"

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
  app.run(debug=True)
