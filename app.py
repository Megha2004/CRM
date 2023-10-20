from flask import Flask, render_template, request, jsonify
import spacy
import csv

nlp = spacy.load("en_core_web_lg")

dataset = []

with open("chatbot.csv", newline="", encoding="ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dataset.append({"Pattern": row["Pattern"], "Response": row["Response" ]})

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]

    if user_input.lower() == 'exit':
        response = "Goodbye!"
    else:
        similarities = {}
        user_input_doc = nlp(user_input)
        
        for data in dataset:
            pattern = nlp(data["Pattern"])
            similarity = user_input_doc.similarity(pattern)
            similarities[data["Pattern"]] = similarity

        app.logger.info("User Input: %s", user_input)
        app.logger.info("Similarities: %s", similarities)

        best_match = max(similarities, key=similarities.get)
        response = next(item["Response"] for item in dataset if item["Pattern"] == best_match)
    
    app.logger.info("Response: %s", response)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
