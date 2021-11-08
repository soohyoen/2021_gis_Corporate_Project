from flask import Flask, render_template, flash, redirect, url_for

from form import RegistrationForm

app = Flask(__name__ )
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

student_data = {
    1: {"name": "슈퍼맨", "score": {"국어": 90, "수학": 65}},
    2: {"name": "배트맨", "score": {"국어": 75, "영어": 80, "수학": 75}}
}

@app.route("/first")
def index():
    return render_template('index.html',
                           template_students = student_data)

@app.route("/first/student/<int:id>")
def student(id):
    return render_template("student.html",
                           template_name=student_data[id]["name"],
                           template_score=student_data[id]["score"])

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 알람 카테고리에 따라 부트스트랩에서 다른 스타일을 적용 (success, danger)
        flash(f'{form.username.data} 님 가입 완료!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/')
def home():
    return render_template('layout.html')