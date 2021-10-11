import os
import datetime
from re import L, split
from typing import Type
from flask.scaffold import F
import pytz
from cs50 import SQL
from flask import Flask, jsonify, flash, redirect, render_template, request, session, url_for
from PIL import Image
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy.sql.operators import op
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from country_list import countries_for_language

from helpers import apology, login_required, login_required_partner, resizer, lookup, usd

# Configure application
application = Flask(__name__)


# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# UPLOAD_FOLDER = '/final_project_Practice'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure templates are auto-reloaded
application.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Debug setting
application.config['ENV'] = 'development'
application.config['DEBUG'] = True
application.config['TESTING'] = True

# Configure session to use filesystem (instead of signed cookies)
application.config["SESSION_FILE_DIR"] = mkdtemp()
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)


# Stripe Configurations
# application.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51JEeRjSAwK0gy0a7ppnQt6BQUVoSj4Jh3YS37hSLJ8XbgzBSLosQbgsRhGLbeB9J2SA8QQiwGbdpuKglLvZnU1Nt00wzjNZEAu'
# application.config['STRIPE_SECRET_KEY'] = 'sk_test_51JEeRjSAwK0gy0a7OnSgXr0Wq8LkEVdDzY3T4B1Caoc6W0U2f8sOnvBuYy9RaaYgCuEPihFKYE0SBogeAEAb8trE00ODPVquDJ'


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///home.db")


# home page
@application.route("/", methods=["GET", "POST"])
def index():
    titlee = {'n': 'index'}
    details = db.execute("SELECT * FROM locations")

    if session.get("user_id") and isinstance(session.get("user_id"), float):
        user_details = db.execute(
            "SELECT * FROM users WHERE id = ?", session.get("user_id"))
        return render_template('index.html', details=details, titlee=titlee, user_details=user_details)
    else:
        session.clear()
        print('NOT LOG IN')
        return render_template('index.html', details=details, titlee=titlee)


# Shows you the homes of a particular city to explore
@application.route("/explore", methods=["GET", "POST"])
def explore():
    if request.method == "POST":
        city = request.form.get("city")
        typeForm = request.form.get("type")
        locality = db.execute(
            "SELECT DISTINCT locality FROM properties WHERE city = ?", city)
        local_properties = {}
        facade = {}

        lenLocal = len(locality)
        print('Localities:')
        print(locality)

        count = 0
        count1 = 0
        for i in locality:
            local_properties[count] = db.execute(
                f"SELECT * FROM properties JOIN bhk_types ON properties.id = bhk_types.property_id WHERE city = ? AND locality = ?", city, i['locality'])

            for j in local_properties[count]:
                facade[count1] = db.execute(
                    "SELECT facade_small_image FROM facade_images WHERE property_id = ?", j['id'])
                count1 += 1
            count += 1

        bhk_types = {}
        counter = 0
        print('Properties according localities-----')
        for i in range(len(local_properties)):
            for j in range(5):
                bhk_types[counter] = db.execute(
                    "SELECT * FROM bhk_types WHERE property_id = ?", local_properties[i][j]['property_id'])

                counter += 1

        # print(bhk_types[29][0]['property_id'])

        print('BHK TYPES------------')

        types_available = []

        count_types = 0
        for g in range(len(bhk_types)):
            types_checker = []
            for i in bhk_types[g][0].values():
                if i == 'yes':
                    if count_types == 5:
                        types_checker.append('4+ BHK')
                    else:
                        types_checker.append(f'{count_types} BHK')
                count_types += 1
            types_available.append(types_checker)
            count_types = 0

            print('-------------------------')

        for m in types_available[0]:
            print(m)
            print('-----------------------')
        print(len(local_properties))

        titlee = {'n': 'results'}
        cityImg = db.execute(
            "SELECT photo FROM locations WHERE city = ?", city)

        if session.get("user_id") or isinstance(session.get("user_id"), float):
            user_details = db.execute(
                "SELECT * FROM users WHERE id = ?", session.get("user_id"))
            return render_template('explore.html', local_properties=local_properties, facade=facade, cityImg=cityImg[0]['photo'], city=city,
                                   titlee=titlee, user_details=user_details, types_available=types_available)
        else:
            return render_template('explore.html', local_properties=local_properties, facade=facade, cityImg=cityImg[0]['photo'], city=city,
                                   titlee=titlee, types_available=types_available)


# Shows your customized search results
@application.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        city = request.form.get("city")
        typeForm = request.form.get("type")
        locality = db.execute(
            "SELECT DISTINCT locality FROM properties WHERE city = ?", city)
        local_properties = {}
        facade = {}

        lenLocal = len(locality)
        print('Localities:')
        print(locality)

        count = 0
        count1 = 0
        for i in locality:
            local_properties[count] = db.execute(
                f"SELECT * FROM properties JOIN bhk_types ON properties.id = bhk_types.property_id WHERE city = ? AND locality = ? AND {typeForm} = ?", city, i['locality'], 'yes')

            for j in local_properties[count]:
                facade[count1] = db.execute(
                    "SELECT facade_small_image FROM facade_images WHERE property_id = ?", j['id'])
                count1 += 1
            count += 1

        print(city)

        print('FACADE IMAGES------')
        print(facade)

        if typeForm == 'one_BHK':
            typeForm = '1 BHK'
        elif typeForm == 'two_BHK':
            typeForm = '2 BHK'
        elif typeForm == 'three_BHK':
            typeForm = '3 BHK'
        elif typeForm == 'four_BHK':
            typeForm = '4 BHK'
        elif typeForm == 'four_plus_BHK':
            typeForm = '4+ BHK'

        titlee = {'n': 'results'}
        cityImg = db.execute(
            "SELECT photo FROM locations WHERE city = ?", city)

        if session.get("user_id") or isinstance(session.get("user_id"), float):
            user_details = db.execute(
                "SELECT * FROM users WHERE id = ?", session.get("user_id"))
            return render_template('results.html', local_properties=local_properties, facade=facade, cityImg=cityImg[0]['photo'], city=city, typeForm=typeForm,
                                   titlee=titlee, user_details=user_details)
        else:
            return render_template('results.html', local_properties=local_properties, facade=facade, cityImg=cityImg[0]['photo'], city=city, typeForm=typeForm,
                                   titlee=titlee)

        '''
        return render_template('success.html', locality=locality, lenLocal=lenLocal)
        '''


