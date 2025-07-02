from flask import Blueprint, request, jsonify
from app.services.llama_service import evaluate_coding

evaluate_coding_bp = Blueprint("evaluate_coding", __name__)

@evaluate_coding_bp.route("/evaluate-coding", methods=["POST"])
def evaluate_coding_route():
    data = request.get_json()
    questions = data.get("questions")
    answers = data.get("answers")

    if not questions or not answers:
        return jsonify({"error": "Missing questions or answers"}), 400

    result = evaluate_coding(questions, answers)
    return jsonify(result)
