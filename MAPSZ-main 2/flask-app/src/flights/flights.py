from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


flights = Blueprint('flights', __name__)

# Get all the flights from the database
@flights.route('/flights', methods=['GET'])
def get_flights():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT flightID, seatsAvailable, airplaneID, airlineID, departureAirport, ' + 
                   'departureTime, departureTerminal, departureGate, arrivalAirport, arrivalTime, arrivalTerminal, arrivalGate FROM flight')

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

#Get all the flights for a specific airline
@flights.route('/flights/<id>', methods=['GET'])
def get_flight_details (id):

    query = 'SELECT flightID, seatsAvailable, airplaneID, airlineID, departureAirport, departureTime, departureTerminal, departureGate, arrivalAirport, arrivalTime, arrivalTerminal, arrivalGate FROM flight WHERE airlineID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@flights.route('/flights', methods=['POST'])
def add_new_passenger():
    
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    seatsAvailable = the_data['seatsAvailable']
    airplaneID = the_data['airplaneID']
    airlineID = the_data['airlineID']
    departureAirport = the_data['departureAirport']
    departureTime = the_data['departureTime']
    arrivalAirport = the_data['arrivalAirport']
    arrivalTime = the_data['arrivalTime']

    # Constructing the query
    query = 'INSERT INTO flight (seatsAvailable, airplaneID, airlineID, departureAirport, departureTime, arrivalAirport, arrivalTime) VALUES ('
    query += f'"{seatsAvailable}", "{airplaneID}", "{airlineID}", "{departureAirport}", "{departureTime}",  "{arrivalAirport}", "{arrivalTime}")'
    current_app.logger.info(query)

    # Executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'



# Deletes a given drink
# Also reduces the corresponding order's total price
@flights.route('/flights', methods=['DELETE'])
def delete_flight():
    the_data = request.json
    current_app.logger.info(the_data)

    flight_id = the_data['flightID']

    query = '''
        DELETE
        FROM flight
        WHERE flightID = %s;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (flight_id,))  # Pass the parameter value as a tuple

    db.get_db().commit()
    return "Successfully deleted flight #{0}!".format(flight_id)



@flights.route('/flights', methods=['PUT'])
def update_flight():
    the_data = request.json

    flight_id = the_data['flightID']
    departureTime = the_data['departureTime']
    arrivalTime = the_data['arrivalTime']

    current_app.logger.info(the_data)

    the_query = 'UPDATE Flight SET '
    the_query += 'departureTime = %s, '  # Use parameterized queries
    the_query += 'arrivalTime = %s '  # Use parameterized queries
    the_query += 'WHERE flightID = %s;'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query, (departureTime, arrivalTime, flight_id))  # Pass the parameter values as a tuple
    db.get_db().commit()

    return "Successfully edited flight #{0}!".format(flight_id)

