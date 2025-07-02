from flask import Blueprint, request, jsonify
from app.services.quiz_service import generate_quiz

generate_quiz_bp = Blueprint("generate_quiz", __name__)

@generate_quiz_bp.route("/generate-quiz", methods=["POST"])
def generate_quiz_route():
    input_data = request.get_json()
    quiz_data = generate_quiz(input_data)
    return jsonify({"quiz": quiz_data})
    
@generate_bp.route("/evaluate-coding", methods=["POST"])
def evaluate_coding_route():
    data = request.get_json()
    questions = data.get("questions")
    user_answers = data.get("answers")

    result = evaluate_coding(questions, user_answers)
    return jsonify(result)
