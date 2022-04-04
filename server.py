from functools import wraps
import hashlib
import json
from flask import Flask,render_template, send_from_directory, request,Response
import jwt
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='client/build')
limiter = Limiter(app, key_func=get_remote_address)

def Hash (string):
    return hashlib.sha256(bytes(str(string), "utf-8")).hexdigest()

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
    # Different id each time but verifiable that the total was $1
    return iv + Hash(Hash("Hindi Cheeni Bhai Bhai") + iv + Hash(username) + Hash(total))

with open("mp.json","r") as f:
    friend_map = json.load(f)["map"]

with open("fernet_key.txt","rb") as f:
    fernet = Fernet(f.read())

with open("usernames.txt","r") as f:
    usernames = f.read().split("\n")

base = Hash("Satyameva Jayate")

def get_bereal_i_to_id (username, i):
    userint = int(Hash(base + Hash(username))[:4],16)
    # Only 0 is same for every user, can tell them to find a specific id corresponding to 0 in spec
    # Every other index depends on username (multiplied by some deterministic "userint")
    num = bytes(str(int(base[:4],16) + userint * i), "utf-8")
    return fernet.encrypt(num).decode()

def get_bereal_id_to_i (username, id):
    userint = int(Hash(base + Hash(username))[:4],16)
    try:
        num = int(fernet.decrypt(bytes(id, "utf-8")))
    except:
        return -1
    
    i = (num - int(base[:4],16)) // userint
    return i

usernamebase = Hash("Angoor Khatte Hain")

def get_bereal_username_to_i (username, id):
    try:
        user_i = usernames.index(id.upper())
    except:
        return -1
    offset = int(Hash(usernamebase + Hash(username))[:4],16)
    return (offset + user_i) % len(friend_map)

def get_bereal_id_to_username (username, id):
    i = get_bereal_id_to_i(username, id)
    if i == -1: return None
    offset = int(Hash(usernamebase + Hash(username))[:4],16)
    user_i = (i - offset) % len(friend_map)
    return usernames[user_i].lower()

def generate_friends_map(n=1000, f=10): # Number of people, avg number of friends
    # MAKE SURE THERE ARE N USERNAMES!!
    rng = list(range(n))
    mp = [[] for i in range(n)]
    for i in range(n*f):
        # Choose arbitrary sample of two people to be friends
        f1, f2 = random.sample(rng, 2)
        mp[f1].append(f2)
        mp[f2].append(f1)

    with open("mp.json","w") as f:
        json.dump({"map":mp},f)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        error_message = {"Error":'a valid token is missing'}, 403
        if 'x-access-token' in request.headers:
            try:
                token = jwt.decode(request.headers['x-access-token'], "", algorithms='HS256')
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

@app.route("/api/getpassword", methods=["GET"])
@limiter.limit("10/minute")
def forgotpassword():
    try:
        username = request.args.get("username")
        return get_password(username)
    except:
        return {"Error": "Can not get password"}, 400

@app.route("/api/authenticate", methods=["GET"])
@limiter.limit("10/minute")
def authenticate():
    error_message = {"Error":'invalid credentials'}, 403
    cookies = request.cookies
    try:
        body = request.args.to_dict()
    except:
        body = {}
    if "username" in body and "password" in body:
        if get_password(body["username"]) != body["password"]:
            return error_message

    elif "jwt" in cookies:
            giventoken = jwt.decode(cookies.get('jwt'), "")
            if "username" not in giventoken:
                return error_message
    else:
        return error_message

    token = jwt.encode(get_jwt(body["username"], get_password(body["username"])), "")
    r = Response()
    r.set_cookie(key='jwt',value=token, httponly=True)
    return {"Token": token}

@limiter.limit("10/minute")
@app.route("/api/data/from/<frm>/to/<to>", methods = ["GET"])
@token_required
def data(username, frm, to):
    try:
        frm = int(frm)
        to = int(to)
    except:
        return {"Error": "Bounds not integers"}, 400

    if abs(frm - to) > 100:
        return {"Error": "Too much data requested"}, 400

    return {
        "Index": [i for i in range(frm, to+1)],
        "Data": get_generic_data(username, frm, to)
    }

@limiter.limit("10/minute")
@app.route("/api/snackpass/submit", methods = ["POST"])
@token_required
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

@limiter.limit("10/minute")
@app.route("/api/bereal/suggestion", methods = ["GET"])
@token_required
def bereal_friend_suggestion(username):
    ids = request.args.get("usernames")
    if not ids:
        return {"Error": "Need at least one id in a comma separated list"}
    else:
        ids = ids.split(",")
    suggestions = set()
    for id in ids:
        if id != "":
            i = get_bereal_username_to_i(username, id)
            if i > 0 and i < len(friend_map):
                suggestions.update([get_bereal_i_to_id(username, j) for j in friend_map[i]])
    
    # Make people do one id in each request
    suggestions = random.sample(list(suggestions),len(suggestions)//len(ids))
    return {"Suggestions": suggestions}

@limiter.limit("10/minute")
@app.route("/api/bereal/username/<id>", methods = ["GET"])
@token_required
def bereal_get_username(username, id):
    username = get_bereal_id_to_username(id)
    if username:
        return {"Username": username}
    else:
        return {"Error": "ID not found"}, 402

@limiter.limit("10/minute")
@app.route("/api/bereal/myid", methods = ["GET"])
@token_required
def bereal_myid(username):
    return {"ID": get_bereal_i_to_id(username,101)}

@app.route("/api", methods = ["GET"])
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
