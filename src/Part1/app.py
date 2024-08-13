import os
import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connection parameters for the PostgreSQL server
SERVER_HOST = os.getenv('DATABASE_HOST', 'localhost')
SERVER_PORT = os.getenv('DATABASE_PORT', '5432')
DB_NAME = os.getenv('DATABASE_NAME', 'user_metrics_db1')
DB_USER = os.getenv('DATABASE_USER', 'myuser')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'mypassword')

def database_exists(conn, db_name):
    """Check if the database already exists."""
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
    exists = cur.fetchone()
    cur.close()
    return exists is not None

def create_database(conn, db_name):
    """Create the database if it does not exist."""
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    cur.close()
    conn.commit()
    print(f"Database {db_name} created successfully!")

def execute_sql_from_file(filename, conn):
    """ Execute SQL statements from a file """
    cur = conn.cursor()
    with open(filename, 'r') as sql_file:
        sql_commands = sql_file.read()
        cur.execute(sql_commands)
    cur.close()
    conn.commit()
    print("SQL file executed successfully!")

def init_db():
    """Initialize the database and create necessary tables."""
    conn = None  # Initialize conn to None

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=SERVER_HOST,
            port=SERVER_PORT,
            database="postgres",  # Connect to the default 'postgres' database
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True

        # Check if the database exists
        if not database_exists(conn, DB_NAME):
            # If not, create it
            create_database(conn, DB_NAME)
        else:
            print(f"Database {DB_NAME} already exists. Skipping creation.")
        
        # Now connect to the newly created database (or existing one)
        conn.close()
        conn = psycopg2.connect(
            host=SERVER_HOST,
            port=SERVER_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # Execute SQL commands from the file to create tables
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init.sql')

        execute_sql_from_file(sql_file_path, conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

# Call the init_db function when the Flask app starts
init_db()

@app.route('/')
def index():
    return "Welcome to the Flask app with database initialization!"

@app.route('/data', methods=['POST'])
def ingest_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=SERVER_HOST,
            port=SERVER_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        user_id = data.get('user_id')
        user_name = data.get('name')
        user_email = data.get('email')

        # Ensure the user_id exists in the users table
        cur.execute("SELECT user_id, name, email FROM users WHERE user_id = %s", (user_id,))
        user_record = cur.fetchone()

        if user_record:
            existing_name, existing_email = user_record[1], user_record[2]
            if existing_name != user_name or existing_email != user_email:
                return jsonify({
                    "status": "error",
                    "message": "user_id already exists but with different name or email"
                }), 400
        else:
            # If the user does not exist, insert it into the users table
            insert_user_query = """
                INSERT INTO users (user_id, name, email)
                VALUES (%s, %s, %s)
            """
            cur.execute(insert_user_query, (
                user_id,
                user_name,
                user_email
            ))

        # Check if the session_id exists in the sessions table
        cur.execute("SELECT session_id FROM sessions WHERE session_id = %s", (data['session_id'],))
        session_exists = cur.fetchone()

        if not session_exists:
            # If the session does not exist, insert it into the sessions table
            insert_session_query = """
                INSERT INTO sessions (session_id, user_id, device_id, platform, location, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s))
            """
            cur.execute(insert_session_query, (
                data['session_id'],
                user_id,
                'device_1',  # Modify these values as needed
                'platform_1',
                'location_1',
                data['timestamp'],
                data['timestamp']  # Assuming start_time and end_time are the same for simplicity
            ))

        # Convert talked_time to an interval
        talked_time_interval = f"{data['talked_time']} seconds"

        # Insert data into the user_metrics table
        insert_metrics_query = """
            INSERT INTO user_metrics (session_id, talked_time, microphone_used, speaker_used, voice_sentiment, timestamp)
            VALUES (%s, %s::interval, %s, %s, %s, to_timestamp(%s))
        """
        cur.execute(insert_metrics_query, (
            data['session_id'],
            talked_time_interval,
            data['microphone_used'],
            data['speaker_used'],
            data['voice_sentiment'],
            data['timestamp']  # Assuming this is Unix time
        ))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
