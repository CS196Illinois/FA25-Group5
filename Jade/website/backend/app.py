from flask import Flask, jsonify, request
from flask_cors import CORS
from api.courses import courses_bp
from api.schedules import schedules_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register blueprints
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(schedules_bp, url_prefix='/api/schedules')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Course Scheduler API is running"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
