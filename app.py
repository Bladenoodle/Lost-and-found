from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import items
import users

app=Flask(__name__)
app.secret_key=config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def limit_length(string, maxlength):
    if len(string)>maxlength or len(string)==0:
        abort(403)

@app.route("/")
def index():
    all_items=items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/find_item")
def find_item():
    query=request.args.get("query")
    if query:
        results=items.find_item(query)
    else:
        query=""
        results=[]
    return render_template("find_item.html", query=query, results=results)

@app.route("/new_item")
def new_item():
    require_login()
    classes=items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    if "return" in request.form:
        return redirect("/")
    if "add" in request.form:
        item_name=request.form["item_name"]
        limit_length(item_name, 50)
        description=request.form["description"]
        limit_length(description, 1000)
        status=request.form["status"]
        user_id=session["user_id"]

        classes=[]
        for entry in request.form.getlist("classes"):
            if entry:
                parts=entry.split(":")
                classes.append((parts[0], parts[1]))
        items.add_item(item_name, description, status, user_id, classes)

        return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item=items.get_item(item_id)
    if not item:
        abort(404)
    classes=items.get_classes(item_id)
    return render_template("show_item.html", item=item, classes=classes)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if not item:
        abort(404)

    if item["user_id"]!=session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id=request.form["item_id"]
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"]!=session["user_id"]:
        abort(403)

    if "return" in request.form:
        return redirect("/item/" + str(item_id))

    if "save" in request.form:
        item_name=request.form["item_name"]
        limit_length(item_name, 50)
        description=request.form["description"]
        limit_length(description, 1000)
        status=request.form["status"]

        items.update_item(item_id, item_name, description, status)

        return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"]!=session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user=users.get_user(user_id)
    if not user:
        abort(404)
    items=users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    if "return" in request.form:
        return redirect("/")
    if "signup" in request.form:
        username=request.form["username"]
        password1=request.form["password1"]
        password2=request.form["password2"]
        if password1 != password2:
            return render_template("401.html")
        try:
            users.create_user(username, password1)
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
        if "login" in request.form:
            username=request.form["username"]
            password=request.form["password"]

            user_id=users.check_login(username, password)

            if user_id:
                session["user_id"]=user_id
                session["username"]=username
                return redirect("/")
            else:
                return render_template("401.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")