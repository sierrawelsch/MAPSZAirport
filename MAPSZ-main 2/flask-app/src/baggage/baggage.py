from flask import Blueprint, request, jsonify, current_app
from src import db

baggage = Blueprint('baggage', __name__)

# Get all the baggage from the database
@baggage.route('/baggage', methods=['GET'])
def get_baggage():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT baggageID, ticketID, passengerID, bagWeight FROM baggage')
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)

# Get a specific airport from the database
@baggage.route('/baggage/<int:id>', methods=['GET'])
def get_baggage_detail(id):
    query = 'SELECT baggageID, ticketID, passengerID, bagWeight FROM baggage WHERE passengerID = %s'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (id,))
    
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]

    return jsonify(json_data)

# Adds a new baggage
@baggage.route('/baggage', methods=['POST'])
def add_new_baggage():
    the_data = request.json
    current_app.logger.info(the_data)

    passengerID = 1
    ticketID = the_data['ticketID']
    flightID = the_data['flightID']
    weight = the_data['bagWeight']

    query = 'INSERT INTO baggage (passengerID, ticketID, flightID, bagWeight) VALUES (%s, %s, %s, %s)'
    query_values = (passengerID, ticketID, flightID, weight)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, query_values)
    db.get_db().commit()

    return 'Success!'


# Deletes a given baggage
@baggage.route('/baggage', methods=['DELETE'])
def delete_baggage():

    the_data = request.json
    current_app.logger.info(the_data)

    baggage_id = the_data['baggageID']

    query = '''
        DELETE
        FROM baggage
        WHERE baggageID = %s;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (baggage_id,))  # Pass the parameter values as a tuple

    db.get_db().commit()
    return "Successfully deleted baggage #{0}!".format(baggage_id)


# Updates a given baggage
@baggage.route('/baggage', methods=['PUT'])
def update_baggage():
    the_data = request.json

    baggage_id = the_data['baggageID']
    weight = the_data['bagWeight']
    
    current_app.logger.info(the_data)

    the_query = 'UPDATE baggage SET '
    the_query += 'bagWeight = %s '  # Use a parameterized query to prevent SQL injection
    the_query += 'WHERE baggageID = %s;'

    current_app.logger.info(the_query)
    
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (weight, baggage_id))  # Pass the parameter values as a tuple
    db.get_db().commit()

    return "Successfully edited baggage #{0}!".format(baggage_id)
