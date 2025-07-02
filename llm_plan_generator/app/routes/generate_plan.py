from flask import Blueprint, request, jsonify
from app.services.plan_service import generate_learning_plan

@generate_bp.route("/generate-plan", methods=["POST"])
def generate_plan_route():
    data = request.get_json()
    result = generate_learning_plan(data)
    return jsonify({"plan": result})
