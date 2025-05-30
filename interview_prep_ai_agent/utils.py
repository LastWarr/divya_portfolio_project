from openai import OpenAI
import os
import json
import random
from datetime import date
import streamlit as st

OpenAI.api_key = st.secrets["openai"]["api_key"]
apikey = st.secrets["openai"]["api_key"]
HISTORY_FILE = "interview_prep_ai_agent/history.json"

TOPICS_FILE = "interview_prep_ai_agent/topics_pool.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            content = f.read().strip()
            if content == "":  
                # Empty file, return default structure
                return {"dates": {}, "covered": []}
            try:
                history = json.loads(content)
                # Ensure required keys exist
                if "dates" not in history:
                    history["dates"] = {}
                if "covered" not in history:
                    history["covered"] = []
                return history
            except json.JSONDecodeError:
                # Corrupted file: reset structure
                return {"dates": {}, "covered": []}
    # File doesn't exist
    return {"dates": {}, "covered": []}

def save_history(history):
    # Ensure keys before saving
    if "dates" not in history:
        history["dates"] = {}
    if "covered" not in history:
        history["covered"] = []
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_topics():
    with open(TOPICS_FILE, "r") as f:
        return json.load(f)

def get_daily_topic():
    today = str(date.today())
    history = load_history()
    all_topics = load_topics()
    if "covered" in history:
        covered = history["covered"]
    else:
        covered = []

    # Return today's topic if already generated
    if today in history["dates"]:
        return history["dates"][today]

    # Filter out already covered topics
    remaining = [t for t in all_topics if t not in covered]

    if not remaining:
        return "🎉 You've covered all topics! Reset your history to start over."

    topic = random.choice(remaining)
    history["dates"][today] = topic
    history["covered"].append(topic)
    save_history(history)

    return topic

def generate_prompt(task, topic=None, user_answer=None, content=None, goal=None):
    if task == "Quiz Me":
        return f"Ask me 3 interview-style questions on the topic: {topic}."
    elif task == "Explain Simply":
        return f"Explain '{topic}' in simple terms like you're teaching a beginner."
    elif task == "Mock Interview":
        return f"You're an interviewer. Start a mock interview on: {topic}. Ask one question at a time."
    elif task == "Evaluate My Answer":
        return f"Evaluate this answer to the question '{topic}': {user_answer}. Give feedback, what’s good, what to improve."
    elif task == "Study Plan":
        return f"Create a 2-week personalized interview study plan for ML/Stats/Deep Learning. My goal: {goal}"
    elif task == "Summarize Notes":
        return f"Summarize the following technical content into key points and a TL;DR: {content}"
    else:
        return f"Help me with: {topic}"

def ask_gpt(task, topic=None, user_answer=None, content=None, goal=None):
    prompt = generate_prompt(task, topic, user_answer, content, goal)

    client = OpenAI(api_key=apikey)

    response = client.responses.create(
        model="gpt-4o",
        instructions="Talk like a helpful data science interview coach",
        input="" + prompt + "\n\nPlease provide a detailed response with examples and explanations.",
    )
    return response.output_text