import flask, flask_login
from .. import db
from flask import request, flash, redirect, session, url_for, current_app, render_template
from . import user_blueprint
from . import forms, models
from ..static.enums import UserType
from ..static import constant_functions as const_func
from ..learning_hub import models as hub_models
import jwt


# ----------------------login/out----------------------------------
@user_blueprint.route("/login_show")
def login_show():
    form = forms.Login()
    if "user" in session:
        return redirect("/profile")
    else:
        return render_template("login.html", form=form)


@user_blueprint.route("/login", methods=['POST', "GET"])
def login():
    # check if user in the DB:
    form = forms.Login()
    user = models.User.query.filter_by(email=form.email.data).first()
    if user:
        if user.password == form.password.data:
            session["user"] = user.username
            session['user_email'] = user.email
            session['role'] = user.role
            flash("login complete, great success!")
            flask_login.login_user(user)
            if user.role == UserType.ADMIN:
                return flask.render_template("admin.html")
            return redirect(url_for("main.index"))
        else:
            flask.flash("password is in correct", category="password")
            return redirect(url_for("users.login_show"))
    else:
        flask.flash("email doesn't exists", category="user")
        return redirect(url_for("users.login_show"))


@user_blueprint.route("/signin_show")
def signin_view():
    form = forms.CreateUser()
    return render_template("signin.html", form=form)


@user_blueprint.route("/signup", methods=['POST', "GET"])
def signup():

    form = forms.CreateUser()
    user = models.User.query.filter_by(username=form.username.data).first()
    if user:
        if user.email == form.email.data:
            flash("email is taken, please use another")
        elif user.username == form.email.data:
            flash("username is taken, please use another")
    else:
        user_role = ''
        for key in UserType:
            if key.name == form.role.data:
                user_role = key

        new_user = models.User(email=form.email.data, password=form.password.data,
                               username=form.username.data, name=form.name.data, role=user_role)
        db.session.add(new_user)
        db.session.commit()
        # todo add check the user creation function
        user_check = models.User.query.filter_by(email = form.email.data).first()
        if user_check:
            flash("user created successfully", category="success")
        else:
            flash("something went wrong", category="fail")

        return redirect(url_for("users.management_home_page"))

    return redirect(url_for("main.index"))


@user_blueprint.route("/signout", methods=['POST', "GET"])
def signout():
    session.clear()
    return redirect(url_for("main.index"))


@user_blueprint.route("/password_forget")
def renew_password():
    return render_template("renew_pass.html")


@user_blueprint.route("/send_pass_link", methods=['POST', "GET"])
def send_pass_link():
    user = models.User.query.filter_by(email=request.form['email']).first()

    if user:
        user.send_pass_link()
        return redirect(url_for("main.index"))
    else:
        flask.flash("email doesn't exists", category="user")
        return redirect(url_for("users.renew_password"))


@user_blueprint.route("/reset_password")
def reset_password():
    token = request.args['jwt_token']
    user = verify_access_token(token)
    if not user:
        pass
    else:
        form = forms.password_reset()
        return flask.render_template("reset_password.html", form=form, email=user.email)


@user_blueprint.route("/change_password", methods=['POST', "GET"])
def change_password():
    form = request.form
    try:
        user = models.User.query.filter_by(email=form['email']).first()
        user.password = form['password']
        db.session.commit()
        flask.flash("password changed successfully")
    except Exception as e:
        print(e)
        return None

    return redirect(url_for("main.index"))


def verify_access_token(token):
    try:
        user_id = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'])
    except Exception as e:
        print(e)
        return None
    return models.User.query.filter_by(id=user_id['user_id']).first()


# # ----------------------end of login/out----------------------------------

# #-----------------------Start of user profile pages ----------------------
@user_blueprint.route('/profile/')
@flask_login.login_required
def profile():
    # get the user from the DB.

    return redirect(url_for("main.under_const"))


# # #-----------------------End of user profile pages ----------------------
#
# # # ----------------------start of management area----------------------------------
@user_blueprint.route("/management")
def management_home_page():
    # if const_func.check_role(UserType.ADMIN):
    #     form_create_user = forms.CreateUser()
    #     return flask.render_template("management_home.html", sign_up_form=form_create_user,
    #                                  student_list=set_students_as_Choices())
    #
    # else:
    #     return flask.redirect(url_for("main.index"))
     form_create_user = forms.CreateUser()
     return flask.render_template("management_home.html", sign_up_form=form_create_user,
                                     student_list=set_students_as_Choices())

def set_students_as_Choices():
    students = models.User.query.filter_by(role=UserType.STUDENT).all()
    students_to_assign = {}
    for s in students:
        if not s.class_id:
            students_to_assign[s.id] = [s.name, s.email]
    return students_to_assign


@user_blueprint.route("/find_user", methods=['POST', "GET"])
def find_user():
    user_email = ""
    if request.method == "POST":
        user_email = request.json
        user = models.User.query.filter_by(email=user_email).first()
        response = {"email": user.email, "name": user.name, 'username': user.username, "role": user.role,
                    "user_id": user.id}
        return response
    return user_email


