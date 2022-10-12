from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ecofriend-123"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecofriend.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(10), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, nullable=True)
    totalpoints = db.Column(db.Integer, unique=False, nullable=True)
    missionscompleted = db.Column(db.String(250), unique=False, nullable=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        selected = request.form["username"]
        myuser = User.query.filter_by(username=selected).first()

        if myuser:
            session['user'] = myuser.username
            session['level'] = myuser.level
            session['points'] = myuser.totalpoints

            missionscompleted = myuser.missionscompleted
            if "m01" in missionscompleted:
                session['m1'] = True
            if "m02" in missionscompleted:
                session['m2'] = True
            if "m03" in missionscompleted:
                session['m3'] = True
            if "q01" in missionscompleted:
                session['q1'] = True

            return redirect(url_for("loggedin"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        new_user = User(username=request.form["username"],
                        password=request.form["password"],
                        email=request.form["email"],
                        country=request.form["country"],
                        level=1,
                        totalpoints=0,
                        missionscompleted='')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route("/loggedin")
def loggedin():
    current = User.query.filter_by(username=session.get('user', None)).first()
    return render_template("loggedin.html",
                           user=current.username,
                           level=current.level,
                           totalpoints=current.totalpoints)


@app.route('/about')
def about():
    selected = session.get('user', None)
    myuser = User.query.filter_by(username=selected).first()

    current_month = datetime.now().strftime('%m')
    current_year = datetime.now().strftime('%y')

    monyr = current_month + current_year
    mission1 = "m01" + monyr
    mission2 = "m02" + monyr
    mission3 = "m03" + monyr

    one, two, three = False, False, False

    missionscompleted = myuser.missionscompleted
    if mission1 in missionscompleted:
        one = True
    if mission2 in missionscompleted:
        two = True
    if mission3 in missionscompleted:
        three = True

    return render_template("about.html", one=one, two=two, three=three)


@app.route('/add/<int:num>')
def add(num):
    selected = session.get('user', None)
    myuser = User.query.filter_by(username=selected).first()

    missionscompleted = myuser.missionscompleted

    current_month = datetime.now().strftime('%m')
    current_year = datetime.now().strftime('%y')

    monyr = current_month + current_year
    mission = "m0" + str(num) + monyr

    if mission not in missionscompleted:
        myuser.totalpoints += 10
        myuser.missionscompleted += mission

    db.session.commit()
    return redirect(url_for('about'))


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/news')
def news():
    return render_template("news.html")


@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")


@app.route('/service')
def service():
    return render_template("service.html")


@app.route('/quiz_add/<int:num>')
def quiz_add(num):
    selected = session.get('user', None)
    myuser = User.query.filter_by(username=selected).first()

    missionscompleted = myuser.missionscompleted

    current_month = datetime.now().strftime('%m')
    current_year = datetime.now().strftime('%y')

    monyr = current_month + current_year
    quiz = "q0" + str(num) + monyr

    if quiz not in missionscompleted:
        myuser.totalpoints += 10
        myuser.missionscompleted += quiz

    db.session.commit()

    return redirect(url_for('loggedin'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
