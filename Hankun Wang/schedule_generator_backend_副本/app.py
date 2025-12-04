from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    try:
        from api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        print("✓ API routes registered successfully")
    except ImportError as e:
        print(f"⚠ Warning: Could not import API routes: {e}")
        print("  The server will start but API endpoints won't be available")
    
    # Root endpoint
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Schedule Generator API',
            'version': '1.0',
            'status': 'running',
            'endpoints': {
                'health': '/health',
                'generate_schedule': '/api/v1/generate-schedule',
                'recommendations': '/api/v1/recommend',
                'search_courses': '/api/v1/courses/search',
                'course_details': '/api/v1/courses/<course_id>'
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'message': 'Server is running'
        }), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Print startup information
    print("\n" + "="*60)
    print("🚀 Schedule Generator Backend Starting...")
    print("="*60)
    print(f"📍 Server URL: http://localhost:{Config.PORT}")
    print(f"📍 Health Check: http://localhost:{Config.PORT}/health")
    print(f"📍 API Base URL: http://localhost:{Config.PORT}/api/v1")
    print("="*60)
    print("\nAvailable Endpoints:")
    print("  POST /api/v1/generate-schedule  - Generate course schedules")
    print("  POST /api/v1/recommend          - Get course recommendations")
    print("  GET  /api/v1/courses/search     - Search courses")
    print("  GET  /api/v1/courses/<id>       - Get course details")
    print("\n" + "="*60)
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run the application
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
