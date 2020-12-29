from students_db import app
from students_db import db
from flask import render_template, request, redirect, url_for, session
# from flask_session import Session
from students_db.models import Student, User
from students_db.forms import RegisterForm, AddStudent, LoginForm
from students_db.helpers import login_required



@app.route('/')
@app.route('/show')
@login_required
def show():
    students = Student.query.all()
    return render_template('table.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddStudent()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data, 
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('show'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f"There was an error with adding students: {err_msg}")
    return render_template('add.html', form=form)

    
@app.route("/delete/<int:id>", methods=["POST", "GET"])
@login_required
def delete(id):
    student = Student.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('show'))
    except:
        print("Something went wrong")
        return redirect(url_for('show'))


@app.route("/checkbox", methods=["GET", "POST"])
@login_required
def handle_checkbox():
    if request.method == "POST":
        students = request.form.getlist('checkbox')
        for s in students:
            s = Student.query.get(s)
            db.session.delete(s)
            db.session.commit()
        return redirect(url_for('show'))
    return redirect(url_for('show'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, password_hash=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        print('registration status: sucess')
        return redirect(url_for('show'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    print(form.username.data)
    print(form.password.data)

    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password_hash == form.password.data:
                print('login status: success')
                return redirect(url_for('show'))
    print('login status: failed')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

