#!/usr/bin/python
from flask import Flask, render_template, url_for, request, redirect

# importing SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from models import (Base, Category, Organization, DATABASE)

# app configuration
app = Flask(__name__)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine(URL(**DATABASE))
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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

    if request.method == 'POST':
        addNewOrg = Organization(
                    name = request.form['name'],
                    description = request.form['description'],
                    site = request.form['site'],
                    category_id = request.form['category'])
        session.add(addNewOrg)
        session.commit()
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
        return redirect(url_for('showOrganizationDetail',
                                    organization_id=organization_id))
    else:
        return render_template('editOrganization.html',
                                    categories = categories,
                                    organization_id = organization_id,
                                    o = editedOrganization)


# Delete organization
@app.route('/organization/<int:organization_id>/delete')
def deleteOrganization(organization_id):
    return "Delete organization"


if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
