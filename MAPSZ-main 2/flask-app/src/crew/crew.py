from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


crew = Blueprint('products', __name__)

# Get all the products from the database
@crew.route('/crew', methods=['GET'])
def get_crew():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT employeeID, flightID FROM crew')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@crew.route('/crew/<flightID>', methods=['GET'])
def get_crew_detail (id):

#maybe display all the employees info ideally???
    query = 'SELECT employeeID, flightID FROM crew WHERE flightID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#could cause issue :)
@crew.route('/crew/<employeeID>', methods=['GET'])
def get_flight_detail (id):

#maybe display all the employees info ideally???
    query = 'SELECT flightID FROM crew WHERE employeeID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Adds a new crew member
@crew.route('/crew', methods=['POST'])
def add_new_crew_member():
    # collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variables
    employeeID = the_data['employeeID']
    flightID = the_data['flightID']

    # Constructing the query with parameterized values
    query = 'INSERT INTO crew (employeeID, flightID) VALUES (%s, %s)'
    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (employeeID, flightID))
    db.get_db().commit()

    return 'Success!'
