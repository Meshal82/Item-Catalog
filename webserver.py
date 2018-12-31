#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from flask import session as login_session
from flask import make_response

# importing SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import *
import random
import string
import httplib2
import json
import requests

# importing oauth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

# importing adding icon

import os
from flask import send_from_directory
# app configuration

app = Flask(__name__)

APPLICATION_NAME = 'catolog-items'

# google client secret
secret_file = json.loads(open('client_secrets.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

engine = create_engine('sqlite:///cars.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# checking if the user exisit in the database

def check_user():
    try:
        email = login_session['email']
        return session.query(User).filter_by(email=email).one()
    except Exception:
        return None


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


def new_state():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return state


# main page
@app.route('/')
@app.route('/cars/')
def showCars():
    cars = session.query(Car).all()
    state = new_state()
    return render_template('main.html', cars=cars, currentPage='main',
                           state=state, login_session=login_session)


# To add new car
@app.route('/car/new/', methods=['GET', 'POST'])
def newCar():
    if request.method == 'POST':

        # check if user is logged in or not
        if 'provider' in login_session and \
                    login_session['provider'] != 'null':
            name = request.form['name']
            picture = request.form['carImage']
            description = request.form['carDescription']
            description = description.replace('\n', '<br>')
            carCategory = request.form['category']
            user_id = check_user().id

            if name and picture and description \
                    and carCategory:
                newCar = Car(
                    name=name,
                    picture=picture,
                    description=description,
                    category=carCategory,
                    user_id=user_id,
                    )
                session.add(newCar)
                session.commit()
                return redirect(url_for('showCars'))
            else:
                state = new_state()
                return render_template(
                    'newCar.html',
                    currentPage='new',
                    title='Add New Car',
                    errorMsg='All Fields are Required!',
                    state=state,
                    login_session=login_session,
                    )
        else:
            state = new_state()
            cars = session.query(Car).all()
            return render_template(
                'main.html',
                cars=cars,
                currentPage='main',
                state=state,
                login_session=login_session,
                errorMsg='Please Login first to Add a car!',
                )
    elif 'provider' in login_session and login_session['provider'] \
            != 'null':
        state = new_state()
        return render_template('newCar.html', currentPage='new',
                               title='Add New Car', state=state,
                               login_session=login_session)
    else:
        state = new_state()
        cars = session.query(Car).all()
        return render_template(
            'main.html',
            cars=cars,
            currentPage='main',
            state=state,
            login_session=login_session,
            errorMsg='Please Login first to Add a car!',
            )


# To show a car of different category
@app.route('/cars/category/<string:category>/')
def sortCars(category):
    cars = session.query(Car).filter_by(category=category).all()
    state = new_state()
    return render_template(
        'main.html',
        cars=cars,
        currentPage='main',
        error='Sorry No Cars in Database on this category ',
        state=state,
        login_session=login_session)


# To show car detail
@app.route('/cars/category/<string:category>/<int:carId>/')
def carDetail(category, carId):
    car = session.query(Car).filter_by(id=carId, category=category).first()
    state = new_state()
    if car:
        return render_template('carDetail.html', car=car,
                               currentPage='detail', state=state,
                               login_session=login_session)
    else:
        return render_template('main.html', currentPage='main',
                               error="""No Car Found with this Category
                                """,
                               state=state,
                               login_session=login_session)


# To edit car detail
@app.route('/cars/category/<string:category>/<int:carId>/edit/',
           methods=['GET', 'POST'])
def editCarDetails(category, carId):
    car = session.query(Car).filter_by(id=carId, category=category).first()
    if request.method == 'POST':

        # check if user is logged in or not

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            name = request.form['name']
            picture = request.form['carImage']
            description = request.form['carDescription']
            carCategory = request.form['category']
            user_id = check_user().id
            

            # check if the car owner is same as logged in user

            if car.user_id == user_id:
                if name and picture and description \
                        and carCategory:
                    car.name = name
                    car.picture = picture
                    description = description.replace('\n', '<br>')
                    car.description = description
                    car.category = carCategory
                    session.add(car)
                    session.commit()
                    return redirect(url_for('carDetail',
                                    category=car.category,
                                    carId=car.id))
                else:
                    state = new_state()
                    return render_template(
                        'editCar.html',
                        currentPage='edit',
                        title='Edit car Details',
                        car=car,
                        state=state,
                        login_session=login_session,
                        errorMsg='All Fields are Required',
                        )
            else:
                state = new_state()
                return render_template(
                    'carDetail.html',
                    car=car,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry, The Owner can only edit car Details!')
        else:
            state = new_state()
            return render_template(
                'carDetail.html',
                car=car,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Edit the car Details!',
                )
    elif car:
        state = new_state()
        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            if user_id == car.user_id:
                car.description = car.description.replace('<br>', '\n')
                return render_template(
                    'editCar.html',
                    currentPage='edit',
                    title='Edit car Details',
                    car=car,
                    state=state,
                    login_session=login_session,
                    )
            else:
                return render_template(
                    'carDetail.html',
                    car=car,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry The Owner can only edit car Details!')
        else:
            return render_template(
                'carDetail.html',
                car=car,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Edit the car Details!',
                )
    else:
        state = new_state()
        return render_template('main.html', currentPage='main',
                               error="""Error Editing the car, No car Found
                               with this Category """,
                               state=state,
                               login_session=login_session)


# To delete cars
@app.route('/cars/category/<string:category>/<int:carId>/delete/')
def deleteCar(category, carId):
    car = session.query(Car).filter_by(category=category, id=carId).first()
    state = new_state()
    if car:

        # check if user is logged in or not

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            if user_id == car.user_id:
                session.delete(car)
                session.commit()
                return redirect(url_for('showCars'))
            else:
                return render_template(
                    'carDetail.html',
                    car=car,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry ,Only the Owner Can delete the car'
                    )
        else:
            return render_template(
                'carDetail.html',
                car=car,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Delete the car',
                )
    else:
        return render_template('main.html', currentPage='main',
                               error="""Error Deleting the car ! No car Found
                               with this Category """,
                               state=state,
                               login_session=login_session)


# JSON Endpoints
@app.route('/cars.json/')
def carsJSON():
    cars = session.query(Car).all()
    return jsonify(Cars=[car.serialize for car in cars])


@app.route('/cars/category/<string:category>.json/')
def carCategoryJSON(category):
    cars = session.query(Car).filter_by(category=category).all()
    return jsonify(Cars=[car.serialize for car in cars])


@app.route('/cars/category/<string:category>/<int:carId>.json/')
def carJSON(category, carId):
    car = session.query(Car).filter_by(category=category, id=carId).first()
    return jsonify(Car=car.serialize)


# google signin function

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
        authorisation code"""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = access_token
    login_session['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    login_session['name'] = data['name']
    login_session['img'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    if not check_user():
        newUser = User(
            name=data['name'], email=data['email'], picture=data['picture'])
        session.add(newUser)
        session.commit()
    return jsonify(name=login_session['name'],
                   email=login_session['email'],
                   img=login_session['img'])


# logout user
@app.route('/logout', methods=['post'])
def logout():

    return gdisconnect()


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']

    # Only disconnect a connected user.

    if access_token is None:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.

        del login_session['credentials']
        del login_session['id']
        del login_session['name']
        del login_session['email']
        del login_session['img']
        login_session['provider'] = 'null'
        response = make_response(json.dumps({'state': 'loggedOut'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # if given token is invalid, unable to revoke token

        response = make_response(json.dumps({'state': 'errorRevoke'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret'
    app.run(host='0.0.0.0', port=8000)
