import datetime
import flask_sqlalchemy
import jwt
from flask_login import UserMixin
from flask_mail import Message
from .. import db, login_manager, mail_manager
import flask
from flask import current_app
from ..user_managment.models import Class

exams_to_questions = db.Table("exams_to_questions",
                              db.Column("quest_id", db.Integer, db.ForeignKey("questions.id")),
                              db.Column("exam_id", db.Integer, db.ForeignKey("exams.id")))

exams_to_class = db.Table("exams_to_class",
                          db.Column("exam_id", db.Integer, db.ForeignKey("exams.id")),
                          db.Column("class_id", db.Integer, db.ForeignKey("class.id")))


class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(264))
    question_text = db.Column(db.String())
    qtype = db.Column(db.PickleType())
    answer = db.Column(db.String())
    wrong_answer1 = db.Column(db.String(264))
    wrong_answer2 = db.Column(db.String(264))
    wrong_answer3 = db.Column(db.String(264))
    notion_id = db.Column(db.Integer, db.ForeignKey("notions.id"))
    notion = db.relationship("Notions", back_populates="question")
    sub_notion_id = db.Column(db.Integer, db.ForeignKey("subnotions.id"))
    sub_notion = db.relationship("SubNotions", back_populates="question")
    is_exam = db.Column(db.Boolean())
    is_test_exam = db.Column(db.Boolean())
    level = db.Column(db.PickleType())
    time_for_completion = db.Column(db.Float())
    exams = db.relationship("Exams", secondary="exams_to_questions", back_populates="questions")


class Exams(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    exam_title = db.Column(db.String(264))
    exam_type = db.Column(db.PickleType())
    level = db.Column(db.PickleType())
    time_for_completion = db.Column(db.Float())
    questions = db.relationship("Questions", secondary="exams_to_questions", back_populates="exams")
    notion_id = db.Column(db.Integer, db.ForeignKey("notions.id"))
    notion = db.relationship("Notions", back_populates="exam")
    sub_notion_id = db.Column(db.Integer, db.ForeignKey("subnotions.id"))
    sub_notion = db.relationship("SubNotions", back_populates="exam")
    classes = db.relationship("Class", secondary="exams_to_class", back_populates="exams")


Class.exams = db.relationship("Exams", secondary="exams_to_class", back_populates="classes")


class Notions(db.Model):
    __tablename__ = "notions"
    id = db.Column(db.Integer, primary_key=True)
    notion = db.Column(db.String(264), unique=True)
    question = db.relationship("Questions", back_populates="notion")
    exam = db.relationship("Exams", back_populates="notion")

    def __init__(self, notion):
        self.notion = notion

    def isnotion(self):
        notion = Notions.query.filter_by(notion=self.notion).first()
        if notion:
            return notion
        else:
            db.session.add(self)
            db.session.commit()
            return Notions.query.filter_by(notion=self.notion).first()


class SubNotions(db.Model):
    __tablename__ = "subnotions"
    id = db.Column(db.Integer, primary_key=True)
    sub_notion = db.Column(db.String(264), unique=True)
    question = db.relationship("Questions", back_populates="sub_notion")
    exam = db.relationship("Exams", back_populates="sub_notion")

    def __init__(self, sub_notion):
        self.sub_notion = sub_notion

    def issubnotion(self):
        sub_notion = SubNotions.query.filter_by(sub_notion=self.sub_notion).first()
        if sub_notion:
            return sub_notion
        else:
            db.session.add(self)
            db.session.commit()
            return SubNotions.query.filter_by(sub_notion=self.sub_notion).first()


class ExamScores(db.Model):
    __tablename__="exam_scores"
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    student = db.Column(db.Integer, db.ForeignKey("user.id"))
    exam = db.Column(db.Integer, db.ForeignKey("exams.id"))
    is_score_published= db.Column(db.Boolean)