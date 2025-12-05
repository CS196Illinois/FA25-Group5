#create web server, handling HTTP requests, sending JSON responses
from flask import Flask, request, jsonify
#allow things running on different port to communicate 
from flask_cors import CORS
from scheduler import generate_schedule

app = Flask(__name__)
CORS(app)
'
#just checking if the server is working
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


#get endpoint
@app.route('/search-courses', methods=['GET'])
def search_courses():
    course_name = request.args.get('name', '') #CS124
    department = request.args.get('department', '') #CS
    keyword = request.args.get('keyword', '') #algorithms

    matching courses = [
        {
            #this can be put in another file
        }
    ]


    return jsonify({
        "success": True,
        #"count":  len(matching_courses),
        "courses": matching_courses,
    }), 200 # 200 stands for OK


@app.route('/preferences', methods=['POST'])
def submit_preferences():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "no data can be provided"
        }), 400 #400 is for bad requests

    hard_prefs = data.get("hard_prefernces, {}")
    soft_prefs = data.get("soft_preferences", {})

    #validate those preferences here!!!!1

    #process preferences here!!!!

    return jsonify({
        "success": True,
        "message": "preferences submitted successfully",
        "summary"
    }), 201 #201 is HTTP status code for "created"
