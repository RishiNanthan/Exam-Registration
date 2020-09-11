from flask import Flask, render_template, request, session, redirect, url_for, send_file
from database import Student, Exam, ExamController, get_all_exams
from hall_ticket import generate_hall_ticket


HOST = "127.0.0.1"
PORT = 8000
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/student/login/', methods=['GET', 'POST'])
def student_login():
    if 'email' in session:
        s = Student()
        if s.login(session['email'], session['password']):
            return render_template('student_home.html')
        return '<script>alert("Retry Login!")</script>' + render_template('student_login.html')
    if request.method == 'GET':
        return render_template('student_login.html')
    else:
        email = request.form['email']
        pwd = request.form['password']
        stu = Student()
        if stu.login(email, pwd):
            session['email'] = stu.email
            session['password'] = stu.password
            return render_template('student_home.html')
        return '<script>alert("Retry Login!")</script>' + render_template('student_login.html')


@app.route('/student/registered_exams/', methods=['GET'])
def student_registered_exams():
    if 'email' in session:
        s = Student()
        if s.login(session['email'], session['password']):
            exams = s.registered_exams()
            return render_template('student_registered_exams.html', exams=exams)
    return '<script>alert("Retry Login!")</script>' + render_template('student_login.html')


@app.route("/student/view_registered_exam/", methods=['POST'])
def student_view_registered_exam():
    if 'email' in session:
        e = Exam()
        if e.get_exam(request.form['subject_code']):
            return render_template('student_view_registered_exam.html', exam=e)
        return redirect(url_for("student_registered_exams"))
    return redirect(url_for("home"))


@app.route('/student/signup/', methods=['GET', 'POST'])
def student_signup():
    if 'email' in session:
        s = Student()
        if s.login(session['email'], session['password']):
            return render_template('student_home.html')
        return '<script>alert("Retry Login!")</script>' + render_template('student_login.html')
    if request.method == 'GET':
        return render_template('student_signup.html')
    else:
        s = Student()
        roll_no = request.form['roll_no']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dept = request.form['dept']
        college = request.form['college']
        if s.signup(roll_no, password, name, email, phone, dept, college):
            session['email'] = email
            session['password'] = password
            return '<script>alert("Account Created Successfully!")</script>' + render_template('student_home.html')
        return '<script>alert("Retry Signup!")</script>' + render_template('student_signup.html')


@app.route('/student/password/', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET' and 'email' in session:
        return render_template('change_password.html')
    elif request.method == 'POST':
        s = Student()
        if s.login(session['email'], session['password']):
            pwd = request.form['password']
            new_pwd = request.form['new_password']
            if s.change_password(pwd, new_pwd):
                session['password'] = new_pwd
                exams = s.registered_exams()
                return '<script>alert("Password changed successfully!")</script>' + render_template('student_home.html',
                                                                                                    exams=exams)
            return '<script>alert("Wrong Password")</script>' + render_template('change_password.html')
        return '<script>alert("Retry Login")</script>' + render_template('student_login.html')
    else:
        return redirect(url_for("student_login"))


@app.route('/student/register/', methods=['GET', 'POST'])
def student_register():
    if 'email' not in session:
        return redirect(url_for('student_login'))
    if request.method == 'GET':
        exams = get_all_exams()
        return render_template('student_register.html', exams=exams)
    else:
        sub_code = request.form['subject_code']
        s = Student()
        exams = get_all_exams()
        if s.login(session['email'], session['password']):
            if s.register(sub_code):
                return '<script>alert("Successfully Registered!")</script>' + render_template(
                    'student_register.html', exams=exams)
            return '<script>alert("Already Registered!")</script>' + render_template('student_register.html',
                                                                                     exams=exams)
        return '<script>alert("Session Expired! Retry Login..")</script>' + render_template('student_login.html')


@app.route('/student/unregister/', methods=['POST'])
def student_unregister():
    if 'email' not in session:
        return redirect(url_for('student_login'))
    if request.method == 'POST':
        sub_code = request.form['subject_code']
        s = Student()
        if s.login(session['email'], session['password']):
            exams = s.registered_exams()
            if s.cancel_exam(sub_code):
                return '<script>alert("Exam Cancelled Successfully!")</script>' + render_template(
                    'student_registered_exams.html', exams=s.registered_exams())
            return '<script>alert("Retry!")</script>' + render_template('student_registered_exams.html', exams=exams)
        return '<script>alert("Session Expired... Retry Login!")</script>' + render_template('student_login.html')


@app.route('/student/logout/')
def student_logout():
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('home'))