# Shows you your selected homes
@application.route("/homes", methods=["GET", "POST"])
def homes():
    if request.method == "POST":
        name = request.form.get("name")
        h_type = request.form.get("type")
        p_id = request.form.get("p_id")
        details = db.execute(
            "SELECT * FROM properties WHERE id = ?", p_id)
        facade = db.execute(
            "SELECT * FROM facade_images WHERE property_id = ?", p_id)
        interiors = db.execute(
            "SELECT * FROM interiors WHERE property_id = ?", p_id)
        bhk_details = db.execute(
            "SELECT * FROM bhk_details WHERE property_id = ?", p_id)
        features = db.execute(
            "SELECT * FROM features WHERE property_id = ?", p_id)
        nearby = db.execute(
            "SELECT * FROM nearby WHERE property_id = ?", p_id)
        audios = db.execute(
            "SELECT * FROM property_audios WHERE property_id = ?", p_id)

        current_date = datetime.date.today()
        print('CHECKING TYPE---')
        print(h_type)
        print(type(h_type))
        print(p_id)

        price_bhk = ''
        if h_type == "1 BHK":
            price_bhk = 'pricing_one'
        elif h_type == "2 BHK":
            price_bhk = 'pricing_two'
        elif h_type == "3 BHK":
            price_bhk = 'pricing_three'
        elif h_type == "4 BHK":
            price_bhk = 'pricing_four'
        elif h_type == "4+ BHK":
            price_bhk = 'pricing_four_plus'

        print('Property ID---')
        print(p_id)
        print('$$$$$$$$$$$$$')
        titlee = {'n': 'homes'}
        if session.get("user_id") or isinstance(session.get("user_id"), float):
            user_details = db.execute(
                "SELECT * FROM users WHERE id = ?", session.get("user_id"))
            return render_template('homes.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], h_type=h_type, details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, price_bhk=price_bhk, bhk_details=bhk_details, audios=audios,
                                   user_details=user_details)
        else:
            return render_template('homes.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], h_type=h_type, details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, price_bhk=price_bhk, bhk_details=bhk_details, audios=audios)


# Shows you your selected homes
@application.route("/homes_preview", methods=["GET", "POST"])
@login_required_partner
def homes_preview():
    if request.method == "POST":
        name = request.form.get("name")
        p_id = request.form.get("p_id")
        details = db.execute(
            "SELECT * FROM properties WHERE id = ?", p_id)
        facade = db.execute(
            "SELECT * FROM facade_images WHERE property_id = ?", p_id)
        interiors = db.execute(
            "SELECT * FROM interiors WHERE property_id = ?", p_id)
        bhk_details = db.execute(
            "SELECT * FROM bhk_details WHERE property_id = ?", p_id)
        bhk_types = db.execute(
            "SELECT * FROM bhk_types WHERE property_id = ?", p_id)
        features = db.execute(
            "SELECT * FROM features WHERE property_id = ?", p_id)
        nearby = db.execute(
            "SELECT * FROM nearby WHERE property_id = ?", p_id)
        audios = db.execute(
            "SELECT * FROM property_audios WHERE property_id = ?", p_id)

        print('BHK TYPES------------')
        types_available = []
        count_types = 0
        for i in bhk_types[0].values():
            if i == 'yes':
                if count_types == 5:
                    types_available.append('4+BHK')
                else:
                    types_available.append(f'{count_types}BHK')
            count_types += 1

        current_date = datetime.date.today()

        print('Property ID---')
        print(p_id)
        print('$$$$$$$$$$$$$')
        titlee = {'n': 'homes'}
        if session.get("user_id") or isinstance(session.get("user_id"), float):
            user_details = db.execute(
                "SELECT * FROM users WHERE id = ?", session.get("user_id"))
            return render_template('homes_owner.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, bhk_details=bhk_details, audios=audios,
                                   user_details=user_details, types_available=types_available)
        else:
            return render_template('homes_owner.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, bhk_details=bhk_details, audios=audios)


@application.route("/homes_users_preview", methods=["GET", "POST"])
@login_required
def homes_users_preview():
    if request.method == "POST":
        name = request.form.get("name")
        h_type = request.form.get("type")
        p_id = request.form.get("p_id")
        details = db.execute(
            "SELECT * FROM properties WHERE id = ?", p_id)
        facade = db.execute(
            "SELECT * FROM facade_images WHERE property_id = ?", p_id)
        interiors = db.execute(
            "SELECT * FROM interiors WHERE property_id = ?", p_id)
        bhk_details = db.execute(
            "SELECT * FROM bhk_details WHERE property_id = ?", p_id)
        features = db.execute(
            "SELECT * FROM features WHERE property_id = ?", p_id)
        nearby = db.execute(
            "SELECT * FROM nearby WHERE property_id = ?", p_id)
        audios = db.execute(
            "SELECT * FROM property_audios WHERE property_id = ?", p_id)

        current_date = datetime.date.today()

        print('Property ID---')
        print(p_id)
        print('$$$$$$$$$$$$$')
        titlee = {'n': 'homes'}
        if session.get("user_id") or isinstance(session.get("user_id"), float):
            user_details = db.execute(
                "SELECT * FROM users WHERE id = ?", session.get("user_id"))
            return render_template('homes_users.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], h_type=h_type, details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, bhk_details=bhk_details, audios=audios,
                                   user_details=user_details)
        else:
            return render_template('homes_users.html', p_id=p_id, name=name, facade=facade[0]['facade_large_image'], h_type=h_type, details=details, interiors=interiors,
                                   titlee=titlee, current_date=current_date, features=features, nearby=nearby, bhk_details=bhk_details, audios=audios)

# Sign Up for Partners


@application.route("/signUpPartner", methods=["GET", "POST"])
def signUpPartner():

    if request.method == "POST":
        """sign partner up"""

        # Forgets any partner_id
        session.clear()

        first_name = request.form.get('first_name').lower()
        last_name = request.form.get('last_name').lower()
        gender = request.form.get('gender').lower()
        isd = request.form.get('isd')
        mobile = request.form.get('mobile_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        pw_hashed = generate_password_hash(password)

        userNames = db.execute("SELECT phone_number, email_id FROM partners")

        for i in range(len(userNames)):
            if mobile in userNames[i]['phone_number'] or email in userNames[i]['email_id']:
                return apology("USERNAME already exits!", 400)

        partner = db.execute("INSERT INTO partners (first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?)",
                             first_name, last_name, gender, isd, mobile, email, pw_hashed)

        partnerId = db.execute("SELECT id FROM partners WHERE first_name = ? AND last_name = ? AND isd_code = ? AND phone_number = ?",
                               first_name, last_name, isd, mobile)

        folder_name = first_name+'-'+last_name+'-'+str(partnerId[0]['id'])
        createFolderAudio = 'audio_files-'+folder_name

        print('$ CURRENT WORKING DIRECTORY $')
        print(os.getcwd())

        os.chdir(f'static/images/partners')
        print('Changed Directory')

        print(os.getcwd())
        os.makedirs(folder_name)

        os.chdir(f'{folder_name}')

        os.makedirs(f'{createFolderAudio}')

        # Remember which partners has logged in
        session["user_id"] = partnerId[0]['id']

        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        # Redirect partner to dashboard
        return redirect('/partner_dashboard')

    # Partners reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("loginPartner.html")


# Sign Up for Users
@application.route("/signupUsers", methods=["GET", "POST"])
def signupUsers():
    """sign users up"""

    # Forgets any user_id
    session.clear()

    if request.method == "POST":
        first_name = request.form.get('first_name').lower()
        last_name = request.form.get('last_name').lower()
        gender = request.form.get('gender').lower()
        isd = request.form.get('isd')
        mobile = request.form.get('mobile_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        pw_hashed = generate_password_hash(password)

        userNames = db.execute("SELECT phone_number, email_id FROM users")

        for i in range(len(userNames)):
            if mobile in userNames[i]['phone_number'] or email in userNames[i]['email_id']:
                return apology("USERNAME already exits!", 400)

        inquiry = db.execute("SELECT id FROM users")
        if not inquiry:
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              1.0, first_name, last_name, gender, isd, mobile, email, pw_hashed)
        else:
            u_id = inquiry[-1]['id']
            u_id = u_id + 1.0
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              u_id, first_name, last_name, gender, isd, mobile, email, pw_hashed)

        userId = db.execute("SELECT id FROM users WHERE first_name = ? AND last_name = ? AND isd_code = ? AND phone_number = ?",
                            first_name, last_name, isd, mobile)

        # Remember which users has logged in
        session["user_id"] = userId[0]['id']

        # Redirect users to dashboard
        return redirect('/')

    # Partners reached route via GET (as by clicking a link or via redirect)


# Sign Up for Users then redirect for payment
@application.route("/signupUsers_payment", methods=["GET", "POST"])
def signupUsers_payment():
    """sign users up"""

    # Forgets any user_id
    session.clear()

    if request.method == "POST":
        first_name = request.form.get('first_name').lower()
        last_name = request.form.get('last_name').lower()
        gender = request.form.get('gender').lower()
        isd = request.form.get('isd')
        mobile = request.form.get('mobile_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        pw_hashed = generate_password_hash(password)

        userNames = db.execute("SELECT phone_number, email_id FROM users")

        for i in range(len(userNames)):
            if mobile in userNames[i]['phone_number'] or email in userNames[i]['email_id']:
                return apology("USERNAME already exits!", 400)

        inquiry = db.execute("SELECT id FROM users")
        if not inquiry:
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              1.0, first_name, last_name, gender, isd, mobile, email, pw_hashed)
        else:
            u_id = inquiry[-1]['id']
            u_id = u_id + 1.0
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              u_id, first_name, last_name, gender, isd, mobile, email, pw_hashed)

        userId = db.execute("SELECT id FROM users WHERE first_name = ? AND last_name = ? AND isd_code = ? AND phone_number = ?",
                            first_name, last_name, isd, mobile)

        # Remember which users has logged in
        session["user_id"] = userId[0]['id']

        countries = dict(countries_for_language('en'))
        mode = request.form.get('mode')
        h_id = request.form.get('home_id')
        price = request.form.get('price')
        h_type = request.form.get('home_type')
        h_name = request.form.get('home_name')

        u_details = db.execute(
            "SELECT * FROM user_details WHERE u_id = ?", session["user_id"])

        if mode == 'payment':
            print('Payment Pro')
            print('Gentleman Bangaya')
            print('-------------------------------')

            if not u_details:
                print('EMPTY USER_DETAIL TABLE')
                return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                       sessionID=session.get("user_id"))
            else:
                return render_template('payment.html', countries=countries, h_id=h_id, h_type=h_type, price=int(float(price)), h_name=h_name,
                                       sessionID=session.get("user_id"))
        if mode == 'survey':
            survey_dt = datetime.datetime.now()
            surveyDate = request.form.get('surveyDate')
            print('SURVEY DATE-------')
            print(surveyDate)
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            splitDate = surveyDate.split('-')
            month = ''
            for i in range(0, 12):
                if int(splitDate[1]) == int(i + 1):
                    month = months[i]

            survey = f'{splitDate[2]}-{month}-{splitDate[0]}'
            if not u_details:
                print('EMPTY USER_DETAIL TABLE')
                return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                       sessionID=session.get("user_id"), surveyDate=surveyDate, mode=mode)
            else:
                insert_userSurveys = db.execute("INSERT INTO user_surveys (u_id, p_id, p_name, type, price, survey_date_txt, survey_date) VALUES(?,?,?,?,?,?,?)",
                                                session["user_id"], h_id, h_name, h_type, price, survey, survey_dt)
                return render_template('scheduled.html', surveyDate=survey)

        '''
        first_name = request.form.get('first_name').lower()
        last_name = request.form.get('last_name').lower()
        gender = request.form.get('gender').lower()
        isd = request.form.get('isd')
        mobile = request.form.get('mobile_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        pw_hashed = generate_password_hash(password)

        userNames = db.execute("SELECT phone_number, email_id FROM users")

        for i in range(len(userNames)):
            if mobile in userNames[i]['phone_number'] or email in userNames[i]['email_id']:
                return apology("USERNAME already exits!", 400)

        inquiry = db.execute("SELECT id FROM users")
        if not inquiry:
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              1.0, first_name, last_name, gender, isd, mobile, email, pw_hashed)
        else:
            u_id = inquiry[-1]['id']
            u_id = u_id + 1.0
            user = db.execute("INSERT INTO users (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                              u_id, first_name, last_name, gender, isd, mobile, email, pw_hashed)

        userId = db.execute("SELECT id FROM users WHERE first_name = ? AND last_name = ? AND isd_code = ? AND phone_number = ?",
                            first_name, last_name, isd, mobile)

        # Remember which users has logged in
        session["user_id"] = userId[0]['id']

        # Redirect users to dashboard
        return redirect('/purchase_process')
        '''

    # Partners reached route via GET (as by clicking a link or via redirect)


