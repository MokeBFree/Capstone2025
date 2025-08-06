# weather_app/core/quiz.py

import tkinter as tk
from tkinter import ttk, messagebox

def generate_quiz_tab(app):
    quiz_tab = ttk.Frame(app.notebook)
    app.notebook.add(quiz_tab, text="Quiz")

    # Sample placeholder questions (you can load from CSV instead)
    questions = [
        {
            "question": "Which city had the highest temperature yesterday?",
            "options": ["New York", "Phoenix", "Chicago", "Denver"],
            "answer": "Phoenix"
        },
        {
            "question": "Which weather condition is typical during a high-pressure system?",
            "options": ["Rain", "Snow", "Clear skies", "Thunderstorms"],
            "answer": "Clear skies"
        },
        {
            "question": "What unit is used to measure atmospheric pressure?",
            "options": ["Inches", "Pascals", "Millibars", "Liters"],
            "answer": "Millibars"
        },
        {
            "question": "Which tool measures wind speed?",
            "options": ["Barometer", "Thermometer", "Anemometer", "Hygrometer"],
            "answer": "Anemometer"
        },
        {
            "question": "Which of these is *not* a cloud type?",
            "options": ["Stratus", "Cumulus", "Nimbus", "Altifog"],
            "answer": "Altifog"
        },
    ]

    app.user_answers = []

    def submit_answers():
        score = 0
        for idx, q in enumerate(questions):
            selected = app.user_answers[idx].get()
            if selected == q["answer"]:
                score += 1
        messagebox.showinfo("Quiz Result", f"You scored {score} out of {len(questions)}")

    for i, q in enumerate(questions):
        q_label = ttk.Label(quiz_tab, text=f"{i+1}. {q['question']}")
        q_label.pack(anchor="w", pady=(10 if i == 0 else 5, 0), padx=10)

        answer_var = tk.StringVar()
        app.user_answers.append(answer_var)

        for option in q["options"]:
            r = ttk.Radiobutton(quiz_tab, text=option, value=option, variable=answer_var)
            r.pack(anchor="w", padx=30)

    submit_btn = ttk.Button(quiz_tab, text="Submit Answers", command=submit_answers)
    submit_btn.pack(pady=20)