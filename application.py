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
    return 'Show organization details'


# Add organization
@app.route('/organization/new')
def newOrganization():
    return 'Add organization'


# Edit organization
@app.route('/organization/<int:organization_id>/edit')
def editOrganization(organization_id):
    return "Edit organization"


# Delete organization
@app.route('/organization/<int:organization_id>/delete')
def deleteOrganization(organization_id):
    return "Delete organization"


if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