# partner validation
@application.route("/loginPartner", methods=["GET", "POST"])
def loginPartner():
    if request.method == "POST":
        """Log partner in"""

        # Forget any partner_id
        session.clear()

        partner_id = request.form.get('p_id')
        partner_password = request.form.get('p_pw')
        print('$$$$$########$$$$$')
        print(partner_id)
        print(partner_password)
        query = db.execute(
            "SELECT * FROM partners WHERE phone_number = ? OR email_id = ?", partner_id, partner_id)

        print('QUERY LENGTH:')
        print(len(query))

        if len(query) != 1:
            return jsonify("*User id doesn't exist")
        elif not check_password_hash(query[0]['hash'], partner_password):
            return jsonify('*Wrong password')
        else:
            # Remember which partners has logged in
            session["user_id"] = query[0]['id']

            print('Redirecting...')
            return jsonify('correct')


# partner validation
@application.route("/loginUser", methods=["GET", "POST"])
def loginUser():
    if request.method == "POST":
        """Log Users in"""

        # Forget any partner_id
        session.clear()

        user_id = request.form.get('u_id')
        user_password = request.form.get('u_pw')
        print('$$$$$########$$$$$')
        print(user_id)
        print(user_password)
        query = db.execute(
            "SELECT * FROM users WHERE phone_number = ? OR email_id = ?", user_id, user_id)

        print('QUERY LENGTH:')
        print(len(query))

        if len(query) != 1:
            return jsonify("*User id doesn't exist")
        elif not check_password_hash(query[0]['hash'], user_password):
            return jsonify('*Wrong password')
        else:
            # Remember which partners has logged in
            session["user_id"] = query[0]['id']

            print('Redirecting...')
            return jsonify('correct')


