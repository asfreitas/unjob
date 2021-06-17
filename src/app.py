from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flaskext.mysql import MySQL
import pymysql, json
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random
import datetime
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.secret_key = "9tUPxDo8F8qDzZ7Ogwhg"

mysql = MySQL()

# config mysql

# app.config['MYSQL_DATABASE_USER'] = 'cs361_freitand'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'R3uPvUR1HIHn28tN'
# app.config['MYSQL_DATABASE_DB'] = 'cs361_freitand'
# app.config['MYSQL_DATABASE_HOST'] = 'classmysql.engr.oregonstate.edu'

UPLOAD_FOLDER = './static/user_documents'
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'unjobbed'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql.init_app(app)

@app.route('/')
def index():
    error = None
    logged_in = is_logged_in()

    return render_template('index.html', logged_in=logged_in)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def cache_job_title(tit):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT `job_id` FROM `cache_job_title` WHERE `job_title` = %s", (tit))
        row = cursor.fetchone()
        if row:
            id = row["job_id"]
            return(id)
        else: #insert the title into the table
            sql = "INSERT INTO cache_job_title (job_title) VALUES (%s)"
            data = (tit)
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM cache_job_title WHERE job_title = %s", (tit))
            row = cursor.fetchone()

            if row:
                job_id = row["job_id"]
                return job_id

    except Exception as e:
        error = True
        flash('Cache error')
        print(e)
    finally:
        conn.close()

def cache_location(loc):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT `loc_id` FROM `cache_location` WHERE `location_name` = %s", (loc))
        row = cursor.fetchone()
        if row:
            id = row["loc_id"]
            return(id)
        else: #insert the title into the table
            sql = "INSERT INTO cache_location (location_name) VALUES (%s)"
            data = (loc)
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM cache_location WHERE location_name = %s", (loc))
            row = cursor.fetchone()

            if row:
                loc_id = row["loc_id"]
                return(loc_id)

            return conn.insert_id()

    except Exception as e:
        error = True
        flash('Cache error')
        print(e)
    finally:
        conn.close()

def get_login_id(email):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id FROM `unjobbed_access` WHERE email = %s", (email))
        row = cursor.fetchone()
        if row:
            id = row["id"]
            return(id)
        return 0

    except Exception as e:
        error = True
        flash('Login Id error')
        print(e)
    finally:
        conn.close()

