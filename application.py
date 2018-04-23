#!/usr/bin/python
from flask import Flask

# app configuration
app = Flask(__name__)


# Show homepage
@app.route('/')
def index():
  return 'Hello World'


# Show organizations list page
@app.route('/organizations')
def showOrganizationsList():
    return 'Show all the organizations'


# Show organization detail
@app.route('/organization/<int:organization_id>')
def showOrganizationDetail(organization_id):
    return 'Show organization details'


# Add organization
@app.route('/organization/new')
def addOrganization():
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
