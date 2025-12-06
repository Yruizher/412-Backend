"""
Our Flask router for running the backend and sending out JSON
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DB_HOST = 'localhost'
DB_NAME = 'MovieDB'
DB_USER = 'yahir'
DB_PASSWORD = '123'

"""
What Im using to connect to the postgres database
"""
def connect_to_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, port=8888, user=DB_USER, password=DB_PASSWORD)

@app.route('/data', methods=['POST'])
def data():
    """
    Will return error response is the query is not in valid JSON format
    """

    if not request.is_json:
        return jsonify({'error': 'Query is not in valid JSON format'})

    """
    Debugging purposes
    """
    print("Received JSON:", request.get_json())

    try:
        """
        Grabs the json if its valid, will connect to the postgres database
        """
        json = request.get_json()
        type = json.get('type')
        query1 = json.get('query')
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query1)

        """
        Will check to see if the query is SELECT, then jsonify the appropriate response based on the query
        """
        if type == 'select':
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = [dict(zip(column_names, row)) for row in data]

            cursor.close()
            connection.close()
            return jsonify(result)


        elif type in ('insert', 'update', 'delete'):
            """
            These are the types on admins can use, will send the query to the DB and send out a success response
            """

            connection.commit()
            item = cursor.rowcount
            cursor.close()
            connection.close()
            return jsonify({

                'status': 'Success!',
                'type': type,
                'rows_affected': item
            })

        else:
            return jsonify({'error': 'Query is not a valid type'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)