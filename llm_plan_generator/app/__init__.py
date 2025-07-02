from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register Blueprints
    from app.routes.generate import generate_bp
    from app.routes.generate_assessment import generate_assessment_bp

    app.register_blueprint(generate_bp)
    app.register_blueprint(generate_assessment_bp)

    return app