# partner logout
@application.route("/logOut_Partner", methods=["GET", "POST"])
def logOut_Partner():
    # Forget any partner_id
    session.clear()
    return redirect('/partner_dashboard')


# user logout
@application.route("/logOut_User", methods=["GET", "POST"])
def logOut_User():
    # Forget any user_id
    session.clear()
    return redirect('/')


# user profile
@application.route("/user_profile", methods=["GET", "POST"])
@login_required
def user_profile():
    titlee = {'n': 'profile'}
    user_details = db.execute(
        "SELECT * FROM users WHERE id = ?", session.get("user_id"))

    user_infos = db.execute(
        "SELECT * FROM user_details WHERE u_id = ?", session.get("user_id"))

    user_homes = db.execute(
        "SELECT * FROM user_homes WHERE u_id = ?", session.get("user_id"))

    home_details = db.execute(
        "SELECT * FROM properties JOIN user_homes ON properties.id = user_homes.p_id WHERE user_homes.u_id = ? ORDER BY user_homes.tenanted_on ASC", session.get("user_id"))

    property_count = db.execute(
        "SELECT COUNT(property_name) FROM properties JOIN user_homes ON properties.id = user_homes.p_id WHERE user_homes.u_id = ?", session.get("user_id"))

    survey_details = db.execute(
        "SELECT * FROM properties JOIN user_surveys ON properties.id = user_surveys.p_id WHERE user_surveys.u_id = ? ORDER BY user_surveys.survey_date ASC", session.get("user_id"))

    survey_count = db.execute(
        "SELECT COUNT(property_name) FROM properties JOIN user_surveys ON properties.id = user_surveys.p_id WHERE user_surveys.u_id = ?", session.get("user_id"))

    print(survey_details)

    colors = ['#6ab04c', '#2980b9', '#f39c12', '#775DD0', '#d35400',
              '#ef476f', '#43aa8b', '#00b4d8', '#e71d36', '#7209b7', '#007f5f', '#e07a5f', '#343a40', '#8ac926', '#db3a34']
    return render_template("user_profile.html", titlee=titlee, user_details=user_details, user_homes=user_homes, home_details=home_details, colors=colors,
                           property_count=property_count[0]['COUNT(property_name)'], survey_count=survey_count[0]['COUNT(property_name)'], user_infos=user_infos, survey_detail=survey_details)


# Partner dashboard
@application.route("/partner_dashboard", methods=["GET", "POST"])
@login_required_partner
def partner_dashboard():
    partner_details = db.execute(
        "SELECT * FROM partners WHERE id = ?", session["user_id"])
    properties = db.execute(
        "SELECT * FROM properties WHERE partner_id = ?", session["user_id"])
    property_count = db.execute(
        "SELECT COUNT(property_name) FROM properties WHERE partner_id = ?", session["user_id"])
    colors = ['#6ab04c', '#2980b9', '#f39c12', '#775DD0', '#d35400',
              '#ef476f', '#43aa8b', '#00b4d8', '#e71d36', '#7209b7', '#007f5f', '#e07a5f', '#343a40', '#8ac926', '#db3a34']

    user_details = db.execute(
        "SELECT DISTINCT * FROM users JOIN user_files ON users.id = user_files.u_id JOIN user_details ON user_files.u_id = user_details.u_id JOIN user_homes ON user_details.u_id = user_homes.u_id JOIN properties ON user_homes.p_id = properties.id WHERE properties.partner_id = ?", session["user_id"])

    tenant_count = db.execute(
        "SELECT DISTINCT COUNT(*) FROM users JOIN user_files ON users.id = user_files.u_id JOIN user_details ON user_files.u_id = user_details.u_id JOIN user_homes ON user_details.u_id = user_homes.u_id JOIN properties ON user_homes.p_id = properties.id WHERE properties.partner_id = ?", session["user_id"])

    survey_details = db.execute(
        "SELECT DISTINCT * FROM users JOIN user_files ON users.id = user_files.u_id JOIN user_details ON user_files.u_id = user_details.u_id JOIN user_surveys ON user_details.u_id = user_surveys.u_id JOIN properties ON user_surveys.p_id = properties.id WHERE properties.partner_id = ?", session["user_id"])

    survey_count = db.execute(
        "SELECT DISTINCT COUNT(*) FROM users JOIN user_files ON users.id = user_files.u_id JOIN user_details ON user_files.u_id = user_details.u_id JOIN user_surveys ON user_details.u_id = user_surveys.u_id JOIN properties ON user_surveys.p_id = properties.id WHERE properties.partner_id = ?", session["user_id"])

    print('TENANTS---')
    print(user_details)

    bhk_types = {}
    bhk_details = {}
    for i in range(len(properties)):
        bhk_types[i] = db.execute(
            "SELECT * FROM bhk_types WHERE property_id IN(SELECT id FROM properties WHERE id = ?)", properties[i]['id'])
        bhk_details[i] = db.execute(
            "SELECT * FROM bhk_details WHERE property_id IN(SELECT id FROM properties WHERE id = ?)", properties[i]['id'])

    '''
    print('------------bhk_types----------------------------')
    print(bhk_types)
    print('------------bhk_details----------------------------')
    print(bhk_details)
    print('------------properties----------------------------')
    print(properties)
    # bhk_types = db.execute("SELECT * FROM bhk_types WHERE id = ?", session["user_id"])
    print(property_count)
    '''

    if partner_details[0]['first_name']:
        first_name = partner_details[0]['first_name']

    if partner_details[0]['last_name']:
        last_name = partner_details[0]['last_name']

    return render_template('dashboard.html', first_name=first_name, last_name=last_name, property_count=property_count[0]['COUNT(property_name)'], survey_details=survey_details,
                           properties=properties, colors=colors, bhk_types=bhk_types, bhk_details=bhk_details, user_details=user_details,
                           tenant_count=tenant_count[0]['COUNT(*)'], survey_count=survey_count[0]['COUNT(*)'])


# Locality suggestion route
@application.route("/searchLocality", methods=["GET", "POST"])
def searchLocality():
    recievedData = request.args.get('q')
    # cityLower = city.lower()

    recievedDataSplit = recievedData.split('$')

    if recievedDataSplit[1]:
        inputValue = recievedDataSplit[0]
        cityName = recievedDataSplit[1].lower()
        locality = db.execute(
            "SELECT DISTINCT locality FROM properties WHERE locality LIKE ? AND city = ? LIMIT 10", inputValue + "%", cityName)
    else:
        inputValue = recievedDataSplit[0]
        locality = db.execute(
            "SELECT DISTINCT locality FROM properties WHERE locality LIKE ? LIMIT 10", inputValue + "%")

    # locality = db.execute("SELECT DISTINCT street FROM buildings WHERE street LIKE ? AND city = ? LIMIT 10", request.args.get('q') + "%", city)
    return jsonify(locality)


