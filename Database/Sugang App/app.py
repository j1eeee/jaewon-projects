import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

connect = psycopg2.connect("dbname = dbproject user = postgres password = 1234")
cur = connect.cursor()

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/register', methods = ['POST'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    button = request.form["send"]

    if button == "login":
        cur.execute("select * from info where id='{}' and pw = '{}';".format(id, password))
        result = cur.fetchall()
        if len(result) == 0:
            return "login error"
        else:
            return redirect(url_for("main_home", id= id))

    elif button == "sign up":
        cur.execute("insert into info values('{}','{}');".format(id, password))
        connect.commit()
        return f"<script>alert('Sign up success!');history.back();</script>)"

    return id + password + button

@app.route("/main_home")
def main_home():
    # get my_result course
    id = request.args.get("id")
    cur.execute("select distinct course_name, dept_name from my_result natural join course where id = '{}';".format(id))
    my_results = cur.fetchall()
    return render_template("home.html", id=id, my_results=my_results)

@app.route("/course", methods = ['GET'])
def course():
    id = request.args.get("id")
    button = request.args.get("send")
    cur.execute(f"select course_name, department.dept_name, professor.prof_name, college from course, department, professor where course.dept_name = department.dept_name and professor.prof_name = course.prof_name and course_name not in (select course_name from my_result where id ='{id}');")
    courses = cur.fetchall()

    return render_template("course.html", id=id, courses=courses)

@app.route("/course_register/<id>/<course_name>", methods = ['GET'])
def course_register(id, course_name):
    cur.execute("insert into my_result values(default, '{}', '{}');".format(course_name, id))
    connect.commit()
    return redirect(url_for("main_home", id=id))

@app.route("/course_delete/<id>/<course_name>", methods = ['GET'])
def course_delete(id, course_name):
    cur.execute(f"delete from my_result where id='{id}' and course_name='{course_name}'")
    connect.commit()
    return redirect(url_for("main_home", id=id))

@app.route("/total", methods=['GET'])
def total_course():
    id = request.args.get("id")
    cur.execute("select count(course_name) from my_result where id='{}';".format(id))
    total = cur.fetchall()
    return render_template("total.html", id=id, total=total)

@app.route("/pwchange", methods=['POST','GET'])
def pwchange():
    if request.method == 'GET':
        id = request.args.get("id")
        return render_template("pwchange.html", id=id)
    elif request.method =='POST':
        id = request.form["id"]
        password = request.form["password"]
        cur.execute(f"update info set pw='{password}' where id='{id}';")
        connect.commit()
        return redirect(url_for("main_home", id=id))

if __name__ == '__main__':
    app.run()