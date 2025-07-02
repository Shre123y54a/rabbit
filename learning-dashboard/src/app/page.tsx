"use client";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function Home() {
  const [goal, setGoal] = useState("");
  const [deadline, setDeadline] = useState<Date | null>(null);
  const [notification, setNotification] = useState("");
  const [plan, setPlan] = useState([]);
  const [activeAssessmentIndex, setActiveAssessmentIndex] = useState<number | null>(null);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [codingQuestions, setCodingQuestions] = useState([]);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [assessmentResult, setAssessmentResult] = useState(null);
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

  const startAssessment = (index: number) => {
    setActiveAssessmentIndex(index);
    setNotification("⚠️ Generate and complete both quiz and coding before submitting.");
    setQuizQuestions([]);
    setCodingQuestions([]);
    setQuizAnswers({});
    setAssessmentResult(null);
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
    setQuizQuestions(data.questions);
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
    setCodingQuestions(data.questions);
    setNotification("✅ Coding questions ready!");
  };

  const handleAnswerSelect = (qid, option) => {
    setQuizAnswers((prev) => ({ ...prev, [qid]: option }));
  };

  const submitAssessment = async () => {
    if (quizQuestions.length === 0) {
      setNotification("❌ No quiz questions to submit.");
      return;
    }
    setNotification("Evaluating...");
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
      setActiveAssessmentIndex(null);
    } else {
      setNotification(`❌ You scored ${result.percentage}%. Try again.`);
    }
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
            placeholder="e.g., Learn Python"
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
            calendarClassName="!text-base !p-4"
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
        <div className="max-w-4xl mx-auto mt-8">
          <table className="w-full border border-gray-700">
            <thead>
              <tr>
                <th className="border px-4 py-2">#</th>
                <th className="border px-4 py-2">Topic</th>
                <th className="border px-4 py-2">Description</th>
                <th className="border px-4 py-2">Estimated Duration</th>
                <th className="border px-4 py-2">Deadline</th>
                <th className="border px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {plan.map((item, index) => (
                <tr key={index}>
                  <td className="border px-4 py-2">{index + 1}</td>
                  <td className="border px-4 py-2">{item.topic}</td>
                  <td className="border px-4 py-2">{item.description}</td>
                  <td className="border px-4 py-2">{item.estimated_duration}</td>
                  <td className="border px-4 py-2">
                    {new Date(item.deadline).toLocaleDateString("en-GB")}
                  </td>
                  <td className="border px-4 py-2">
                    <button
                      onClick={() => startAssessment(index)}
                      disabled={index > unlockedIndex}
                      className={`px-3 py-1 rounded ${
                        index <= unlockedIndex
                          ? "bg-blue-500 hover:bg-blue-600"
                          : "bg-gray-600 cursor-not-allowed"
                      }`}
                    >
                      Take Assessment
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeAssessmentIndex !== null && (
        <div className="max-w-4xl mx-auto mt-8 space-y-6">
          <div>
            <button
              onClick={generateQuiz}
              className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded mr-2"
            >
              Generate Quiz
            </button>
            <button
              onClick={generateCoding}
              className="bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded"
            >
              Generate Coding Questions
            </button>
          </div>

          {quizQuestions.length > 0 && (
            <table className="w-full border border-gray-700 mt-4">
              <thead>
                <tr>
                  <th className="border px-4 py-2">Question</th>
                  <th className="border px-4 py-2">Options</th>
                </tr>
              </thead>
              <tbody>
                {quizQuestions.map((q, i) => (
                  <tr key={i}>
                    <td className="border px-4 py-2">{q.question}</td>
                    <td className="border px-4 py-2">
                      {q.options.map((opt, j) => (
                        <label key={j} className="mr-4">
                          <input
                            type="radio"
                            name={`q-${i}`}
                            value={opt}
                            checked={quizAnswers[q.id] === opt}
                            onChange={() => handleAnswerSelect(q.id, opt)}
                            className="mr-1"
                          />
                          {opt}
                        </label>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {codingQuestions.length > 0 && (
            <div className="mt-4">
              <h3 className="text-lg font-semibold mb-2">Coding Questions</h3>
              <ul className="list-disc list-inside space-y-2">
                {codingQuestions.map((c, i) => (
                  <li key={i}>{c.question}</li>
                ))}
              </ul>
            </div>
          )}

          {quizQuestions.length > 0 && (
            <button
              onClick={submitAssessment}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded mt-4"
            >
              Submit Assessment
            </button>
          )}

          {assessmentResult && (
            <p className="text-yellow-300 mt-2">
              You scored {assessmentResult.percentage}% ({assessmentResult.correct_count} out of {assessmentResult.total_questions})
            </p>
          )}
        </div>
      )}
    </main>
  );
}
