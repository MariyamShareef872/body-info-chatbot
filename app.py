import csv
from flask import Flask, render_template, request
from difflib import get_close_matches

app = Flask(__name__)
qa_data = {}

# Load data from CSV
with open("body_facts.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header if present
    for row in reader:
        if len(row) >= 2:
            question = row[0].strip().lower()
            answer = row[1].strip()
            image = row[2].strip() if len(row) > 2 else ""
            if image:
                answer += f"<br><img src='/static/images/{image}' width='180'>"
            qa_data[question] = answer

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get("msg").strip().lower()

    # Exact match
    if user_input in qa_data:
        return qa_data[user_input]

    # Fuzzy match
    matches = get_close_matches(user_input, qa_data.keys(), n=1, cutoff=0.6)
    if matches:
        return f"(Did you mean: '{matches[0]}'?)<br>{qa_data[matches[0]]}"

    return "😕 I couldn’t find any matching information."

if __name__ == "__main__":
    app.run(debug=True)
