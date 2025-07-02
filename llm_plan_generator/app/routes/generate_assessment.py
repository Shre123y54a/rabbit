from flask import Blueprint, request, jsonify

generate_assessment_bp = Blueprint('generate_assessment', __name__)

@generate_assessment_bp.route('/generate-assessment', methods=['POST'])
def generate_assessment():
    data = request.get_json()
    topic = data.get('topic')
    goal = data.get('goal')
    return jsonify({
        "quizQuestions": [
            {
                "question": f"What is the main concept of {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "Option A"
            }
        ],
        "codingQuestion": f"Write a simple example of {topic} in code."
    })
