#create web server, handling HTTP requests, sending JSON responses
from flask import Flask, request, jsonify
#allow things running on different port to communicate 
from flask_cors import CORS
from scheduler import generate_schedule

app = Flask(__name__)
CORS(app)

#just checking if the server is working
@app.route('/ping')
def ping():
    return "hello this server is working yeah"

if __name__ == '__main__':
    app.run(debug=True)


#backend api endpoint for frontend to call



#get endpoint
@app.route('/search-courses/', methods=['GET'])
def search_courses():

    #here extract department name using spilt 
    course_name = request.args.get('name', '') #CS124
    department = request.args.get('department', '') #CS


    matching courses = [
        {
            #ALGO NEEDED
        }
    ]


    return jsonify({
        "success": True,
        #"count":  len(matching_courses),
        "courses": matching_courses,
    }), 200 # 200 stands for OK


    
@app.route('/preferences', methods=['POST'])
def generate():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "no data can be provided"
        }), 400 #400 is for bad requests

    
    course_list = data.get("course_list")
    CRN_list = data.get("CRN_list")
    hard_breaks = data.get("hard_breaks")
    soft_preferences = data.get("soft_preferences")
    
    top_ten_schedules = generate_schedule(course_list, CRN_list, hard_breaks, soft_preferences)

    return jsonify({
        "success": True,
        "schedules": top_ten_schedules
    }), 201 #201 is HTTP status code for "created"
