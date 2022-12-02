from flask import render_template, request, redirect, session
from app import app, db
from app.models import Reviews
from utils import get_DB

jobsDB  = None
usersDb = None
db = None

def intializeDB():
    global jobsDB, db, usersDb
    db = get_DB()
    usersDb = db.Users
    jobsDB = db.Jobs

def process_jobs(job_list):
    processed = list()
    for job in job_list:
        job['id'] = job.pop('_id')
        processed.append(job)
    return processed

def get_all_jobs():
    all_jobs = list(jobsDB.find())
    return process_jobs(all_jobs)



def get_my_jobs(username):
    intializeDB()
    user = usersDb.find_one({"username": username})
    if user == None:
        pass

    reviews = user['reviews']
    return process_jobs(jobsDB.find({"_id": {'$in': reviews}}))

#create job review
@app.route('/review')
def review():
    """
    An API for the user review page, which helps the user to add reviews
    """
    intializeDB()
    if not ('username' in session.keys() and session['username']):
        return redirect("/")
    entries = get_all_jobs()
    return render_template('review-page.html', entries=entries)


#view all
@app.route('/pageContent')
def page_content():
    """An API for the user to view all the reviews entered"""
    intializeDB()
    entries = get_all_jobs()
    return render_template('page_content.html', entries=entries)


#view all
@app.route('/myjobs')
def myjobs():
    """An API for the user to view all the reviews created by them"""
    intializeDB()
    entries = get_my_jobs(session['username'])
    return render_template('myjobs.html', entries=entries)

#search
@app.route('/pageContentPost', methods=['POST'])
def page_content_post():
    """An API for the user to view specific reviews depending on the job title"""
    intializeDB()
    if request.method == 'POST':
        form = request.form
        search_title = form.get('search')
        if search_title.strip() == '':
            entries = get_all_jobs()
        else:
            entries = process_jobs(jobsDB.find({"job_title": "/"+search_title+"/"}))
        return render_template('page_content.html', entries=entries)

@app.route('/')
@app.route('/home')

def home():
    """An API for the user to be able to access the homepage through the navbar"""
    intializeDB()
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    """An API to help users add their reviews and store it in the database"""

    intializeDB()
    user = usersDb.find_one({"username": session['username']})
    if user == None:
        pass
    reviews = user['reviews']

    if request.method == 'POST':
        form = request.form

        job = {
            "_id": form.get('job_title') + "_" + form.get('company') + "_" + form.get('locations'),
                "title": form.get('job_title'),
                "company": form.get('company'),
                "description": form.get('job_description'),
                "locations": form.get('locations'),
                "department": form.get('department'),
                "hourly_pay":   form.get('hourly_pay'),
                "benefits": form.get('benefits'),
                "review": form.get('review'),
                "rating": form.get('rating'),
                "recommendation": form.get('recommendation'),
                "author": session['username']
            }

        if jobsDB.find_one({'_id': job['_id']})== None:
            jobsDB.insert_one(job)
            reviews.append(job['_id'])
            usersDb.update_one({"username": session['username']}, {"$set": {"reviews": reviews}})

    return redirect('/')

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect('/')

@app.route("/login", methods=["POST", "GET"])
def login():

    intializeDB()
    if 'username' in session.keys() and session['username']:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        user = usersDb.find_one({"username": username})
        passw =  request.form.get("password")

        if user and user["password"] == passw:
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/")

    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():

    intializeDB()
    if 'username' in session.keys() and session['username']:
        print("User ", session['username']," already logged in")
        return redirect("/")
        
    if request.method == "POST":
        username = request.form.get("username")
        user = usersDb.find_one({"username": username})
        passw =  request.form.get("password")

        #new user
        if not user:
            user = {
                "username": username,
                "password": passw,
                "reviews": list()
            }
            usersDb.insert_one(user)
            
        session["username"] = username
        return redirect("/")

    return render_template("signup.html")

# @app.route('/update/<int:id>')
# def updateRoute(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             return render_template('update.html', entry=entry)
#
#
# @app.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             form = request.form
#             title = form.get('job_title')
#             description = form.get('job_description')
#             department = form.get('department')
#             locations = form.get('locations')
#             hourly_pay = form.get('hourly_pay')
#             benefits = form.get('benefits')
#             review = form.get('review')
#             rating = form.get('rating')
#             entry.title = title
#             entry.description = description
#             entry.department = department
#             entry.locations = locations
#             entry.hourly_pay = hourly_pay
#             entry.benefits = benefits
#             entry.review = review
#             entry.rating = rating
#             db.session.commit()
#         return redirect('/')
#
#
# @app.route('/delete/<int:id>')
# def delete(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             db.session.delete(entry)
#             db.session.commit()
#         return redirect('/')