@user_blueprint.route("/update_user", methods=['POST', 'GET'])
def update_user():
    form = request.form
    user = models.User.query.filter_by(id=request.form['user_id']).first()
    user.name = form['name']
    user.email = form['email']
    user.role = form['role']
    user.username = form['username']
    db.session.commit()
    return redirect(url_for("users.management_home_page"))


@user_blueprint.route("/delete_user", methods=['POST', 'GET'])
def delete_user():
    email = request.form['d_email']
    user = models.User.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        user_check = models.User.query.filter_by(email=email).first()
        if not user_check:
            flash("user deleted successfully", category="success")
        else:
            flash("something went wrong", category="fail")
    else:
        flash("Email doesn't exist", category="fail")

    return redirect(url_for("users.management_home_page"))


@user_blueprint.route("/create_new_class", methods=['POST', 'GET'])
def create_new_class():
    form = request.form
    student_list = []
    for key, value in form.items():
        if "student_" in key:
            student_list.append(models.User.query.filter_by(id=form[key]).first())

    new_class = models.Class(class_name=form['class_name'], users=student_list)
    db.session.add(new_class)
    db.session.commit()

    new_class = models.Class.query.filter_by(class_name =form['class_name'])
    if new_class:
        flash("class created successfully", category="success")
    else:
        flash("something went wrong", category="fail")

    return redirect(url_for("users.management_home_page"))



@user_blueprint.route("/find_class", methods=['POST', 'GET'])
def find_class():
    class_name = request.json
    class_data = models.Class.query.filter_by(class_name=class_name).first()
    response = {class_name: []}
    for user in class_data.users:
        response[class_name].append((user.id, user.name, user.email))
    return response


@user_blueprint.route("/delete_student", methods=['POST', 'GET'])
def delete_student():
    students_to_remove_from_class = request.form
    students_to_remove_from_class = students_to_remove_from_class.to_dict(flat=False)
    class_name = students_to_remove_from_class["class_name"]
    del students_to_remove_from_class["class_name"]
    for key, value in students_to_remove_from_class.items():
        user = models.User.query.filter_by(id=value[0]).first()
        user.class_id = None
        db.session.commit()

    if check_delete_class(class_name):
        flash ("Class and Students were deleted", category="success")
    else:
        flash("Students were deleted from class", category="success")

    return redirect(url_for("users.management_home_page"))


def check_delete_class(class_name):
    student_class = models.Class.query.filter_by(class_name=class_name[0]).first()

    if not student_class.users:
        db.session.delete(student_class)
        db.session.commit()
        return True
    return False

@user_blueprint.route("/admin_landing_page", methods=['POST', 'GET'])
def admin_landing_page():
    response = {}
    students = models.User.query.filter_by(role=UserType.STUDENT).all()
    classes = models.Class.query.all()
    questions = hub_models.Questions.query.all()
    exams = hub_models.Exams.query.all()
    exam_scores = hub_models.ExamScores.query.all()
    notions = hub_models.Notions.query.all()
    num_of_students = len(students)
    response['num_of_students'] = num_of_students
    num_of_questions = len(questions)
    response['num_of_questions'] = num_of_questions
    num_of_classes = len(classes)
    response['num_of_classes'] = num_of_classes
    response['students_by_class'] = get_studnets_by_class(students, classes)
    response['avg_score_by_exam'] = get_avg_score_by_exam(exams, exam_scores)
    response['q_by_notion'] = get_q_by_notion(questions, notions)
    return response


def get_studnets_by_class(students, classes):
    classes_by_studedents = {}
    for cls in classes:
        if cls.class_name not in classes_by_studedents:
            classes_by_studedents[cls.class_name] = {'stdnt_amnt': 0}

        for student in students:
            if student.class_name == cls:
                classes_by_studedents[cls.class_name]['stdnt_amnt'] += 1

        classes_by_studedents[cls.class_name]['max_capacity'] = cls.max_capacity
    return classes_by_studedents


def get_avg_score_by_exam(exams, exam_scores):
    scores_by_exam = {}
    num_of_exam_takers = 0
    for exam in exams:
        exam_total = 0
        num_of_exam_takers = 0
        for student_score in exam_scores:
            if student_score.exam == exam.id:
                exam_total += student_score.score
                num_of_exam_takers += 1
        if num_of_exam_takers > 0:
            scores_by_exam[exam.exam_title] = exam_total / num_of_exam_takers

    return scores_by_exam


def get_q_by_notion(questions, notions):
    q_by_notion = {}

    for notion in notions:
        if notion.notion not in q_by_notion:
            q_by_notion[notion.notion] = 0

        for q in questions:
            if q.notion_id == notion.id:
                q_by_notion[notion.notion] += 1
    return q_by_notion


@user_blueprint.route("/admin_page", methods=['POST', 'GET'])
def admin_page():
    if session['role'] == UserType.ADMIN:
        return flask.render_template("admin.html")
    else:
        return redirect(url_for("main.home"))
