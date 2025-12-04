#create web server, handling HTTP requests, sending JSON responses
from flask import Flask, request, jsonify
#allow things running on different port to communicate 
from flask_cors import CORS
from scheduler import generate_schedule

app = Flask(__name__)
CORS(app)
'
#just checking if server is working
@app.route('/ping')
def ping():
    return "hello this server is working yeah"

if __name__ == '__main__':
    app.run(debug=True)


#backend api endpoint for frontend to call

#if receives generate request 
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    courses = data.get("courses", [])
    prefs = data.get("preferences", {})

    result = generate_schedule(courses, prefs)

    return jsonify({"schedules": result})
