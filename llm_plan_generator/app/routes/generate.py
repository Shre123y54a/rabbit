from flask import Blueprint, request, jsonify
from app.services.llama_service import generate_quiz, generate_coding_question
from app.services.evaluate_services import evaluate_quiz
from app.services.llama_service import generate_learning_plan  # ✅ ADD THIS

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-quiz", methods=["POST"])
def generate_quiz_route():
    data = request.get_json()
    topic = data.get("topic")
    result = generate_quiz(topic)
    return jsonify({"questions": result})

@generate_bp.route("/generate-coding", methods=["POST"])
def generate_coding_route():
    data = request.get_json()
    topic = data.get("topic")
    result = generate_coding_question(topic)
    return jsonify({"questions": result})

@generate_bp.route("/evaluate-quiz", methods=["POST"])
def evaluate_quiz_route():
    data = request.get_json()
    result = evaluate_quiz(data)
    return jsonify(result)

@generate_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    goal = data.get("goal")
    deadline = data.get("deadline")
    result = generate_learning_plan(goal, deadline)  # 🔧 This should return the full plan
    return jsonify({"plan": result})
