from flask import Flask, render_template, request
import abstractExtractor
import queryGenerator
import QAfunctions

app = Flask(__name__)
def answerQuestion(title, question, config):
    question = title + question

    query = queryGenerator.generateQuery(config, question)
    papers = abstractExtractor.get_paper_info(query, 15)
    solution = QAfunctions.get_answer(question, papers, config)

    return solution


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form["question"]
        title = request.form["title"]
        config = "config.yaml"
        answer = answerQuestion("Title: " + title, "Details: " + question, config)

        return render_template("index.html", title=title, question=question, answer=answer)
    return render_template("index.html", title=None, question=None, answer=None)

if __name__ == "__main__":
    app.run(debug=True)