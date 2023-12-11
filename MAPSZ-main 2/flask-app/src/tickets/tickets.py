from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


tickets = Blueprint('ticket', __name__)

# Get all the products from the database
@tickets.route('/tickets', methods=['GET'])
def get_products():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT ticketID, flightID, seatNum, class, price, boardingGroup, passengerID FROM ticket')

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

# Get all the tickets of a specific passenger from the database
@tickets.route('/tickets/<id>', methods=['GET'])
def get_ticket_detail (id):

    query = 'SELECT ticketID, flightID, seatNum, class, price, boardingGroup, passengerID FROM ticket WHERE passengerID = 1' 
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


# Adds a new ticket
@tickets.route('/tickets', methods=['POST'])
def add_new_ticket():

    # collecting data from the request object
    # Flask gets the request object and .json converts it to a json
    the_data = request.json
    # current_app import gives the logger object that logs all the data in the console
    current_app.logger.info(the_data)

    # extracting the variable
    flightID = the_data.get('flightID')
    seatNum = the_data.get('seatNum')
    classType = the_data.get('class')
    price = the_data.get('price')
    boardingGroup = the_data.get('boardingGroup')
    passengerID = the_data.get('passengerID')

    # Constructing the query
    query = f'INSERT INTO ticket (flightID, seatNum, class, price, boardingGroup, passengerID) VALUES ("{flightID}", "{seatNum}", "{classType}", "{price}", "{boardingGroup}", "{passengerID}")'
    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success!'


# Deletes a given ticket
# Deletes all baggage that contain that ticket as well
@tickets.route('/tickets', methods=['DELETE'])
def delete_ticket():
    the_data = request.json
    current_app.logger.info(the_data)

    ticket_id = the_data['ticketID']
    
    query = '''
        DELETE
        FROM ticket
        WHERE ticketID = %s;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (ticket_id,))

    db.get_db().commit()
    return "Successfully deleted ticket #{0}!".format(ticket_id)


# updates a given ticket
@tickets.route('/ticket/<ticketID>', methods=['PUT'])
def update_ticket(ticketID):
    the_data = request.json

#   ticketID INT AUTO_INCREMENT NOT NULL,
#   flightID INT,
#   seatNum VARCHAR(10),
#   class VARCHAR(20),
#   price DECIMAL(10, 2),
#   boardingGroup CHAR(1),
#   passengerID INT,

    ticketID = the_data['ticketID']
    flightID = the_data['flightID']
    seatNum = the_data['seatNum']
    classType = the_data['class']
    boardingGroup = the_data['boardingGroup']
    passengerID = the_data['passengerID']
    
    current_app.logger.info(the_data)

    the_query = 'UPDATE ticket SET '
    the_query += 'boardingGroup = "' + str(boardingGroup) + '", '
    the_query += 'passengerID = "' + str(passengerID) + '", '
    the_query += 'flightID = "' + str(flightID) + '", '
    the_query += 'seatNum = "' + str(seatNum) + '", '
    the_query += 'class = ' + str(classType) + ' '
    the_query += 'WHERE ticketID = {0};'.format(ticketID)

    current_app.logger.info(the_query)
    
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully editted ticket #{0}!".format(ticketID)