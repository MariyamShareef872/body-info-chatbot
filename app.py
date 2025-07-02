from flask import Flask, render_template, request
import csv

app = Flask(__name__)

body_info = {}

# 📥 Load CSV
with open("body_facts.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        part = row["part"].strip().lower()
        body_info[part] = {
            "info": row["info"],
            "image": "/" + row["image"]
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get("msg").strip().lower()

    # ✅ Step 1: Try exact match
    if user_input in body_info:
        data = body_info[user_input]
        return f"""
            <div style="text-align: center;">
                <b style="font-size: 18px;">{user_input.title()}</b><br>
                <p>{data['info']}</p>
                <img src="{data['image']}" alt="{user_input}" style="width: 180px; height: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); margin-top: 10px;">
            </div>
        """

    # ✅ Step 2: Try partial matches
    for part in body_info:
        if part in user_input or user_input in part:
            data = body_info[part]
            return f"""
                <div style="text-align: center;">
                    <b style="font-size: 18px;">{part.title()}</b><br>
                    <p>{data['info']}</p>
                    <img src="{data['image']}" alt="{part}" style="width: 180px; height: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); margin-top: 10px;">
                </div>
            """

    return "Sorry, I don't have information about that body part yet."

if __name__ == "__main__":
    app.run(debug=True)