@application.route("/localities", methods=["GET", "POST"])
def localities():
    recievedData = request.args.get('q')
    print('$$---CITY---$$:')
    print(recievedData)
    localitiesQuery = db.execute(
        "SELECT DISTINCT locality FROM properties WHERE city = ?", recievedData)
    print('$$---LOCALITIES---$$:')
    print(localitiesQuery)
    return jsonify(localitiesQuery)


# Sign Up for Partners
@application.route("/add_property", methods=["GET", "POST"])
@login_required_partner
def add_property():
    if request.method == "POST":
        building_name = request.form.get('building_name').lower()
        building_age = request.form.get('building_age')
        city = request.form.get('city').lower()
        state = request.form.get('state').lower()
        country = request.form.get('country').lower()
        zip_code = request.form.get('zip')
        locality = request.form.get('locality').lower()
        landmark = request.form.get('landmark').lower()
        neighbourhood = request.form.get('neighbourhood')
        bhkTypes = request.form.getlist('bhkType')
        total_nos = request.form.getlist('total_nos')
        pricingBHK = request.form.getlist('priceBHK')
        homify_categories = request.form.getlist('homify_categories')
        house_number = request.form.get('house_number')

        # Whats nearby?
        malls = request.form.get('malls')
        hospitals = request.form.get('hospitals')
        parks = request.form.get('parks')
        schools = request.form.get('schools')
        colleges = request.form.get('colleges')
        universities = request.form.get('universities')
        pharmacies = request.form.get('pharmacies')
        vegetable_shops = request.form.get('vegetable_shops')
        transportations = request.form.get('transportations')

        # Features-
        parking = request.form.get('parking')
        balcony = request.form.get('balcony')
        geyser = request.form.get('geyser')
        refrigerator = request.form.get('refrigerator')
        sofas = request.form.get('sofas')
        security_guards = request.form.get('security_guards')
        security_cameras = request.form.get('security_cameras')
        basic_furnitures = request.form.get('basic_furnitures')
        attached_bathrooms = request.form.get('attached_bathrooms')
        general_bathroom = request.form.get('general_bathroom')

        bhkTypes_check = [None] * 5
        if bhkTypes:
            for i in range(len(bhkTypes)):
                if bhkTypes[i] == '1_BHK':
                    bhkTypes_check[0] = 'yes'
                elif bhkTypes[i] == '2_BHK':
                    bhkTypes_check[1] = 'yes'
                elif bhkTypes[i] == '3_BHK':
                    bhkTypes_check[2] = 'yes'
                elif bhkTypes[i] == '4_BHK':
                    bhkTypes_check[3] = 'yes'
                elif bhkTypes[i] == '4_PLUS_BHK':
                    bhkTypes_check[4] = 'yes'
                else:
                    bhkTypes_check[i] = 'no'

            for j in range(len(bhkTypes_check)):
                if bhkTypes_check[j] == None:
                    bhkTypes_check[j] = 'no'

        print(homify_categories)
        homify_categories_check = [None] * 8
        if homify_categories:
            for i in range(len(homify_categories)):
                if homify_categories[i] == 'homify standard':
                    homify_categories_check[0] = 'yes'
                elif homify_categories[i] == 'homify go':
                    homify_categories_check[1] = 'yes'
                elif homify_categories[i] == 'homify towers':
                    homify_categories_check[2] = 'yes'
                elif homify_categories[i] == 'homify stay':
                    homify_categories_check[3] = 'yes'
                elif homify_categories[i] == 'homify prime':
                    homify_categories_check[4] = 'yes'
                elif homify_categories[i] == 'homify cloud':
                    homify_categories_check[5] = 'yes'
                elif homify_categories[i] == 'homify suburb':
                    homify_categories_check[6] = 'yes'
                elif homify_categories[i] == 'homify classic':
                    homify_categories_check[7] = 'yes'
                else:
                    homify_categories_check[i] = 'no'

            for j in range(len(homify_categories_check)):
                if homify_categories_check[j] == None:
                    homify_categories_check[j] = 'no'

        if total_nos:
            for i in range(len(total_nos)):
                if total_nos[i] == '':
                    total_nos[i] = 'NULL'

        if pricingBHK:
            for i in range(len(pricingBHK)):
                if pricingBHK[i] == '':
                    pricingBHK[i] = 'NULL'

        # list of acceptable image extentions
        img_extns = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

        # Validates Facade Image
        file = request.files['facade']
        filename = secure_filename(file.filename)

        # Extracting extension name only
        split = filename.rsplit('.')
        extention = split[-1]

        if extention in img_extns:
            print('Valid Image Extention')
        else:
            return apology("Please upload a valid file with jpg, jpeg, png, gif, or bmp extension", 400)

        # Validates interior images
        file_interiors = request.files.getlist('interiors')
        file_interiors_extensions = []
        for i in file_interiors:
            file_interiors_name = secure_filename(i.filename)
            split_ineriors = file_interiors_name.rsplit('.')
            extention_interiors = split_ineriors[-1]
            file_interiors_extensions.append(extention_interiors)

            if extention_interiors in img_extns:
                print('Valid Image Extention')
            else:
                return apology("Please upload valid files", 400)

        # Validates audio Files
        fileDayOpen = request.files['day_time_audio_open']
        fileDayClose = request.files['day_time_audio_close']
        fileNight = request.files['night_time_audio']

        # list of acceptable audio extentions
        audio_extns = ['mp3', 'wav']
        audio_files = [fileDayOpen, fileDayClose, fileNight]
        audio_extensions = []
        # Extracting audio extension name only
        for i in audio_files:
            audio_file_name = secure_filename(i.filename)
            split_audio = audio_file_name.rsplit('.')
            extention_audio = split_audio[-1]
            audio_extensions.append(extention_audio)

            if extention_audio in audio_extns:
                print('Valid Image Extention')
            else:
                return apology("Please upload a valid audio file", 400)

        # Expelling empty objects from the list
        bhkNos = []
        for i in total_nos:
            if i:
                bhkNos.append(i)

        # Expells empty objects from the list
        priceEachBHK = []
        for i in pricingBHK:
            if i:
                priceEachBHK.append(i)

        # Extracting partner id
        partner_details = db.execute(
            "SELECT id, first_name, last_name FROM partners WHERE id = ?", session["user_id"])

        # Inserting into properties table
        properties = db.execute("INSERT INTO properties (partner_id, property_name, property_age, house_number, landmark, neighbourhood, locality, city, state, country, zip_code) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                partner_details[0]['id'], building_name, building_age, house_number, landmark, neighbourhood, locality, city, state, country, zip_code)

        # Extracts property id
        property_id = db.execute("SELECT id FROM properties WHERE property_name = ? AND partner_id = ? AND house_number = ? AND city = ? AND state = ? AND country = ? AND locality = ? AND zip_code = ?",
                                 building_name, partner_details[0]['id'], house_number, city, state, country, locality, zip_code)

        # Inserts into bhk_types table
        bhk_types = db.execute("INSERT INTO bhk_types (property_id, one_BHK, two_BHK, three_BHK, four_BHK, four_PLUS_BHK) VALUES(?,?,?,?,?,?)",
                               property_id[0]['id'], bhkTypes_check[0], bhkTypes_check[1], bhkTypes_check[2], bhkTypes_check[3], bhkTypes_check[4])

        # Inserts into homify_categories table
        homify_categoriesTb = db.execute("INSERT INTO homify_categories (property_id, homify_standard, homify_go, homify_towers, homify_stay, homify_prime, homify_cloud, homify_suburb, homify_classic) VALUES(?,?,?,?,?,?,?,?,?)",
                                         property_id[0]['id'], homify_categories_check[0], homify_categories_check[
                                             1], homify_categories_check[2], homify_categories_check[3], homify_categories_check[4],
                                         homify_categories_check[5], homify_categories_check[6], homify_categories_check[7])

        # Inserts into bhk_details table
        bhk_details = db.execute("INSERT INTO bhk_details (property_id, total_one, pricing_one, total_two, pricing_two, total_three, pricing_three, total_four, pricing_four, total_four_plus, pricing_four_plus) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                 property_id[0]['id'], total_nos[0], pricingBHK[0], total_nos[1], pricingBHK[1], total_nos[2], pricingBHK[2],
                                 total_nos[3], pricingBHK[3], total_nos[4], pricingBHK[4])

        # Inserts into nearby table
        nearby = db.execute("INSERT INTO nearby (property_id, malls, hospitals, parks, schools, colleges, universities, pharmacies, vegetable_shops, transportations) VALUES(?,?,?,?,?,?,?,?,?,?)",
                            property_id[0]['id'], malls, hospitals, parks, schools, colleges, universities, pharmacies, vegetable_shops, transportations)

        # Inserts into features table
        features = db.execute("INSERT INTO features (property_id, parking, balcony, geyser, refrigerator, sofas, security_guards, security_cameras, basic_furnitures, attached_bathrooms, general_bathroom) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                              property_id[0]['id'], parking, balcony, geyser, refrigerator, sofas, security_guards, security_cameras, basic_furnitures, attached_bathrooms, general_bathroom)

        # Handling folders and file paths for images
        building_name_split = building_name.split()
        building_name_dashes = ''

        for i in range(len(building_name_split)):
            building_name_dashes = building_name_dashes + \
                building_name_split[i]
            if not building_name_split[i] == building_name_split[-1]:
                building_name_dashes = building_name_dashes + '_'

        partnerFolder = partner_details[0]['first_name']+'-' + \
            partner_details[0]['last_name']+'-'+str(partner_details[0]['id'])
        audio_file_folder = 'audio_files-'+partnerFolder
        createFolder = building_name_dashes+'-'+str(property_id[0]['id'])
        # Folder path where images will get saved
        saveFilePath = partnerFolder+'/'+createFolder
        # Folder path where audio files will get saved
        saveFileAudioPath = partnerFolder+'/'+audio_file_folder

        print('$ CURRENT WORKING DIRECTORY $')
        print(os.getcwd())

        os.chdir(f'static/images/partners/{partnerFolder}')
        print('Changed Directory')

        # creating folders
        print(os.getcwd())
        os.makedirs(createFolder)

        # Giving homify's customized name and appending the extention
        file_name = createFolder+'.'+extention

        # Saving File to the desired location
        file.save(os.path.join(f'{createFolder}', file_name))

        # Handling interior images
        for i in range(len(file_interiors)):
            # Giving homify's customized name and appending the extention
            file_name1 = createFolder+'-' + \
                f'interior-{i}'+'.'+file_interiors_extensions[i]

            # Saving File to the desired location
            file_interiors[i].save(os.path.join(f'{createFolder}', file_name1))

        # Handling audio files
        for i in range(len(audio_files)):
            # Giving homify's customized name and appending the extention
            file_name2 = createFolder+'-'+f'audio-{i}'+'.'+audio_extensions[i]

            # Saving File to the desired location
            audio_files[i].save(os.path.join(
                f'{audio_file_folder}', file_name2))

        # Changing directory
        os.chdir(f'{createFolder}')

        # Saving images into a list
        img_list = os.listdir()
        print('Image list----')
        print(img_list)

        resized_image_sm = ''
        resized_image_lg = ''

        # Loops the images for resizing and saving
        for i in img_list:
            img_name = i.split('.')
            if i == file_name:
                # Opens the facade image
                image = Image.open(i)

                # Saves a copy of facade image into 640px
                # Calls the resizer function for resizing
                resized_image = resizer(image, 640)
                resized_image_sm = f'{img_name[0]}-sm.{img_name[-1]}'
                resized_image.save(f'{resized_image_sm}')  # Saves the image

                # Saves a copy of facade image into 1280px
                resized_image = resizer(image, 1280)
                resized_image_lg = f'{img_name[0]}-lg.{img_name[-1]}'
                resized_image.save(f'{resized_image_lg}')
                os.remove(f'{i}')
            else:
                # Opens the facade image
                image = Image.open(i)

                # Saves the interior images into 1280px
                resized_image = resizer(image, 1280)
                resized_image.save(f'{i}')

        # Creating image's name with included folder name to save on SQL database
        sql_insertFile_name_sm = saveFilePath+'/'+resized_image_sm
        sql_insertFile_name_lg = saveFilePath+'/'+resized_image_lg

        # Inserts facade image in the facade_images table
        facade_images = db.execute("INSERT INTO facade_images (property_id, facade_large_image, facade_small_image) VALUES(?,?,?)",
                                   property_id[0]['id'], sql_insertFile_name_lg, sql_insertFile_name_sm)

        # Inserts interior images in the interiors table
        for i in range(len(file_interiors)):
            file_name_for_interiors = createFolder+'-' + \
                f'interior-{i}'+'.'+file_interiors_extensions[i]
            sql_insertFile_name1 = saveFilePath+'/'+file_name_for_interiors
            db.execute("INSERT INTO interiors (property_id, interior_images) VALUES(?,?)",
                       property_id[0]['id'], sql_insertFile_name1)

        # Inserts audio files in the property_audios table
        for i in range(len(audio_files)):
            if audio_extensions[i] == 'mp3':
                audio_type = 'mpeg'
            else:
                audio_type = 'wav'
            file_name_for_audios = createFolder+'-' + \
                f'audio-{i}'+'.'+audio_extensions[i]
            sql_insertFile_name2 = saveFileAudioPath+'/'+file_name_for_audios
            db.execute("INSERT INTO property_audios (property_id, audio_file, audio_type) VALUES(?,?,?)",
                       property_id[0]['id'], sql_insertFile_name2, audio_type)

        '''
        return render_template('success.html', building_name=building_name, building_name_dashes=building_name_dashes, city=city, state=state, country=country,
                                zip_code=zip_code, locality=locality, landmark=landmark, neighbourhood = neighbourhood, bhkTypes=bhkTypes,
                                total_nos=total_nos, pricingBHK=pricingBHK, malls=malls, hospitals=hospitals, parks=parks, schools=schools,
                                colleges=colleges, universities=universities, pharmacies=pharmacies, vegetable_shops=vegetable_shops,
                                transportations=transportations, parking=parking, balcony=balcony, geyser=geyser, refrigerator=refrigerator,
                                sofas=sofas, security_guards=security_guards, security_cameras=security_cameras, basic_furnitures=basic_furnitures,
                                attached_bathrooms=attached_bathrooms, general_bathroom=general_bathroom, bhkTypes_check=bhkTypes_check,
                                homify_categories=homify_categories, homify_categories_check=homify_categories_check)

        '''

        os.chdir('..')  # Going back to owner's dir
        os.chdir('..')  # Going back to partners folder
        os.chdir('..')  # Going back to image dir
        os.chdir('..')  # Going back to static dir
        os.chdir('..')  # Going back to Homify dir

        return redirect('/partner_dashboard')
        imgs = db.execute(
            "SELECT * FROM facade_images WHERE property_id = ?", 1)
        inti = db.execute("SELECT * FROM interiors WHERE property_id = ?", 1)

        # return render_template('success.html', imgs=imgs, inti=inti)
    return render_template("add_property_form.html")


@application.route("/purchase_process", methods=["GET", "POST"])
def purchase_process():
    if request.method == "POST":
        countries = dict(countries_for_language('en'))
        h_id = request.form.get('home_id')
        price = request.form.get('price')
        mode = request.form.get('mode')
        h_type = request.form.get('home_type')
        h_name = request.form.get('home_name')
        survey_dt = datetime.datetime.now()

        u_details = db.execute(
            "SELECT * FROM user_details WHERE u_id = ?", session["user_id"])

        if mode == 'survey':
            surveyDate = request.form.get('surveyDate')
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            splitDate = surveyDate.split('-')
            month = ''
            for i in range(0, 12):
                if int(splitDate[1]) == int(i + 1):
                    month = months[i]

            survey = f'{splitDate[2]}-{month}-{splitDate[0]}'

            if not u_details:
                print('EMPTY USER_DETAIL TABLE')
                return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                       sessionID=session.get("user_id"), surveyDate=surveyDate, mode=mode)
            else:
                insert_userSurveys = db.execute("INSERT INTO user_surveys (u_id, p_id, p_name, type, price, survey_date_txt, survey_date) VALUES(?,?,?,?,?,?,?)",
                                                session["user_id"], h_id, h_name, h_type, price, survey, survey_dt)
                return render_template('scheduled.html', surveyDate=survey)

        if not u_details:
            print('EMPTY USER_DETAIL TABLE')
            return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                   sessionID=session.get("user_id"))
        else:
            return render_template('payment.html', countries=countries, h_id=h_id, h_type=h_type, price=int(float(price)), h_name=h_name,
                                   sessionID=session.get("user_id"))

    q = request.args.get('q')
    if q:

        u_details = db.execute(
            "SELECT * FROM user_details WHERE u_id = ?", session["user_id"])

        splitQ = q.split('$')
        print('SPLITING Q----')
        print(splitQ)
        countries = dict(countries_for_language('en'))
        h_id = splitQ[0]
        price = splitQ[1]
        mode = splitQ[2]
        h_type = splitQ[3]
        h_name = splitQ[4]
        survey_dt = datetime.datetime.now()

        if mode == 'survey':
            surveyDate = splitQ[5]
            print('SVDATE 5------')
            print(surveyDate)

            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            splitDate = surveyDate.split('-')
            month = ''
            for i in range(0, 12):
                if int(splitDate[1]) == int(i + 1):
                    month = months[i]
            survey = f'{splitDate[2]}-{month}-{splitDate[0]}'

            if not u_details:
                print('EMPTY USER_DETAIL TABLE')
                return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                       sessionID=session.get("user_id"), surveyDate=surveyDate, mode=mode)
            else:
                insert_userSurveys = db.execute("INSERT INTO user_surveys (u_id, p_id, p_name, type, price, survey_date_txt, survey_date) VALUES(?,?,?,?,?,?,?)",
                                                session["user_id"], h_id, h_name, h_type, price, survey, survey_dt)
                return render_template('scheduled.html', surveyDate=survey)

        if not u_details:
            print('EMPTY USER_DETAIL TABLE')
            return render_template('purchase_process.html', countries=countries, h_id=h_id, h_type=h_type, price=price, h_name=h_name,
                                   sessionID=session.get("user_id"))
        else:
            return render_template('payment.html', countries=countries, h_id=h_id, h_type=h_type, price=int(float(price)), h_name=h_name,
                                   sessionID=session.get("user_id"))


