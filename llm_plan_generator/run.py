from flask import Flask
from flask_cors import CORS
from app.routes.generate import generate_bp
from app.routes.generate_assessment import generate_assessment_bp
from app.routes.evaluate_coding import evaluate_coding_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(generate_bp)
app.register_blueprint(generate_assessment_bp)
app.register_blueprint(evaluate_coding_bp)

if __name__ == "__main__":
    app.run(debug=True)
