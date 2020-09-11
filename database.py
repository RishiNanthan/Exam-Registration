import sqlite3 as sql

# Student

query1 = ''' insert into student(roll_no,password,name,email,
        phone,dept,college) values('{}','{}','{}','{}',{},'{}','{}'); '''

query2 = ''' create table if not exists student(
        roll_no varchar(15) unique not null, password varchar(50) not null, name varchar(30) not null, email varchar(30)
         primary key, phone int unique not null, dept varchar(3) not null, college varchar(50) not null ); '''

query3 = ''' select roll_no from exam_register where subject_code='{}' ; '''

query4 = ''' select roll_no,password,name,email,phone,dept,college from student where email='{}'; '''

query5 = ''' update student set password = '{}' where email='{}'; '''

# Exam

query6 = ''' create table if not exists exam( subject_code varchar(10) primary key, subject_name varchar(25) not null,
        domain varchar(30) not null, exam_fee int not null, exam_date date not null, syllabus varchar(200) );	'''

query7 = ''' insert into exam(subject_code,subject_name,domain,
        exam_fee,exam_date,syllabus) values('{}','{}','{}',{},'{}','{}'); '''

query8 = ''' select subject_name,subject_code,domain,exam_fee,exam_date,syllabus from exam ; '''

query9 = ''' select subject_name,subject_code,domain,exam_fee,exam_date,syllabus from
        exam where subject_code='{}'; '''

query10 = ''' delete from exam where subject_code='{}'; '''

# Exam_Register

query11 = ''' create table if not exists exam_register( roll_no varchar(15) not null, subject_code varchar(10) not null, 
        foreign key (roll_no) references student(roll_no) , foreign key (subject_code) references exam(subject_code) 
        ); '''

query12 = ''' insert into exam_register(roll_no,subject_code) values('{}','{}'); '''

query13 = ''' select subject_code from exam_register where roll_no='{}' ;'''

query14 = ''' delete from exam_register where roll_no='{}' and subject_code='{}';'''

# Exam_Controller

query15 = ''' create table if not exists exam_controller( username varchar(50) primary key, password varchar(50) 
        not null ); '''

query16 = ''' insert into exam_controller values('{}','{}')'''

query17 = ''' select password from exam_controller where username='{}' ;'''

query18 = ''' delete from exam_register where subject_code = '{}';'''

# DEFAULT


conn = sql.connect('ExamRegistration.db')
conn.execute(query2)
conn.execute(query6)
conn.execute(query11)
conn.execute(query15)
conn.commit()
conn.close()


# CLASSES