@application.route("/payment_page", methods=["GET", "POST"])
def payment_page():

    if request.method == 'POST':
        countries = dict(countries_for_language('en'))
        h_id = request.form.get('h_id')
        h_name = request.form.get('h_name')
        session_id = request.form.get('session_id')
        h_type = request.form.get('h_type')
        price = int(request.form.get('price'))
        mode = request.form.get('mode')
        selfie = request.files['selfie']
        doc = request.files['doc']
        survey_dt = datetime.datetime.now()

        print(h_name)

        status = request.form.get('status')
        occupation = request.form.get('occupation')
        address = request.form.get('address_line_1')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        users = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"])

        insert_userDeatails = db.execute("INSERT INTO user_details (u_id, status, occupation, address_line, city, state, country) VALUES(?,?,?,?,?,?,?)",
                                         session["user_id"], status, occupation, address, city, state, country)

        print('CHECKING EXTENSIONS')

        # list of acceptable image extentions
        img_extns = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

        print('PULLING FILENAME')

        selfie_name = secure_filename(selfie.filename)
        doc_name = secure_filename(doc.filename)

        print('SPLITING FILENAME')

        # Extracting extension name only
        split0 = selfie_name.rsplit('.')
        split1 = doc_name.rsplit('.')
        selfieExt = split0[-1]
        docExt = split1[-1]

        print('TESTING APOLOGY')

        if selfieExt in img_extns and docExt in img_extns:
            print('Valid Image Extention')
        else:
            return apology("Please upload a valid file with jpg, jpeg, png, gif, or bmp extension", 400)

        os.chdir("static/images/users")

        print('SETTING CUSTOM NAMES')
        str_u_id = str(users[0]['id'])
        # Giving homify's customized name and appending the extention
        cstm_selfie_nm = str_u_id + '-' + users[0]['first_name'] + \
            '_' + users[0]['last_name'] + '-' + 'slf'
        cstm_doc_nm = str_u_id + '-' + users[0]['first_name'] + \
            '_' + users[0]['last_name'] + '-' + 'doc'

        print(os.getcwd())

        print('SAVING FILES')

        #selfie.save(os.path.join(f'selfies/', selfie_name))
        #doc.save(os.path.join(f'docs/', doc_name))

        # Saves a copy of selfie image into 640px
        resized_image_nm = f'{cstm_selfie_nm}.{selfieExt}'
        # Saves the image
        selfie.save(f'selfies/{resized_image_nm}')

        # Saves a copy of document image into 640px
        resized_image_nm1 = f'{cstm_doc_nm}.{docExt}'
        # Saves the image
        doc.save(f'docs/{resized_image_nm1}')

        sql_selfie_nm = f'selfies/{cstm_selfie_nm}.{selfieExt}'

        sql_doc_nm = f'docs/{cstm_doc_nm}.{docExt}'

        insert_userFiles = db.execute("INSERT INTO user_files (u_id, image, document) VALUES(?,?,?)",
                                      session["user_id"], sql_selfie_nm, sql_doc_nm)

        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

        print(os.getcwd())

        print('END OF FILE -- EOF!')

        if mode == 'survey':
            surveyDate = request.form.get('surveyDate')

            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            splitDate = surveyDate.split('-')
            month = ''
            for i in range(0, 12):
                if int(splitDate[1]) == int(i + 1):
                    month = months[i]
            survey = f'{splitDate[2]}-{month}-{splitDate[0]}'

            insert_userSurveys = db.execute("INSERT INTO user_surveys (u_id, p_id, p_name, type, price, survey_date_txt, survey_date) VALUES(?,?,?,?,?,?,?)",
                                            session["user_id"], h_id, h_name, h_type, price, survey, survey_dt)

            return render_template('scheduled.html', surveyDate=survey)

        return render_template('payment.html', countries=countries, price=price, h_type=h_type, h_id=h_id, h_name=h_name)


