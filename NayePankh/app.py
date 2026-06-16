from flask import Flask, request, jsonify, session
from flask import render_template_string
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, render_template_string, send_from_directory

import os

load_dotenv()

app = Flask(__name__)

app.secret_key = "chatbot_secret"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


with open("index.html", "r", encoding="utf-8") as f:
    HTML = f.read()
    
@app.route("/styles.css")
def style():

    return send_from_directory(".", "styles.css")


@app.route("/script.js")
def script():

    return send_from_directory(".", "script.js")

@app.route("/")
def home():

    if "messages" not in session:

        session["messages"] = [

            {
                "role":"system",

                "content":"""

You are an AI chatbot for students.

Help users regarding:

- Careers
- Internships
- Skills
- Education
- Programming
- Technology

Be friendly and concise.

"""

            }

        ]

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])

def chat():

    user_message = request.json["message"]

    messages = session["messages"]

    messages.append(

        {
            "role":"user",

            "content":user_message
        }

    )

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages,

        temperature=0.7,

        max_tokens=500

    )

    reply = response.choices[0].message.content

    messages.append(

        {
            "role":"assistant",

            "content":reply
        }

    )

    session["messages"] = messages

    return jsonify({

        "reply":reply

    })


@app.route("/history")

def history():

    return jsonify(

        session.get("messages",[])

    )


@app.route("/clear")

def clear():

    session.pop("messages",None)

    return jsonify({

        "status":"cleared"

    })


if __name__ == "__main__":

    app.run(debug=True)