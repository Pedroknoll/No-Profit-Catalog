#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, \
    flash, jsonify

from flask import session as login_session
import random, string
import os, sys

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
from NoProfitCatalog.models import (Base, User, Category, Organization)

# app configuration
app = Flask(__name__)

CLIENT_ID = json.loads(
    open(os.path.join(sys.path[0], "NoProfitCatalog/client_secrets.json"), "r").read())['web']['client_id']
APPLICATION_NAME = "achaONG Application"


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
# Store it in the session for later validationself.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is {}" % login_session['state']
    return render_template('login.html', STATE=state)


# Oauth - Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Parametro invalido.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received {} ".format(access_token))

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token
        exchange we have to split the token first on commas and select
        the first index which gives us the key : value for the server
        access token then we split it on colons to pull out the actual
        token value and replace the remaining quotes with nothing so
        that it can be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token={}&fields=name,id,email'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:{}".format(url)
    # print "API JSON result: {}".format(result)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token={}&redirect=0&height=200&width=200'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += 'Logando..'
    flash("Sucesso! Você está logado como {}" \
            .format(login_session['username']).decode('utf8'))
    print("done!")
    return output

# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/{}/permissions?access_token={}' \
            .format(facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"



# Oauth - Google
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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}' \
            .format(access_token))
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
                                            'connected.'), 200)
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
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += 'Logando..'
    flash("Sucesso! Você está logado como {}" \
        .format(login_session['username']).decode('utf8'))
    print("done!")
    return output


# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}' \
        .format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke'
                                'token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


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
    creator = getUserInfo(organization.user_id)
    category = session.query(Category).\
                    filter_by(id=organization.category_id).\
                    one()
    if ('username' not in login_session
            or creator.id != login_session['user_id']):
        return render_template('organizationDetail.html',
                                    organization = organization,
                                    category = category)
    else:
        return render_template('organizationDetail.html',
                                    organization = organization,
                                    category = category,
                                    logged_and_creator = True)


# Add organization
@app.route('/organization/new', methods=['GET', 'POST'])
def newOrganization():
    if 'username' not in login_session:
        flash("Você precisa estar logado para cadastrar uma Organização" \
            .decode('utf8'))
        return redirect(url_for('showLogin'))
    else:
        categories = session.query(Category).all()
        user = getUserInfo(login_session['user_id'])
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
            return redirect(url_for('showOrganizationDetail',
                                        organization_id=addNewOrg.id))
        else:
            return render_template('newOrganization.html',
                                        categories = categories)


# Edit organization
@app.route("/organization/<int:organization_id>/edit",
            methods=['GET', 'POST'])
def editOrganization(organization_id):
    if 'username' not in login_session:
        flash("Você precisa estar logado para editar uma Organização" \
            .decode('utf8'))
        return redirect(url_for('showLogin'))
    else:
        """Save edited organization to the database"""
        categories = session.query(Category).all()
        editedOrganization = session.query(Organization).\
                                filter_by(id=organization_id).\
                                one()

        if editedOrganization.user_id == login_session['user_id'] and \
            request.method == 'POST':
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
        elif editedOrganization.user_id == login_session['user_id'] :
            return render_template('editOrganization.html',
                                        categories = categories,
                                        organization_id = organization_id,
                                        o = editedOrganization)
        else:
            flash("Você não é o criador desta página e não"
                    "está autorizado à editá-la".decode('utf8'))
            return redirect(url_for('showOrganizationDetail',
                                        organization_id=organization_id))


# Delete organization
@app.route("/organization/<int:organization_id>/delete",
            methods=['GET', 'POST'])
def deleteOrganization(organization_id):
    if 'username' not in login_session:
        flash("Você precisa estar logado para deletar uma Organização" \
            .decode('utf8'))
        return redirect(url_for('showLogin'))
    else:
        """Delete organization from the database"""
        organizationToDelete = session.query(Organization).\
                                filter_by(id=organization_id).\
                                one()
        if organizationToDelete.user_id == login_session['user_id'] and \
            request.method == 'POST':
            session.delete(organizationToDelete)
            session.commit()
            flash("Organização deletada com sucesso!".decode('utf8'))
            return redirect(url_for('showOrganizationsList'))
        elif organizationToDelete.user_id == login_session['user_id']:
            return render_template('deleteOrganization.html',
                                        o = organizationToDelete)
        else:
            flash("Você não é o criador desta página e não"
                    "está autorizado à deletá-la".decode('utf8'))
            return redirect(url_for('showOrganizationDetail',
                                        organization_id=organization_id))


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("Você foi desconectado com sucesso!".decode('utf8'))
        return redirect(url_for('index'))
    else:
        flash("Você não está logado!".decode('utf8'))
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
