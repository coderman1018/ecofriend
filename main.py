from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

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
    points = db.Column(db.Integer, unique=False, nullable=True)
    m1 = db.Column(db.Boolean, unique=False, nullable=False)
    m2 = db.Column(db.Boolean, unique=False, nullable=False)
    m3 = db.Column(db.Boolean, unique=False, nullable=False)
    q1 = db.Column(db.Boolean, unique=False, nullable=False)


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
            session['points'] = myuser.points
            session['m1'], session['m2'], session[
                'm3'] = myuser.m1, myuser.m2, myuser.m3
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
                        points=0,
                        m1=False,
                        m2=False,
                        m3=False,
                        q1=False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route("/loggedin")
def loggedin():
    myuser = session.get('user', None)
    current = User.query.filter_by(username=myuser).first()
    level = current.level
    points = current.points

    return render_template("loggedin.html",
                           user=current.username,
                           level=level,
                           points=points)


@app.route('/about')
def about():
    selected = session.get('user', None)
    myuser = User.query.filter_by(username=selected).first()
    one, two, three = myuser.m1, myuser.m2, myuser.m3
    return render_template("about.html", one=one, two=two, three=three)


@app.route('/add/<int:num>')
def add(num):
    selected = session.get('user', None)
    myuser = User.query.filter_by(username=selected).first()
    if num == 1 and myuser.m1 == False:
        myuser.points += 10
        myuser.m1 = True
    elif num == 2 and myuser.m2 == False:
        myuser.points += 10
        myuser.m2 = True
    elif num == 3 and myuser.m3 == False:
        myuser.points += 10
        myuser.m3 = True
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
    #print('num here is' + num)
    selected = session.get('user', None)
    #print('user here is' + selected)
    myuser = User.query.filter_by(username=selected).first()
    #print(myuser)
    if num >= 70 and myuser.q1 == False:
        myuser.points += 10
        myuser.q1 = True
    db.session.commit()
    return redirect(url_for('loggedin'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
