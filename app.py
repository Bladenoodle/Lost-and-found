from flask import Flask
from flask import make_response, abort, redirect, render_template, request, session
import config
import items
import users
import claims
import sqlite3
import time

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter("datetimeformat")
def datetime_format(value):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value))

def require_login():
    if "user_id" not in session:
        abort(403)

def limit_length(string, maxlength):
    if len(string)>maxlength or len(string) == 0:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query", "")
    status = request.args.get("status", "")
    location = request.args.get("location", "")
    results = items.find_item(query, status, location)
    return render_template("find_item.html", query=query, status=status, location=location, results=results)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    if "return" in request.form:
        return redirect("/")
    if "add" in request.form:
        item_name = request.form["item_name"]
        limit_length(item_name, 50)
        description = request.form["description"]
        limit_length(description, 1000)
        status = request.form["status"]
        user_id = session["user_id"]

        all_classes = items.get_all_classes()

        classes = []
        for entry in request.form.getlist("classes"):
            if entry:
                parts = entry.split(":")
                if parts[0] not in all_classes:
                    abort(403)
                if parts[1] not in all_classes[parts[0]]:
                    abort(403)
                classes.append((parts[0], parts[1]))

        upload_time = int(time.time())
        edit_time = upload_time

        items.add_item(item_name, description, status, user_id, classes, upload_time, edit_time)

        return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    all_claims = claims.get_claims(item_id)
    classes = items.get_classes(item_id)
    images = items.get_images(item_id)

    return render_template("show_item.html", item=item, classes=classes, all_claims=all_claims, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")

    return response

@app.route("/edit_images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    images = items.get_images(item_id)

    return render_template("edit_images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    file = request.files["image"]

    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if not file.filename.endswith(".png"):
        return "VIRHE: väärä tiedostomuoto"

    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"

    item_id = request.form["item_id"]
    if not item_id:
        abort(403)

    items.add_image(item_id, image)
    return redirect("/edit_images/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)

    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes = items.get_all_classes()
    item_classes = {}
    for item_class in all_classes:
        item_classes[item_class] = ""
    for entry in items.get_classes(item_id):
        item_classes[entry["item_class_name"]] = entry["value"]
    return render_template("edit_item.html", item=item, all_classes=all_classes, item_classes=item_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if "return" in request.form:
        return redirect("/item/" + str(item_id))

    if "save" in request.form:
        item_name = request.form["item_name"]
        limit_length(item_name, 50)
        description = request.form["description"]
        limit_length(description, 1000)
        status = request.form["status"]

        all_classes = items.get_all_classes()

        classes = []
        for entry in request.form.getlist("classes"):
            if entry:
                parts = entry.split(":")
                if parts[0] not in all_classes:
                    abort(403)
                if parts[1] not in all_classes[parts[0]]:
                    abort(403)
                classes.append((parts[0], parts[1]))

        edit_time = int(time.time())
        items.update_item(item_id, item_name, description, status, classes, edit_time)

        return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/create_claim", methods=["POST"])
def create_claim():
    require_login()

    contact_info = request.form["contact_info"]
    limit_length(contact_info, 100)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    if claims.get_claim_by_user(item_id, user_id):
        old_claim = claims.get_claim_by_user(item_id, user_id)
        return render_template("replace_claim.html", old_claim=old_claim, contact_info=contact_info)
    else:
        claims.add_claim(item_id, user_id, contact_info)
        return redirect("/item/" + str(item_id))

@app.route("/remove_claim/<int:claim_id>", methods=["POST"])
def remove_claim(claim_id):
    require_login()
    claim = claims.get_claim_by_id(claim_id)
    if not claim:
        abort(404)
    if claim["user_id"] != session["user_id"]:
        abort(403)

    item_id = claim["item_id"]
    claims.remove_claim(claim_id)
    return redirect("/item/" + str(item_id))

@app.route("/replace_claim/<int:claim_id>", methods=["POST"])
def replace_claim(claim_id):
    require_login()
    claim = claims.get_claim_by_id(claim_id)
    if not claim:
        abort(404)
    if claim["user_id"] != session["user_id"]:
        abort(403)
    new_contact_info = request.form["contact_info"]
    if not new_contact_info:
        abort(404)

    if "return" in request.form:
        return redirect("/item/" + str(claim[1]))
    if "replace" in request.form:
        claims.replace_claim(claim_id, new_contact_info)
        return redirect("/item/" + str(claim[1]))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods = ["POST"])
def create():
    if "return" in request.form:
        return redirect("/")
    if "signup" in request.form:
        username = request.form["username"]
        limit_length(username, 30)
        password1 = request.form["password1"]
        limit_length(password1, 50)
        password2 = request.form["password2"]
        limit_length(password2, 50)
        if password1 != password2:
            return render_template("reject.html", password=True)
        try:
            users.create_user(username, password1)
            user_id = users.check_login(username, password1)
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        except sqlite3.IntegrityError:
            return render_template("reject.html", username=True)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        if "return" in request.form:
            return redirect("/")
        if "login" in request.form:
            username = request.form["username"]
            password = request.form["password"]

            user_id = users.check_login(username, password)

            if user_id:
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return render_template("reject.html", login=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")