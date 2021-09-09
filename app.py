from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

 #from user's answers, put in here ['Yes', 'No', 'Less than $10,000', 'Yes']

@app.get('/')
def show_form():
    """shows the main page - title of survey, instructions and start button"""
    session["responses"] = []
    return render_template("survey_start.html", 
        survey_title = survey.title ,
        survey_instructions = survey.instructions)

@app.post('/begin')
def start_survey():
    """Redirects user to the first question of survey"""
    return redirect('/questions/0')

@app.get('/questions/<int:q_num>')
def show_questions(q_num):
    """render question template, once they hit the button, it sends a post request
    and redirects to next question (get req)"""
    current_question = len(session["responses"])
    if q_num > current_question:
        flash("Redirecting to next question in survey")
        return redirect(f"/questions/{current_question}")
    return render_template("question.html", question = survey.questions[q_num])


@app.post('/answer')
def handle_answer():
    """handle post request from user answers and append to responses list"""

    responses = session["responses"]
    responses.append(request.form.get("answer"))
    session["responses"] = responses
    next_q_num = len(responses)
    
    if next_q_num > len(survey.questions) - 1:
        return redirect("/thanks")

    return redirect(f"/questions/{next_q_num}")

@app.get('/thanks')
def completed():
    """Returns a thank you page once the user has completed the survey"""
    return render_template("completion.html")

