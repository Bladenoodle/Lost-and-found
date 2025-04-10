from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import items

app=Flask(__name__)
app.secret_key=config.secret_key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="GET":
        all_items=items.get_items()
        return render_template("index.html", items=all_items)
    if request.method=="POST":
        if "new_item" in request.form:
            return redirect("/new_item")
        if "logout" in request.form:
            return redirect("/logout")
        if "login" in request.form:
            return redirect("/login")
        if "sign_up" in request.form:
            return redirect("/register")

@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    if "return" in request.form:
        return redirect("/")
    else:
        item_name=request.form["item_name"]
        description=request.form["description"]
        status=request.form["status"]
        user_id=session["user_id"]

        items.add_item(item_name, description, status, user_id)

        return redirect("/")

@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def show_item(item_id):
    if request.method=="GET":
        item=items.get_item(item_id)
        return render_template("show_item.html", item=item)
    if request.method=="POST":
        if "remove" in request.form:
            return redirect("/remove_item/" + str(item_id))
        else:
            return redirect("/edit_item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item=items.get_item(item_id)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id=request.form["item_id"]
    item_name=request.form["item_name"]
    description=request.form["description"]
    status=request.form["status"]

    items.update_item(item_id, item_name, description, status)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    if request.method == "GET":
        item=items.get_item(item_id)
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    if "return" in request.form:
        return redirect("/")
    else:
        username=request.form["username"]
        password1=request.form["password1"]
        password2=request.form["password2"]
        if password1 != password2:
            return render_template("401.html")
        password_hash=generate_password_hash(password1)

        try:
            sql="INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return render_template("401.html")
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")

    if request.method=="POST":
        if "return" in request.form:
            return redirect("/")
        else:
            username=request.form["username"]
            password=request.form["password"]

            sql="SELECT id, password_hash FROM users WHERE username=?"
            result=db.query(sql, [username])

            if not result:
                return render_template("401.html")

            user=result[0]
            user_id=user["id"]
            password_hash=user["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"]=user_id
                session["username"]=username
                return redirect("/")
            else:
                return render_template("401.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")