@application.route("/payment_page_survey", methods=["GET", "POST"])
def payment_page_survey():
    if request.method == "POST":
        countries = dict(countries_for_language('en'))
        u_id = request.form.get('u_id')
        h_id = request.form.get('h_id')
        h_type = request.form.get('h_type')
        h_name = request.form.get('h_name')
        price = int(request.form.get('price'))
        action = request.form.get('action')
        sl_no = request.form.get('sl_no')
        mode = "survey"

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        tenanted_dt = datetime.datetime.now()
        dt_str = str(datetime.date.today())
        dt_split = dt_str.split('-')
        month = ''
        for i in range(0, 12):
            if int(dt_split[1]) == int(i + 1):
                month = months[i]
        tenanted_dt_txt = f'{dt_split[2]}-{month}-{dt_split[0]}'

        if action == 'accept':
            return render_template('payment.html', countries=countries, price=price, h_type=h_type, h_id=h_id, h_name=h_name, mode=mode, sl_no=sl_no)

        if action == 'reject':
            delete_from_survey = db.execute(
                "DELETE FROM user_surveys WHERE sl_no = ? AND u_id = ? AND p_id = ? AND type = ?", sl_no, u_id, h_id, h_type)
            return redirect('/user_profile')

        if action == 'done':
            insert_userHomes = db.execute("INSERT INTO user_homes (u_id, p_id, p_name, type, price, tenanted_on_txt, tenanted_on) VALUES(?,?,?,?,?,?,?)",
                                          u_id, h_id, h_name, h_type, price, tenanted_dt_txt, tenanted_dt)

            delete_from_survey = db.execute(
                "DELETE FROM user_surveys WHERE sl_no = ? AND u_id = ? AND p_id = ? AND type = ?", sl_no, u_id, h_id, h_type)

            return redirect('/partner_dashboard')

        if action == 'cancel':
            delete_from_survey = db.execute(
                "DELETE FROM user_surveys WHERE sl_no = ? AND u_id = ? AND p_id = ? AND type = ?", sl_no, u_id, h_id, h_type)
            return redirect('/partner_dashboard')


