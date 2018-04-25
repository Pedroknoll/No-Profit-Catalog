#!/usr/bin/python
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, \
    flash, jsonify

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# importing SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from models import (Base, User, Category, Organization, DATABASE)

# app configuration
app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "achaONG Application"

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine(URL(**DATABASE))
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Oauth - Google
# Create anti-forgery state token
# Store it in the session for later validationself.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Sucesso! Você está logado como {}".format(login_session['username']).decode('utf8'))
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Organization Information
@app.route('/organizations/JSON')
def showOrganizationsListJSON():
    organizations = session.query(Organization).all()
    return jsonify(Organizations=[org.serialize for org in organizations])


@app.route('/organization/<int:organization_id>/JSON')
def showOrganizationDetailJSON(organization_id):
    organization = session.query(Organization).\
                        filter_by(id=organization_id).\
                        one()
    return jsonify(Organization=organization.serialize)


# App routes
# Show homepage
@app.route('/')
def index():
  categories = session.query(Category).limit(5).all()
  return render_template('index.html', categories = categories)


# Show organizations list page
@app.route('/organizations')
def showOrganizationsList():
    categories = session.query(Category).all()
    organizations = session.query(Organization).all()
    filter_count = session.query(Organization).count()
    return render_template('organizationsList.html',
                                categories = categories,
                                organizations = organizations,
                                filter_count = filter_count)


# Show all organizations in a specific category
@app.route('/organizations/category/<int:category_id>')
def showCategoryOrganizations(category_id):
    categories = session.query(Category).order_by(Category.name)
    chosen_category = session.query(Category).\
                        filter_by(id=category_id).\
                        one()
    organizations = session.query(Organization).\
                        filter_by(category_id=chosen_category.id)
    filter_count = session.query(Organization).\
                        filter_by(category_id=chosen_category.id).\
                        count()
    return render_template('filterResults.html',
                                categories = categories,
                                chosen_category = chosen_category,
                                organizations = organizations,
                                filter_count = filter_count)


# Show organization detail
@app.route('/organization/<int:organization_id>')
def showOrganizationDetail(organization_id):
    organization = session.query(Organization).\
                        filter_by(id=organization_id).\
                        one()
    category = session.query(Category).\
                    filter_by(id=organization.category_id).\
                    one()
    return render_template('organizationDetail.html',
                                organization = organization,
                                category = category)


# Add organization
@app.route('/organization/new', methods=['GET', 'POST'])
def newOrganization():
    categories = session.query(Category).all()

    if 'username' not in login_session:
        flash("Você precisa estar logado para cadastrar uma Organização".decode('utf8'))
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        addNewOrg = Organization(
                    name = request.form['name'],
                    description = request.form['description'],
                    site = request.form['site'],
                    category_id = request.form['category'],
                    user_id=login_session['user_id'])
        session.add(addNewOrg)
        session.commit()
        flash("Organização criada com sucesso!".decode('utf8'))
        return redirect(url_for('showOrganizationsList'))
    else:
        return render_template('newOrganization.html',
                                    categories = categories)


# Edit organization
@app.route("/organization/<int:organization_id>/edit",
            methods=['GET', 'POST'])
def editOrganization(organization_id):
    categories = session.query(Category).all()
    editedOrganization = session.query(Organization).\
                            filter_by(id=organization_id).\
                            one()

    """Save edited organization to the database"""
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form['name']:
            editedOrganization.name = request.form['name']
        if request.form['site']:
            editedOrganization.site = request.form['site']
        if request.form['description']:
            editedOrganization.description = request.form['description']
        if request.form['category']:
            editedOrganization.category_id = request.form[ 'category']
        session.add(editedOrganization)
        session.commit()
        flash("Organização editada com sucesso!".decode('utf8'))
        return redirect(url_for('showOrganizationDetail',
                                    organization_id=organization_id))
    else:
        return render_template('editOrganization.html',
                                    categories = categories,
                                    organization_id = organization_id,
                                    o = editedOrganization)


# Delete organization
@app.route("/organization/<int:organization_id>/delete",
            methods=['GET', 'POST'])
def deleteOrganization(organization_id):
    organizationToDelete = session.query(Organization).\
                            filter_by(id=organization_id).\
                            one()

    """Delete organization from the database"""
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        session.delete(organizationToDelete)
        session.commit()
        flash("Organização deletada com sucesso!".decode('utf8'))
        return redirect(url_for('showOrganizationsList'))
    else:
        return render_template('deleteOrganization.html',
                                    o = organizationToDelete)


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