class Student:

    def __init__(self, roll_no=None):
        if roll_no is not None:
            con = sql.connect('ExamRegistration.db')
            cur = con.cursor()
            cur.execute("select name,dept,year from student where roll_no='{}';".format(roll_no))
            s = cur.fetchone()
            self.roll_no = roll_no
            self.name = s[0]
            self.dept = s[1]
            self.year = s[2]
            return

        self.name = self.roll_no = self.dept = self.college = self.phone = None
        self.email = self.password = None

    def login(self, email, password):
        # roll_no,password,name,email,phone,dept,year
        try:
            con = sql.connect('ExamRegistration.db')
            cur = con.cursor()
            cur.execute(query4.format(email))
            stu = cur.fetchone()
            con.close()
            if stu is None or password != stu[1]:
                return False
            self.roll_no = stu[0]
            self.password = stu[1]
            self.name = stu[2]
            self.email = stu[3]
            self.phone = stu[4]
            self.dept = stu[5]
            self.college = stu[6]

        except Exception as e:
            print("Error : database-student-login")
            print(e)
            return False

        return True

    def signup(self, roll_no, password, name, email, phone, dept, college):
        try:
            con = sql.connect('ExamRegistration.db')
            q = query1.format(roll_no, password, name, email, phone, dept, college)
            con.execute(q)
            con.commit()
            con.close()
            self.roll_no = roll_no
            self.password = password
            self.name = name
            self.email = email
            self.phone = phone
            self.dept = dept
            self.college = college

        except Exception as e:
            print("Error : database-student-signup")
            print(e)
            return False

        return True

    def change_password(self, password, new_password):
        if self.password is None:
            print("Not logged in yet")
            return False
        try:
            con = sql.connect('ExamRegistration.db')
            if self.password == password:
                q = query5.format(new_password, self.email)
                con.execute(q)
                con.commit()
                return True
            print("Old Password doesn't match!")
            return False
        except Exception as e:
            print("Error : database-student-change_password")
            print(e)
            return False

    def register(self, subject_code):
        if self.password is None:
            print("Not logged in yet")
            return False

        try:
            con = sql.connect("ExamRegistration.db")
            exams = self.registered_exams()
            for exam in exams:
                if exam.subject_code == subject_code:
                    return False
            q = query12.format(self.roll_no, subject_code)
            con.execute(q)
            con.commit()
            return True

        except Exception as e:
            print("Error : database-student-register")
            print(e)
            return False

    def registered_exams(self):
        if self.password is None:
            print("Not logged in yet")
            return False

        try:
            con = sql.connect("ExamRegistration.db")
            cur = con.cursor()
            q = query13.format(self.roll_no)
            cur.execute(q)
            e = cur.fetchall()
            con.close()
            exams = []
            for i in e:
                em = Exam()
                if em.get_exam(i[0]):
                    exams += [em]
            return exams

        except Exception as e:
            print("Error : database-student-registered_exams")
            print(e)
            return False

    def cancel_exam(self, subject_code):
        if self.password is None:
            print("Not logged in yet")
            return False

        try:
            con = sql.connect("ExamRegistration.db")
            q = query14.format(self.roll_no, subject_code)
            con.execute(q)
            con.commit()
            con.close()
            return True

        except Exception as e:
            print("Error : database-student-cancel_exam")
            print(e)
            return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Exam:
    def __init__(self, subject_code=None):
        self.subject_code = self.subject_name = self.domain = None
        self.exam_fee = self.exam_date = self.syllabus = None
        if subject_code is not None:
            self.get_exam(subject_code)

    def add(self, subject_code, subject_name, domain, exam_fee, exam_date, syllabus):
        try:
            con = sql.connect('ExamRegistration.db')
            q = query7.format(subject_code, subject_name, domain, exam_fee, exam_date, syllabus)
            con.execute(q)
            con.commit()
            con.close()
            self.subject_code = subject_code
            self.subject_name = subject_name
            self.domain = domain
            self.exam_date = exam_date
            self.exam_fee = exam_fee
            self.syllabus = syllabus

            return True

        except Exception as e:
            print("Error : database-Exam-add")
            print(e)
            return False

    def remove(self):
        try:
            con = sql.connect('ExamRegistration.db')
            q = query10.format(self.subject_code)
            q1 = query18.format(self.subject_code)
            con.execute("begin transaction")
            con.execute(q)
            con.execute(q1)
            con.commit()
            con.close()

            return True

        except Exception as e:
            print("Error : database-Exam-remove")
            print(e)
            return False

    def get_exam(self, subject_code):
        try:
            con = sql.connect('ExamRegistration.db')
            q = query9.format(subject_code)
            cur = con.cursor()
            cur.execute(q)
            e = cur.fetchone()
            con.close()
            if e is None:
                return False

            self.subject_code = e[1]
            self.subject_name = e[0]
            self.domain = e[2]
            self.exam_date = e[4]
            self.exam_fee = e[3]
            self.syllabus = e[5]

            return True

        except Exception as e:
            print("Error : database-Exam-get_exam")
            print(e)
            return False

    def registered_students(self):
        try:
            con = sql.connect('ExamRegistration.db')
            cur = con.cursor()
            q = query3.format(self.subject_code)
            cur.execute(q)
            s = cur.fetchall()
            students = []
            for i in s:
                students += [Student(i[0])]
            return students

        except Exception as e:
            print("Error : database-Exam-registered_students")
            print(e)
            return False

    def __str__(self):
        return self.subject_name

    def __repr__(self):
        return self.__str__()


class ExamController:
    def __init__(self):
        self.username = self.password = None

    def login(self, username, password):
        try:
            con = sql.connect("ExamRegistration.db")
            cur = con.cursor()
            cur.execute(query17.format(username))
            pwd = cur.fetchone()
            con.close()
            if pwd is not None and pwd[0] == password:
                self.username = username
                return True
            return False

        except Exception as e:
            print("Error : database-ExamController-login")
            print(e)
            return False

    def signup(self, username, password):
        try:
            con = sql.connect("ExamRegistration.db")
            con.execute(query16.format(username, password))
            con.commit()
            self.username = username
            return True

        except Exception as e:
            print("Error : database-ExamController-signup")
            print(e)
            return False


# FUNCTIONS

def get_all_exams():
    try:
        con = sql.connect("ExamRegistration.db")
        cur = con.cursor()
        q = "select subject_code from exam ;"
        cur.execute(q)
        e = cur.fetchall()
        exams = []
        for i in e:
            exams += [Exam(i[0])]
        return exams

    except Exception as e:
        print("Error : database-get_all_exams")
        print(e)
        return False


# TEST HERE


if __name__ == '__main__':
    pass
