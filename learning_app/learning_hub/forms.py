import flask_wtf
import wtforms as wtf
from wtforms import validators as valid
from wtforms.fields.html5 import EmailField
from ..static import enums


class CreateQuestion(flask_wtf.FlaskForm):
    """
    Form for create question
    """
    qtype = wtf.SelectField("Question Type", choices=[(type.name, type.value) for type in enums.QuestionType], render_kw={"class": "form-control"})
    question_title = wtf.StringField("Question Title", [valid.InputRequired(message="Title is required")], render_kw={"class": "form-control"})
    question_text = wtf.StringField("Question Body", [valid.InputRequired(message="Quieston body is required")],
                                    widget=wtf.widgets.TextArea(), render_kw={"class": "form-control"})
    answer = wtf.StringField("Answer", [valid.InputRequired(message="Answer is required")], render_kw={"class": "form-control"})
    wrong_answer1 = wtf.StringField("Wrong Answer 1", render_kw={"class": "form-control"})
    wrong_answer2 = wtf.StringField("Wrong Answer 2", render_kw={"class": "form-control"})
    wrong_answer3 = wtf.StringField("Wrong Answer 3", render_kw={"class": "form-control"})
    notion = wtf.StringField("Notion", render_kw={"class": "form-control"})
    sub_notion = wtf.StringField("Sub Notion", render_kw={"class": "form-control"})
    is_exam = wtf.BooleanField("Is Exam", render_kw={"class": "form-control"})
    is_test_exam = wtf.BooleanField("Is Test Exam")
    level = wtf.SelectField("Complexity level", [valid.InputRequired(message="Complexity is required")],
                            choices=[(type.name, type.value) for type in enums.QuestionComplexity], render_kw={"class": "form-control"})
    time_for_completion = wtf.FloatField("Time for completion",
                                         render_kw={"class": "form-control","placeholder": "Time in minutes"})  # todo - change to actual time
    submit = wtf.SubmitField('Register Question', render_kw={"class": "form-control btn btn-success"})


class Notion(flask_wtf.FlaskForm):
    notion = wtf.StringField("Enter New Notion", [valid.InputRequired(message="input is Required")])


class SubNotion(flask_wtf.FlaskForm):
    notion = wtf.StringField("Enter Notion", [valid.InputRequired(message="input is Required")])
    # todo change to relationship with notion table
    sub_notion = wtf.StringField("Enter new sub notion", [valid.InputRequired(message="input is Required")])


class CreateExam(flask_wtf.FlaskForm):
    type = wtf.SelectField("Exam Type", choices=[(type.name, type.value) for type in enums.ExamType], render_kw={"class": "form-control"})
    exam_title = wtf.StringField("Exam Title", [valid.InputRequired(message="input is Required")], render_kw={"class": "form-control"})
    notion = wtf.StringField("Enter Notion", [valid.InputRequired(message="input is Required")], render_kw={"class": "form-control"})
    sub_notion = wtf.StringField("Enter new sub notion", render_kw={"class": "form-control"})
    level = wtf.SelectField("Complexity level", [valid.InputRequired(message="Complexity is required")],
                            choices=[(type.name, type.value) for type in enums.QuestionComplexity], render_kw={"class": "form-control"})
    time = wtf.StringField("Exam time", render_kw={"placeholder": "Time in minutes","class": "form-control"})
    submit = wtf.SubmitField('Register Exam', render_kw={"class": "btn btn-success form-control"})
