from flask import *
import mysql.connector
import connect;

connection = None
dbconn = None
app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, \
                                             password=connect.dbpass, host=connect.dbhost, \
                                             database=connect.dbname, autocommit=True, buffered=True)
        dbconn = connection.cursor(dictionary=True)
        return dbconn
    else:
        return dbconn


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def admin():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        return response
    if request.method == 'POST':
        try:
            print(request)
            data = request.get_json()
            print(data)
            query = """INSERT INTO jobs (job_title, company_name, location, job_type, salary_min, salary_max, application_deadline, job_description) VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"""
            values = (data['job_title'], data['company_name'], data['location'], data['job_type'], data['salary_min'], data['salary_max'], data['application_deadline'], data['job_description'])
            # values = (
            #     data.get('job_title'),
            #     data.get('company_name', ''),
            #     data.get('location', ''),
            #     data.get('job_type', ''),
            #     data.get('salary_min', ''),
            #     data.get('salary_max', ''),
            #     data.get('application_deadline', ''),
            #     data.get('job_description','')
            # )
            cur = getCursor()
            print(values)
            cur.execute(query, values)
            cur.execute("select job_title, company_name, location, job_type, salary_min, salary_max, application_deadline,job_description from jobs")
            job = cur.fetchall()
            print(job)
            response = make_response(jsonify({"data":job}))
            return response
        except Exception as e:
            return jsonify({"error": str(e)})
    cur = getCursor()
    cur.execute(
        "select job_title, company_name, location, job_type, salary_min, salary_max, application_deadline,job_description from jobs")
    job = cur.fetchall()
    response = make_response(jsonify({"data":job}))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Or specific origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == "__main__":
    app.run(debug=True)