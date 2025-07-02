"use client";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { format } from "date-fns";

export default function Home() {
  const [goal, setGoal] = useState("");
  const [deadline, setDeadline] = useState(null);
  const [notification, setNotification] = useState("");
  const [plan, setPlan] = useState([]);
  const [activeAssessmentIndex, setActiveAssessmentIndex] = useState(null);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [codingQuestions, setCodingQuestions] = useState([]);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [codingAnswers, setCodingAnswers] = useState({});
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [codingResult, setCodingResult] = useState(null);
  const [unlockedIndex, setUnlockedIndex] = useState(0);

  const generatePlan = async () => {
    if (!goal || !deadline) {
      setNotification("Please enter both a goal and a deadline.");
      return;
    }
    setNotification("Generating learning plan...");
    const response = await fetch("http://localhost:5000/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        goal,
        deadline: deadline.toISOString().split("T")[0]
      }),
    });
    const data = await response.json();
    setPlan(data.plan);
    setNotification("✅ Learning plan generated!");
    setUnlockedIndex(0);
  };

  const startAssessment = (index) => {
    setActiveAssessmentIndex(index);
    setNotification("⚠️ Generate and complete both quiz and coding before submitting.");
    setQuizQuestions([]);
    setCodingQuestions([]);
    setQuizAnswers({});
    setCodingAnswers({});
    setAssessmentResult(null);
    setCodingResult(null);
  };

  const generateQuiz = async () => {
    if (activeAssessmentIndex === null) return;
    setNotification("Generating quiz...");
    const response = await fetch("http://localhost:5000/generate-quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: plan[activeAssessmentIndex].topic }),
    });
    const data = await response.json();
    setQuizQuestions(data);
    setNotification("✅ Quiz ready!");
  };

  const generateCoding = async () => {
    if (activeAssessmentIndex === null) return;
    setNotification("Generating coding questions...");
    const response = await fetch("http://localhost:5000/generate-coding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: plan[activeAssessmentIndex].topic }),
    });
    const data = await response.json();
    setCodingQuestions(data);
    setNotification("✅ Coding questions ready!");
  };

  const handleAnswerSelect = (qid, option) => {
    setQuizAnswers((prev) => ({ ...prev, [qid]: option }));
  };

  const handleCodingAnswerChange = (qid, text) => {
    setCodingAnswers((prev) => ({ ...prev, [qid]: text }));
  };

  const submitAssessment = async () => {
    if (quizQuestions.length === 0) {
      setNotification("❌ No quiz questions to submit.");
      return;
    }
    setNotification("Evaluating quiz...");
    const response = await fetch("http://localhost:5000/evaluate-quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        questions: quizQuestions,
        answers: quizAnswers,
      }),
    });
    const result = await response.json();
    setAssessmentResult(result);

    if (result.percentage >= 85) {
      setNotification(`🎉 You scored ${result.percentage}%. Next topic unlocked.`);
      setUnlockedIndex((prev) => prev + 1);
    } else {
      setNotification(`❌ You scored ${result.percentage}%. Try again.`);
    }
  };

  const submitCoding = async () => {
    if (codingQuestions.length === 0) {
      setNotification("❌ No coding questions to submit.");
      return;
    }
    setNotification("Evaluating coding...");
    const response = await fetch("http://localhost:5000/evaluate-coding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        questions: codingQuestions,
        answers: codingAnswers,
      }),
    });
    const result = await response.json();
    setCodingResult(result);
    setNotification(`✅ Coding evaluated. You scored ${result.percentage}%`);
  };

  return (
    <main className="bg-gray-900 min-h-screen p-8 text-white">
      <div className="max-w-xl mx-auto bg-gray-800 p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4">Learning Plan Generator</h1>

        <div className="mb-4">
          <label className="block mb-1">Goal</label>
          <input
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            className="w-full border border-gray-600 rounded px-4 py-3 text-white bg-gray-700 placeholder-gray-400 text-lg focus:outline-none focus:border-blue-400"
            placeholder="e.g., Learn Machine Learning"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1">Deadline</label>
          <DatePicker
            selected={deadline}
            onChange={(date) => setDeadline(date)}
            minDate={new Date()}
            dateFormat="dd-MM-yyyy"
            placeholderText="Select a date"
            className="w-full border border-gray-600 rounded px-4 py-3 text-white bg-gray-700 placeholder-gray-400 text-lg focus:outline-none focus:border-blue-400"
          />
        </div>

        <button
          onClick={generatePlan}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow"
        >
          Generate Plan
        </button>

        {notification && (
          <p className="mt-3 text-yellow-300">{notification}</p>
        )}
      </div>

      {plan.length > 0 && (
        <div className="max-w-4xl mx-auto mt-8 space-y-6">
          {plan.map((item, index) => (
            <div key={index} className={`p-4 border rounded ${index <= unlockedIndex ? "border-green-500" : "border-gray-600 opacity-50"}`}>
              <h2 className="text-xl font-bold">{item.topic}</h2>
              <p>{item.description}</p>
              <p><strong>Duration:</strong> {item.estimated_duration}</p>
              <p><strong>Deadline:</strong> {format(new Date(item.deadline), "dd-MM-yyyy")}</p>

              {index <= unlockedIndex && (
                <button
                  onClick={() => startAssessment(index)}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded"
                >
                  Take Assessment
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {activeAssessmentIndex !== null && (
        <div className="max-w-4xl mx-auto mt-8 space-y-6">
          {/* Quiz Section */}
          {quizQuestions.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-2">Quiz Questions</h3>
              {quizQuestions.map((q) => (
                <div key={q.id} className="mb-4">
                  <p className="font-semibold">{q.question}</p>
                  {q.options.map((opt) => (
                    <button
                      key={opt}
                      onClick={() => handleAnswerSelect(q.id, opt)}
                      className={`mr-2 mt-1 px-2 py-1 rounded border ${
                        quizAnswers[q.id] === opt ? "bg-blue-500" : "bg-gray-700"
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              ))}
              <button
                onClick={submitAssessment}
                className="mt-2 bg-purple-500 hover:bg-purple-600 px-3 py-1 rounded"
              >
                Submit Quiz
              </button>
              {assessmentResult && (
                <div className="mt-2 text-green-400">
                  Quiz Score: {assessmentResult.percentage}%
                </div>
              )}
            </div>
          )}

          {/* Coding Section */}
          {codingQuestions.length > 0 && (
            <div>
              <h3 className="text-xl font-bold mb-2">Coding Questions</h3>
              {codingQuestions.map((q) => (
                <div key={q.id} className="mb-4">
                  <p className="font-semibold">{q.question}</p>
                  <textarea
                    rows={4}
                    className="w-full border border-gray-600 rounded px-2 py-1 bg-gray-700 mt-1"
                    onChange={(e) => handleCodingAnswerChange(q.id, e.target.value)}
                    value={codingAnswers[q.id] || ""}
                  />
                </div>
              ))}
              <button
                onClick={submitCoding}
                className="mt-2 bg-purple-500 hover:bg-purple-600 px-3 py-1 rounded"
              >
                Submit Coding Answers
              </button>
              {codingResult && (
                <div className="mt-2 text-green-400">
                  Coding Score: {codingResult.percentage}%<br/>
                  Feedback:
                  <ul className="list-disc pl-5">
                    {codingResult.feedback.map((f, i) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Buttons to Generate */}
          {quizQuestions.length === 0 && (
            <button
              onClick={generateQuiz}
              className="mr-2 bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded"
            >
              Generate Quiz
            </button>
          )}
          {codingQuestions.length === 0 && (
            <button
              onClick={generateCoding}
              className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded"
            >
              Generate Coding
            </button>
          )}
        </div>
      )}
    </main>
  );
}
