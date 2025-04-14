# Lost and found

* The user can create an account and log into the application.
* The user can add information about found or lost items to the application.
* The user can view both the items they have added and the items added by other users.
* The user can search for item posts with keywords.
* The user can view their own and other user's profiles for the amount of posts they have uploaded and a list of links to the posts.
* The user can select categories while making/editing a post. (categories include the campus where the item is lost/found and the date when it was lost/found.
* The user can make claim requests in other user's posts and view requests on their own posts.

# Installation
- Create python workspace and enter:
    * python3 -m venv venv
    * source venv/bin/activate (if windows: source venv/Scripts/activate)
- Install flask
- Update init.sql:
  * python3 date_generator.py
- Create & setup database.db:
  * sqlite3 database.db < init.sql
  * sqlite3 database.db < schema.sql
  * cat > config.py
     > secret_key = (any secret key of your choice e.g.      "18fd24bf6a2ad4dac04a33963db1c42f")
- run application with:
  * flask run


  
