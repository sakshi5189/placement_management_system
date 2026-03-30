from flask import Flask, render_template, request, redirect, session
from db import conn, cursor

app = Flask(__name__)
app.secret_key = "secret123"


# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            cursor.execute(
                "INSERT INTO users (name,email,password) VALUES (?,?,?)",
                (name, email, password)
            )
            conn.commit()
            return redirect('/login')
        except:
            return "Email already exists!"

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = user[2]
            return redirect('/')
        else:
            return "Invalid Login"

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# HOME
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')


# ADD STUDENT
@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        cgpa = request.form['cgpa']
        skill = request.form['skill']

        cursor.execute(
            "INSERT INTO students (name,cgpa,skill) VALUES (?,?,?)",
            (name, cgpa, skill)
        )
        conn.commit()
        return redirect('/')

    return render_template('add_student.html')


# ADD COMPANY
@app.route('/add_company', methods=['GET','POST'])
def add_company():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        cgpa = request.form['cgpa']
        skill = request.form['skill']

        cursor.execute(
            "INSERT INTO companies (name,min_cgpa,skill) VALUES (?,?,?)",
            (name, cgpa, skill)
        )
        conn.commit()
        return redirect('/')

    return render_template('add_company.html')


# ELIGIBLE
@app.route('/eligible')
def eligible():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    data = []
    for c in companies:
        cursor.execute(
            "SELECT * FROM students WHERE cgpa >= ? AND skill=?",
            (c[2], c[3])
        )
        students = cursor.fetchall()

        data.append({'company': c[1], 'students': students})

    return render_template('eligible.html', data=data)


# PREDICTION
@app.route('/predict')
def predict():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    results = []
    for s in students:
        if s[2] > 8:
            chance = "High"
        elif s[2] >= 6:
            chance = "Medium"
        else:
            chance = "Low"

        results.append({
            'id': s[0],
            'name': s[1],
            'chance': chance
        })

    return render_template('predict.html', results=results)


# DELETE STUDENT
@app.route('/delete_student/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    return redirect('/eligible')


if __name__ == '__main__':
    app.run()