@application.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == 'POST':
        card_number = request.form.get('card_num')
        card_exp = request.form.get('card_exp')
        h_id = request.form.get('h_id')
        h_type = request.form.get('h_type')
        h_name = request.form.get('h_name')
        price = request.form.get('price')
        cvc = request.form.get('cvc')
        card_name = request.form.get('card_name')
        sl_no = request.form.get('sl_no')
        mode = request.form.get('mode')
        print('RE-DIRECTING TO THANK YOU PAGE')

        tenanted_dt = datetime.datetime.now()
        dt_str = str(datetime.date.today())
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        dt_split = dt_str.split('-')
        month = ''
        for i in range(0, 12):
            if int(dt_split[1]) == int(i + 1):
                month = months[i]
        tenanted_dt_txt = f'{dt_split[2]}-{month}-{dt_split[0]}'

        print(dt_split)

        if mode:
            insert_userHomes = db.execute("INSERT INTO user_homes (u_id, p_id, p_name, type, price, tenanted_on_txt, tenanted_on) VALUES(?,?,?,?,?,?,?)",
                                          session["user_id"], h_id, h_name, h_type, price, tenanted_dt_txt, tenanted_dt)

            delete_from_survey = db.execute(
                "DELETE FROM user_surveys WHERE sl_no = ? AND u_id = ? AND p_id = ? AND type = ?", sl_no, session["user_id"], h_id, h_type)

            return render_template('thanks.html')

        insert_userHomes = db.execute("INSERT INTO user_homes (u_id, p_id, p_name, type, price, tenanted_on_txt, tenanted_on) VALUES(?,?,?,?,?,?,?)",
                                      session["user_id"], h_id, h_name, h_type, price, tenanted_dt_txt, tenanted_dt)

        return render_template('thanks.html')


@application.route("/footer")
def footer():
    titlee = {'n': 'about me'}
    if session.get("user_id") or isinstance(session.get("user_id"), float):
        user_details = db.execute(
            "SELECT * FROM users WHERE id = ?", session.get("user_id"))
        return render_template('about_me.html', titlee=titlee, user_details=user_details)
    else:
        return render_template('about_me.html', titlee=titlee)


@application.route("/contact")
def contact():
    titlee = {'n': 'about me'}
    if session.get("user_id") or isinstance(session.get("user_id"), float):
        user_details = db.execute(
            "SELECT * FROM users WHERE id = ?", session.get("user_id"))
        return render_template('contact.html', titlee=titlee, user_details=user_details)
    else:
        return render_template('contact.html', titlee=titlee)


@application.route("/about_project")
def about_project():
    titlee = {'n': 'about project'}
    if session.get("user_id") or isinstance(session.get("user_id"), float):
        user_details = db.execute(
            "SELECT * FROM users WHERE id = ?", session.get("user_id"))
        return render_template('about_project.html', titlee=titlee, user_details=user_details)
    else:
        return render_template('about_project.html', titlee=titlee)


if __name__ == '__main__':
    application.run(debug=False, use_debugger=True, use_reloader=True)