@app.route('/exam/login/', methods=['GET', 'POST'])
def exam_login():
    if 'username' in session:
        return render_template('exam_home.html')
    if request.method == 'GET':
        return render_template('exam_login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        e = ExamController()
        if e.login(username, password):
            session['username'] = e.username
            return render_template('exam_home.html')
        return '<script>alert("Retry Login!")</script>' + render_template('exam_login.html')


@app.route('/exam/add_exam/', methods=['GET', 'POST'])
def add_exam():
    if 'username' in session and request.method == 'GET':
        return render_template('add_exam.html')
    elif 'username' in session and request.method == 'POST':
        sub_code = request.form['subject_code']
        sub_name = request.form['subject_name']
        domain = request.form['domain']
        exam_fee = request.form['exam_fee']
        exam_date = request.form['exam_date']
        syllabus = request.form['syllabus']
        e = Exam()
        if e.add(sub_code, sub_name, domain, exam_fee, exam_date, syllabus):
            return '<script>alert("Successfully Added!")</script>' + render_template('add_exam.html')
        return '<script>alert("Retry!")</script>' + render_template('add_exam.html')

    return '<script>alert("Session Expired! Retry Login..")</script>' + render_template('exam_login.html')


@app.route('/exam/remove_exam/', methods=['POST'])
def remove_exam():
    if 'username' in session and request.method == 'POST':
        sub = request.form['subject_code']
        e = Exam(sub)
        if e.remove():
            exams = get_all_exams()
            return '<script>alert("Successfully Removed")</script>' + render_template('exam_view_exams.html',
                                                                                      exams=exams)
        return '<script>alert("Retry!")</script>' + render_template('exam_view_exams.html', exams=get_all_exams())
    return '<script>alert("Session Expired! Retry Login..")</script>' + render_template('exam_login.html')


@app.route('/exam/logout/')
def exam_logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/exam/view_exams/')
def exam_view_exams():
    if 'username' in session:
        exams = get_all_exams()
        return render_template('exam_view_exams.html', exams=exams)
    return '<script>alert("Retry Login!")</script>' + render_template('exam_login.html')


@app.route('/exam/view_exam/', methods=['POST'])
def exam_view_exam():
    if 'username' in session:
        exam = Exam()
        exam.get_exam(request.form['subject_code'])
        return render_template('exam_view_exam.html', exam=exam)
    return '<script>alert("Retry Login!")</script>' + render_template('exam_login.html')


@app.route('/student/view_exam/', methods=['POST'])
def student_view_exam():
    if 'email' in session:
        exams = get_all_exams()
        for exam in exams:
            if exam.subject_code == request.form['subject_code']:
                return render_template('student_view_exam.html', exam=exam)
    return '<script>alert("Retry Login!")</script>' + render_template('exam_login.html')


@app.route('/student/view_exams/')
def student_view_exams():
    if 'email' in session:
        exams = get_all_exams()
        return render_template('student_register.html', exams=exams)
    return '<script>alert("Retry Login!")</script>' + render_template('student_login.html')


@app.route('/student/hall_ticket/')
def student_hall_ticket():
    if 'email' in session:
        email = session['email']
        password = session['password']
        s = Student()
        if s.login(email, password):
            subjects = s.registered_exams()
            file = generate_hall_ticket(email, subjects)
            return send_file(file, attachment_filename="hall_ticket.pdf")
        return redirect(url_for('student_login'))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.secret_key = "Hello World"
    app.run(host=HOST, port=PORT, debug=True)
