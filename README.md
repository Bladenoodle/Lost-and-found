# Lost and found

# Description
Everyone’s had that moment — you forget something on campus, rush back, and... it’s gone. That’s where Lost and Found comes in!

This app is designed for University of Helsinki students who have lost or found items on any campus. Users can post about missing or discovered items and connect with others to help return belongings to their owners.

With Lost and Found, hopefully no student has to suffer the frustration of permanently losing their stuff at uni!


# Features
* Users can create an account and log into the application.
* Users can add posts about lost or found items.
* Users can edit or delete their own posts.
* Users can add or remove images in their own posts.
* Users can view both their own posts and those made by others.
* Users can search for item posts using keywords, location, and status(found or lost).
* Users can view their own and others' profiles, including post counts and a list of linked posts.
* Users can select categories when creating or editing a post. (Categories include the campus where the item was lost/found and when was the item lost/found.)
* Users can make claim requests on others' posts and view incoming requests on their own posts.
# Installation
- Move to directory lost-and-found:
```
cd lost-and-found
```
- Create python workspace and enter:
```
python3 -m venv venv
```
Linux/MacOS:
```
source venv/bin/activate
```
Windows:
```
source venv/Scripts/activate
```
- Install flask:
```
pip install flask
```
- Create & setup database.db:
```
sqlite3 database.db < init.sql
sqlite3 database.db < schema.sql
```
```
cat > config.py
 > secret_key = (any secret key of your choice e.g. "18fd24bf6a2ad4dac04a33963db1c42f")
```
- run application with:
```
flask run
```
# Application performance test with large data sets

I simulated a large dataset using a [`seed.py`](seed.py) script included in the repository. The test aimed to evaluate how the application performs with a large number of items and whether optimizations were needed.

## Initial test
**Parameters:**
* `user_count = 1000`
* `item_count = 10⁵`
* `message_count = 10⁶`

**Result:**
Index page load time was **over a second**

## Optimizations done:

- added **pagination** on the index page
  
- improved database indexing

## Tests after optimization:

### Test 1
**Parameters:**
* `user_count = 1000`
* `item_count = 10⁵`
* `message_count = 10⁶`

**Result:**
Index page load time was **under 0.1 seconds**
(20 randomly selected pages)

### Test 2
**Parameters:**
* `user_count = 1000`
* `item_count = 10⁶`
* `message_count = 10⁷`

**Result:**
Index page load time was **under 0.1 seconds**
(20 randomly selected pages)
