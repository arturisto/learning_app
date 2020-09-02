import flask, flask_login
import requests
from .. import db, login_manager
from flask import request, flash, redirect, session, url_for, current_app, render_template
from . import learning_hub_bp
from . import forms, models
from ..static import constant_functions as const_func
from ..static import enums
import jwt
from ..user_managment import models as user_models


@learning_hub_bp.route("/free-for-all")
def free_for_all_questions():
    return render_template("free_for_all_q.html")


@learning_hub_bp.route("/get_q_ids_free_for_all", methods=["POST", "GET"])
def get_q_ids_free_for_all():
    is_timed = request.json
    if is_timed:
        questions = models.Questions.query.filter(models.Questions.time_for_completion > "0",
                                                  models.Questions.is_exam == "0",
                                                  models.Questions.is_test_exam == "0").all()

    else:
        questions = models.Questions.query.filter(models.Questions.is_exam == "0",
                                                  models.Questions.is_test_exam == "0").all()

    return create_response(questions, is_timed)


@learning_hub_bp.route("/get_q_by_id", methods=["POST", "GET"])
def get_q_by_id():
    response = ""

    q = models.Questions.query.filter_by(id=request.json).first()

    return build_q_response(q)


def build_q_response(q):
    if q.qtype == enums.QuestionType.SINGLE:
        response = {"id": q.id,
                    "title": q.question_title,
                    "body": q.question_text,
                    "answer": q.answer,
                    "type": q.qtype.value,
                    "notion": q.notion.notion,
                    "subnotion": q.sub_notion.sub_notion,
                    "level": q.level.value,
                    "time": q.time_for_completion}
    else:
        response = {"id": q.id,
                    "title": q.question_title,
                    "body": q.question_text,
                    "answer": q.answer,
                    "wrong1": q.wrong_answer1,
                    "wrong2": q.wrong_answer2,
                    "wrong3": q.wrong_answer3,
                    "type": q.qtype.value,
                    "notion": q.notion.notion,
                    "subnotion": q.sub_notion.sub_notion,
                    "level": q.level.value,
                    "time": q.time_for_completion}
    return response


@learning_hub_bp.route("/exe_by_notion", methods=["POST", "GET"])
def exe_by_notion():
    notions = models.Notions.query.all()
    subnotions = models.SubNotions.query.all()
    return render_template("exercise_by_notion.html", notions=notions, subnotions=subnotions)


@learning_hub_bp.route("/get_q_by_notion", methods=["POST", "GET"])
def get_q_by_notion():
    notion = models.Notions.query.filter_by(notion=request.json[0]).first()
    sub_notion = models.SubNotions.query.filter_by(sub_notion=request.json[1]).first()
    is_timed = request.json[2]
    if is_timed:
        questions = models.Questions.query.filter(models.Questions.time_for_completion > "0", \
                                                  models.Questions.is_exam == "0", \
                                                  models.Questions.is_test_exam == "0", \
                                                  models.Questions.notion_id == notion.id, \
                                                  models.Questions.sub_notion_id == sub_notion.id).all()

    else:
        questions = models.Questions.query.filter(models.Questions.is_exam == 0, \
                                                  models.Questions.is_test_exam == 0, \
                                                  models.Questions.notion_id == notion.id, \
                                                  models.Questions.sub_notion_id == sub_notion.id).all()

    if questions:
        return create_response(questions, is_timed)
    else:
        return "false"


def create_response(questions, timer):
    response = {}
    if timer:
        for number, q in enumerate(questions):
            response[number] = [q.id, q.time_for_completion]
    else:
        for number, q in enumerate(questions):
            response[number] = [q.id]
    return response


@learning_hub_bp.route("/exams")
def exams_main():
    if session["role"] != enums.UserType.STUDENT:
        flash("This is student area, teachers and admins belong in management", category="student_vs_teachers")
        return render_template("exams.html")
    exams = ""
    student_email = session['user_email']
    student_class = user_models.User.query.filter_by(email=student_email).first()
    if not student_class.class_name:
        flash("You are not assigned to class", category="error")

    elif not student_class.class_name.exams:
        flash("You are not assigned an exam", category="error")
    else:
        exams = student_class.class_name.exams
    return render_template("exams.html", exams=exams)


@learning_hub_bp.route("/get_exam", methods=["POST", "GET"])
def get_exam():
    exam_id = request.json

    exam = models.Exams.query.filter_by(id=exam_id).first()
    response = {"id": exam.id,
                "name": exam.exam_title,
                "time": exam.time_for_completion}

    return response


@learning_hub_bp.route("/get_questions_by_exam", methods=["POST", "GET"])
def get_questions_by_exam():
    exam_id = request.json
    exam = models.Exams.query.filter_by(id=exam_id).first()
    questions = models.Questions.query.filter(models.Questions.exams.contains(exam)).all()
    response = {}
    return create_response(questions, False)


@learning_hub_bp.route("/submit_exam", methods=['POST', 'GET'])
def submit_exam():
    calculate_exam_score(request.json)
    return "True"


def calculate_exam_score(answer_sheet):
    """
    The score, for now is calculated by equal amount - 100 / number of questions
    """
    exam = models.Exams.query.filter_by(id=answer_sheet["exam_id"]).first()
    student = user_models.User.query.filter_by(email=session['user_email']).first()
    number_of_questions = len(exam.questions)
    number_of_correct_questions = 0
    exam_questions = exam.questions
    for answer in answer_sheet['answers']:
        for q in exam_questions:
            if answer['answer'] == q.answer:
                number_of_correct_questions += 1

    score = (number_of_correct_questions / number_of_questions) * 100

    exam_score = models.ExamScores()
    exam_score.score = score
    exam_score.student = student.id
    exam_score.exam = exam.id
    db.session.add(exam_score)
    db.session.commit()

    return True


@learning_hub_bp.route("/practice_exam")
def practice_exam():
    return redirect(url_for("main.under_const"))