def cache_job_search(job_id, job_loc, log_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT COUNT(*) cnt FROM xref_job_search WHERE id = %s", (log_id))
        row = cursor.fetchone()
        if row:
            num_searches = row["cnt"]

    except Exception as e:
        error = True
        flash('Cache Job Search error')
        print(e)
    finally:
        conn.close()

def login_error_check(email, pwd):
    if(email == ""):
        return "Please fill in an email address"
    if(pwd == ""):
        return "Please fill in a password"

    return "good"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    logged_in = is_logged_in()
    log_id = None

    if request.method == 'POST':
        error = None
        email = request.form['emailaddress']
        pwd = request.form['pword']

        testResults = login_error_check(email, pwd)

        if testResults == "good":
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM unjobbed_access WHERE email = %s", (email))
                row = cursor.fetchone()

                if row:
                    pw = row["password"]
                    pwCheck = check_password_hash(pw, pwd)
                    if (pwCheck):
                        session['logged_in']= True
                        session['email'] = email
                        session['username'] = row['username']
                        profCheck = is_profile_filled_in(email)

                        #check if the dirty flag is set to reset the password
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute("SELECT forgot_login FROM unjobbed_access WHERE email = %s", (email))
                        row2 = cursor.fetchone()
                        if row2:

                            forgot = row2["forgot_login"]

                            if forgot == 1:
                                return redirect(url_for('password_reset'))
                            else:
                                conn = mysql.connect()
                                cursor = conn.cursor(pymysql.cursors.DictCursor)
                                #cursor.execute("SELECT CONCAT(cjt.job_title, \" - \", cl.location_name) AS prevSearch FROM xref_job_search xjs, cache_job_title cjt, cache_location cl WHERE cjt.job_id = xjs.job_id AND xjs.loc_id = cl.loc_id AND xjs.id = %s ORDER BY search_date_time DESC", (log_id))
                                #TopFive = cursor.fetchall()
                                flash('You have successfully logged in.')
                                return redirect(url_for('saved_searches'))
                                #return render_template('saved_searches.html', success=success, error=error, logged_in=logged_in, TopFive=TopFive)

                            session['profile_flag'] = profCheck
                            if (profCheck):
                                success = True
                                logged_in = is_logged_in()

                                email = session['email']
                                log_id = get_login_id(email)
                                return redirect(url_for('saved_searches'))
                            else:
                                warning = True
                                logged_in = is_logged_in()
                                flash('Please finish filling out your profile')
                                return redirect(url_for('profile'))
                                #return render_template('profile.html', error=error, logged_in=logged_in, warning=warning)
                    else:
                        error = True
                        flash('Log in error: You either entered an incorrect email address or password.')
                        return render_template('login.html', success=success, error=error, logged_in=logged_in)

                else:
                    error = True
                    flash('Log in error: You either entered an incorrect email address or password.')
                    return render_template('login.html', success=success, error=error, logged_in=logged_in)
                return render_template('login.html', success=success, error=error, logged_in=logged_in)

            except Exception as e:
                error = True
                flash('Log in error')
                print(e)
            finally:
                    conn.close()
        else:
            error = True
            flash(testResults)
            return render_template('login.html', error=error, logged_in=logged_in)
    else:
        return render_template('login.html', success=success, error=error, logged_in=logged_in)
    return render_template('login.html', success=success, error=error, logged_in=logged_in)

@app.route('/login_js/<string:email>/<string:pwd>/<string:job>/<string:loc>/')
def login_js(email, pwd, job, loc):
    #TODO: redirect to search results
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM unjobbed_access WHERE email = %s", (email))
        row = cursor.fetchone()
        if row:
            pw = row["password"]
            pwCheck = check_password_hash(pw, pwd)
            if (pwCheck):
                success = True
                session['logged_in']= True
                session['email'] = email
                success = True
                error = False
                logged_in = is_logged_in()
                flash('You have successfully logged in.')

                # cache job search
                lclemail = session['email']
                log_id = get_login_id(lclemail)

                save_top_searches(job, loc, log_id)

                #TODO- redirect to search_results

                return redirect(url_for('search_results'))
                #return render_template('search_results.html', success=success, error=error, logged_in=logged_in)
            else:
                print('error loop1')
                error = True
                success = False
                logged_in = is_logged_in()
                flash('Login error')
                return render_template('index.html', success=success, error=error, logged_in=logged_in)
        else:
            print('error loop2')
            error = True
            success = False
            logged_in = is_logged_in()
            flash('Login error')
            return render_template('index.html', success=success, error=error, logged_in=logged_in)
    except Exception as e:
            print('error loop3')
            error = True
            flash('Log in error')
            print(e)
    finally:
            conn.close()
    return render_template('login_js.html')

#this returns True if every field is filled in, False otherwise
def is_profile_filled_in(email):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `user_profile` INNER JOIN unjobbed_access ON `user_profile`.user_id = `unjobbed_access`.id WHERE `unjobbed_access`.`email` = %s", (email))
        row = cursor.fetchone()
        if row:
            profile_id = row["profile_id"]
            fname = row["fname"]
            lname = row["lname"]
            city = row["city"]
            zipcode = row["zipcode"]
            state = row["state"]
            phone = row["phone"]
            address = row["address"]
            is_user_18 = row["is_user_18"]
            pref_comm = row["pref_comm"]
            desired_pay = row["desired_pay"]
            date_to_start = row["date_to_start"]
            reason_for_leaving = row["reason_for_leaving"]
            legally_eligible = row["legally_eligible"]

            if(fname == ""):
                return False
            if(lname == ""):
                return False
            if(city == ""):
                return False
            if(city == ""):
                return False
            if(zipcode == ""):
                return False
            if(state == ""):
                return False
            if(phone == ""):
                return False
            if(address == ""):
                return False
            if(is_user_18 == ""):
                return False
            if(pref_comm == ""):
                return False
            if(desired_pay == ""):
                return False
            if(date_to_start == ""):
                return False
            if(reason_for_leaving == ""):
                return False
            if(legally_eligible == ""):
                return False

            return True
        else:
            return False

    except Exception as e:
        error = True
        flash('Profile read error')
        print(e)
    finally:
        conn.close()

def check_signup(usrnm, email, pwd, cpwd):
    if(usrnm == ""):
        return "Please fill in a username"
    if(email == ""):
        return "Please fill in an email address"
    if(pwd == ""):
        return "Please fill in a password"
    if(cpwd == ""):
        return "Please confirm the password"

    return "good"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    logged_in = is_logged_in()

    if request.method == 'POST':
        email = request.form['emailaddress']
        pwd = request.form['pword']
        cpwd = request.form['confpword']
        usrnm = request.form['username']
        _hashed_password = generate_password_hash(pwd)

        results = check_signup(usrnm, email, pwd, cpwd)

        if results == "good":
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT username FROM unjobbed_access WHERE username = %s", (usrnm))
                user = cursor.fetchone()

                if user:
                    error = True
                    flash('Username is already taken.  Please enter a different Username.')
                    return render_template('signup.html', error=error, logged_in=logged_in)
                else:
                    if (pwd != cpwd):
                        error = True
                        flash('Your passwords do not match')
                        return render_template('signup.html', error=error, logged_in=logged_in)
                    else:
                        #check to see if the user exists already
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute("SELECT * FROM unjobbed_access where email = %s", (email))
                        unj = cursor.fetchall()

                        if unj:
                            error = True
                            flash('Email address is already registered.  Please log in.')
                            return render_template('login.html', error=error, logged_in=logged_in)
                        else:
                            #create the login
                            confStr = randomString(size=8, chars=string.ascii_uppercase + string.digits)

                            sql = "INSERT INTO unjobbed_access (username,email,password,forgot_login,confirmed_login, confirmed_login_string) VALUES (%s,%s, %s, %s, %s, %s)"
                            data = (usrnm, email, _hashed_password, 0, 0, confStr)
                            cursor = conn.cursor()
                            cursor.execute(sql, data)
                            conn.commit()
                            success = True

                            flash('Login created.  Please log in.')
                            return redirect(url_for('login'))
                            #return render_template('login.html', success=success, error=error)
            except Exception as e:
                error = True
                flash('Sign Up error')
                print(e)
            finally:
                conn.close()
        else:
            error = True
            flash(results)
            return render_template('signup.html', error=error, logged_in=logged_in)
    else:
        return render_template('signup.html', error=error, logged_in=logged_in)

# borrowed from: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
def randomString(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    email = None
    success = None
    if request.method == 'POST':
        email = request.form['yourEmail']

        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT count(*) as cnt FROM unjobbed_access WHERE email = %s", (email))
            row = cursor.fetchone()
            if row:
                email_count = row["cnt"]

                if email_count == 1: #send the email
                    success = True
                    flash('A new password will be sent to your email if we have that email address on file.')

                    newPW = randomString(size=8, chars=string.ascii_uppercase + string.digits)
                    print('newPW')
                    print(newPW)
                    _hashed_password = generate_password_hash(newPW)
                    #_hashed_password = generate_password_hash('12345')
                    print(_hashed_password)

                    sql = "UPDATE unjobbed_access SET password = %s, forgot_login = 1 WHERE email = %s"
                    data = (_hashed_password, email)
                    cursor = conn.cursor()
                    cursor.execute(sql, data)
                    conn.commit()

                    msg = 'From: unjobbed@gmail.com\nTo: ' + str(email) + '\nSubject: Password reset\n\n'
                    msg += 'Your new password is: '
                    msg += newPW
                    msg += '\n\nPlease visit UnJobbed.com\login to log into your account'

                    gmail = 'unjobbed@gmail.com'
                    password = 'sC6XsehSTnCKsb3Zcm3S'
                    send_to_email = email
                    subject = 'Password Reset'
                    message = msg

                    msg = MIMEMultipart()
                    msg['From'] = gmail
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    server = smtplib.SMTP('64.233.184.108', 587)
                    server.starttls()
                    server.login(gmail, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()

                    return render_template('forgot_password.html', success=success)

            return render_template('forgot_password.html', success=success)

        except Exception as e:
            error = True
            flash('Cache Job Search error')
            print(e)
        finally:
            conn.close()

        return render_template('forgot_password.html')

    return render_template('forgot_password.html')

def save_top_searches(job_id, loc_id, person_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT count(*) as cnt FROM xref_job_search WHERE `id` = %s", (person_id))
        row = cursor.fetchone()

        if row:
            myCount = row["cnt"]
            curtime = datetime.datetime.now()

            if (myCount == 5):
                #delete the oldest row
                cursor.execute("SELECT js2.* FROM xref_job_search js2 WHERE js2.search_date_time in (SELECT min(js1.search_date_time) FROM xref_job_search js1 WHERE js1.id = %s)", (person_id))
                oldest = cursor.fetchone()

                if oldest:
                    delId = oldest["search_id"]
                    cursor.execute("DELETE FROM xref_job_search WHERE search_id = %s", (delId))
                    conn.commit()

                    #save the new search
                    cursor.execute("INSERT INTO xref_job_search (job_id, loc_id, id, search_date_time) VALUES (%s, %s, %s, %s) ", (job_id, loc_id, person_id, curtime))
                    conn.commit()
            else:
                #save the new search
                cursor.execute("INSERT INTO xref_job_search (job_id, loc_id, id, search_date_time) VALUES (%s, %s, %s, %s) ", (job_id, loc_id, person_id, curtime))
                conn.commit()

    except Exception as e:
        error = True
        flash('Top five search error')
        print(e)
    finally:
        conn.close()

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    error = None
    try:
        logged_in = is_logged_in()
         # user data from form and session
        email = session['email']
        log_id = get_login_id(email)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `user_profile` INNER JOIN unjobbed_access ON `user_profile`.user_id = `unjobbed_access`.id WHERE `unjobbed_access`.id = %s", (log_id))
        has_profile = cursor.fetchone()
        data = has_profile

        if has_profile:
            user_has_profile = True
        else:
            user_has_profile = False
        if logged_in:
            # get username for displaying at profile page
            username = session['username']
        else:
            username = None
        if request.method == "POST":
            # profile information

            fname = request.form['fname']
            lname = request.form['lname']
            city = request.form['city']
            address = request.form['address']
            zipcode = request.form['zip']
            state = request.form['state']
            phone = request.form['phone']

            # example platform questions
            is_user_18 = request.form['is_18']
            pref_comm = request.form['pref_comm']
            desired_pay = request.form['desired_pay']
            date_to_start = request.form['date_to_start']
            reason_for_leaving = request.form['reason_for_leaving']
            legally_eligible = request.form['legally_eligible']
            form_data = (fname, lname, city, address, zipcode, state, phone, is_user_18,
                pref_comm, desired_pay, date_to_start, reason_for_leaving, legally_eligible, log_id)
            if not user_has_profile:
                # insert profile into database and add key to userid
                print ("user does not have a profile")
                query = """INSERT INTO user_profile (fname, lname, city, address, zipcode, state, phone, is_user_18,
                pref_comm, desired_pay, date_to_start, reason_for_leaving, legally_eligible, user_id)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 """
                cursor.execute(query, form_data)
                conn.commit()
                print ("About to render template with no data passed")
                #return render_template('profile.html')
            else:
                print (form_data)
                print ("user has profile")
                query = """ UPDATE user_profile INNER JOIN unjobbed_access ON `user_profile`.user_id = `unjobbed_access`.id
                SET fname = %s, lname = %s, city = %s, address = %s, zipcode = %s,
                state = %s, phone = %s, is_user_18 = %s, pref_comm = %s, desired_pay = %s, date_to_start = %s,
                reason_for_leaving = %s, legally_eligible = %s
                WHERE `unjobbed_access`.id = %s
                """
                cursor.execute(query, form_data)
                conn.commit()
            return redirect(url_for('profile'))

    except Exception as e:
        error = True
        flash('Profile error')
        print(e)
    finally:
        conn.close()
    return render_template('profile.html', logged_in=logged_in, username=username, data=data, has_profile = has_profile)

@app.route('/saved_searches', methods=['GET', 'POST'])
def saved_searches():
    if request.method == 'POST':
        error = None
        success = None
        logged_in = is_logged_in()

        job = request.form['jobTitle']
        loc = request.form['location']
        searchURL = request.form['searchURL']
        jobTitle = job
        location = loc
        print(searchURL)

        if not job:
            error= True
            flash('Please enter a job title.')
            return render_template('saved_searches.html', logged_in=logged_in, error=error)
        elif not loc:
            error= True
            flash('Please enter a location.')
            return render_template('saved_searches.html', logged_in=logged_in, error=error)
        else:
            #cache the job title, if it doesn't exist already
            job_id = cache_job_title(job.title())

            #cache the location if it doesn't exist already
            job_loc = cache_location(loc.title())

            # cache job search
            email = session['email']
            log_id = get_login_id(email)

            save_top_searches(job_id, job_loc, log_id)

            return render_template('search_results.html', logged_in=logged_in, jobTitle=jobTitle, location=location)

        return render_template('saved_searches.html', error=error, logged_in=logged_in)
    else:
        error = None
        logged_in = is_logged_in()

        email = session['email']
        log_id = get_login_id(email)

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT CONCAT(cjt.job_title, \" - \", cl.location_name) AS prevSearch FROM xref_job_search xjs, cache_job_title cjt, cache_location cl WHERE cjt.job_id = xjs.job_id AND xjs.loc_id = cl.loc_id AND xjs.id = %s ORDER BY search_date_time DESC", (log_id))
        #cursor.execute("SELECT CONCAT(\"/search_results/?jobTitle=\", cjt.job_title, \"&location=\", cl.location_name) AS prevSearch FROM xref_job_search xjs, cache_job_title cjt, cache_location cl WHERE cjt.job_id = xjs.job_id AND xjs.loc_id = cl.loc_id AND xjs.id = %s ORDER BY search_date_time DESC", (log_id))
        #cursor.execute("SELECT CONCAT(\"/search_results/?jobTitle=\", REPLACE(cjt.job_title, \' \', \'+\'), \"&location=\", REPLACE(REPLACE(cl.location_name, \' \', \'+\'), \',\',\'%2C\')) AS prevSearch FROM xref_job_search xjs, cache_job_title cjt, cache_location cl WHERE cjt.job_id = xjs.job_id AND xjs.loc_id = cl.loc_id AND xjs.id = %s ORDER BY search_date_time DES", (log_id))
        TopFive = cursor.fetchall()

        return render_template('saved_searches.html', logged_in=logged_in, TopFive=TopFive)
    return render_template('saved_searches.html', logged_in=logged_in)

@app.route('/search_results/')
def search_results():
    error = None
    logged_in = is_logged_in()
    jobTitle = request.args.get('jobTitle')
    location = request.args.get('location')

    return render_template('search_results.html', logged_in=logged_in, jobTitle=jobTitle, location=location)

@app.route('/process_search_results/<string:job>/<string:loc>/', methods=['GET', 'POST'])
def process_search_results(job, loc):
    error = None
    logged_in = is_logged_in()
    return render_template('process_search_results.html', logged_in=logged_in)

# @app.route('/resume')
# def resume():
#     error = None
#     logged_in = is_logged_in()
#     return render_template('resume.html', logged_in=logged_in)
#
#




@app.route('/resume_builder_add', methods=['GET','POST'])
def resume_builder_add():
    error = None
    logged_in = is_logged_in()
    try:
        logged_in = is_logged_in()
         # user data from form and session
        email = session['email']
        log_id = get_login_id(email)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if request.method == "POST":
            # work experience form fields
            employer = request.form['employer']
            job_title = request.form['job_title']
            start_date = request.form['start_date']
            currently_employed = request.form['currently_employed']
            job_desc = request.form['job_desc']
            end_date = request.form['end_date']

            # insert resume item into database referencing user_id
            if currently_employed == "1":
                form_data = (log_id, employer, job_title, currently_employed, job_desc, start_date)
                query = """INSERT INTO unjobbed_resume (user_id, employer, job_title, currently_employed, job_desc, start_date)
                 VALUES (%s,%s,%s,%s,%s,%s)
                 """
                cursor.execute(query, form_data)
            else:
                form_data = (log_id, employer, job_title, currently_employed, job_desc, start_date, end_date)
                query = """INSERT INTO unjobbed_resume (user_id, employer, job_title, currently_employed, job_desc, start_date, end_date)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)
                 """
                cursor.execute(query, form_data)

            conn.commit()
    except Exception as e:
        error = True
        flash('Resume Builder error')
        print(e)
    finally:
        conn.close()
    return redirect(url_for('resume'))


@app.route('/resume_builder_delete', methods=['GET','POST'])
def resume_builder_delete():
    error = None
    logged_in = is_logged_in()
    try:
        resume_item_id = request.form['resume_item_id']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == "POST":
            # insert resume item into database referencing user_id
            query = "DELETE FROM unjobbed_resume WHERE id = %s"
            cursor.execute(query, (resume_item_id))
            conn.commit()

    except Exception as e:
        error = True
        flash('Resume Builder error')
        print(e)
    finally:
        conn.close()
    return render_template('resume_builder.html', logged_in=logged_in)


@app.route('/resume',methods=['GET','POST'])
def resume():
    error = None
    logged_in = is_logged_in()
    try:
         # user data from form and session
        email = session['email']
        log_id = get_login_id(email)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data = ""
        if request.method == "GET":
            form_data = (log_id)
            # insert profile into database and add key to userid
            # query = "SELECT * FROM unjobbed_resume WHERE user_id = %s"
            cursor.execute("SELECT id, job_title, employer, job_desc, currently_employed, DATE_FORMAT(start_date,'%%m/%%d/%%Y') AS start_date, DATE_FORMAT(end_date,'%%m/%%d/%%Y') AS end_date FROM unjobbed_resume WHERE user_id = %s ORDER BY currently_employed DESC, end_date DESC;", (log_id))
            data = cursor.fetchall()
            conn.commit()

            username = session['username']
            uploaded_resume = False
            uploaded_coverletter = False
            for file in os.listdir(UPLOAD_FOLDER):
                if file.find(username) != -1:
                    if file.find('_resume') != -1:
                        uploaded_resume = True
                    if file.find('_coverletter') != -1:
                        uploaded_coverletter = True
                    if uploaded_coverletter and uploaded_resume:
                        break


    except Exception as e:
        error = True
        flash('Resume Builder error')
        print(e)
    finally:
        conn.close()
    return render_template('resume_builder.html', data=data, logged_in=logged_in,  uploaded_resume=uploaded_resume, uploaded_coverletter=uploaded_coverletter)

@app.route('/applications')
def applications():
    error = None
    logged_in = is_logged_in()
    return render_template('applications.html', logged_in=logged_in)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out')
    return redirect(url_for('login'))

@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    error = None
    logged_in = is_logged_in()
    email = session['email']
    print(email)

    if request.method == 'POST':
        oldPw = request.form['currPword']
        newPw = request.form['newPword']
        newPwConf = request.form['confpword']
        print(oldPw)
        print(newPw)
        print(newPwConf)

        #confirm the oldpassword here
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM unjobbed_access WHERE email = %s", (email))
            row = cursor.fetchone()

            if row:
                pw = row["password"]
                pwCheck = check_password_hash(pw, oldPw)
                if (pwCheck):
                    if(newPw != newPwConf):
                        error = True
                        flash('Your passwords do not match')
                        return render_template('password_reset.html', error=error, logged_in=logged_in)
                    else:
                        _hashed_password = generate_password_hash(newPw)
                        print(_hashed_password)
                        conn = mysql.connect()
                        sql = "UPDATE unjobbed_access SET password = %s, forgot_login = 0 WHERE email = %s"
                        data = (_hashed_password, email)
                        cursor = conn.cursor()
                        cursor.execute(sql, data)
                        conn.commit()

                        success = True

                        profCheck = is_profile_filled_in(email)
                        if (profCheck):
                            return redirect(url_for('saved_searches'))
                        else:
                            return redirect(url_for('profile'))
                else:
                    error = True
                    flash('You entered the incorrect current password.')
                    return render_template('password_reset.html', error=error, logged_in=logged_in)

        except Exception as e:
            error = True
            flash('Resume Builder error')
            print(e)
        finally:
            conn.close()
    else:
        flash('Please reset your password')
        warning = True
        return render_template('password_reset.html', logged_in=logged_in, warning=warning)
    return render_template('password_reset.html', logged_in=logged_in)


@app.route('/resume_upload', methods=['GET'])
def resume_upload():
    username = session['username']
    uploaded_resume = False
    uploaded_coverletter = False
    for file in os.listdir(UPLOAD_FOLDER):
        if file.find(username) != -1:
            if file.find('_resume') != -1:
                uploaded_resume = True
            if file.find('_coverletter') != -1:
                uploaded_coverletter = True
            if uploaded_coverletter and uploaded_resume:
                break


    return render_template('resume_upload.html', uploaded_resume=uploaded_resume, uploaded_coverletter=uploaded_coverletter)


# This code was adapted from the official Flask website on file uploads
# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
@app.route('/file_upload', methods=['POST'])
def file_handler():
        username = session['username']

        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('resume'))
        file = request.files['file']
        cl_or_resume = request.form['upload_type']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(url_for('resume'))
        if file and allowed_file(file.filename):
            filename = username
            if cl_or_resume == 'resume':
                filename += '_resume.pdf'
            else:
                filename += '_coverletter.pdf'

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('resume'))
            #redirect to resume builder here


def is_logged_in():
    if session.get('email') is None:
        return False
    return True

if __name__== '__main__':
    app.secret_key='9tUPxDo8F8qDzZ7Ogwhg'
    #app.run(host='0.0.0.0', port=4000)
app.run(debug=True)
