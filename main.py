from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/addreqdan'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com', 
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'agarwal.danish.17it1066@gmail.com',
    MAIL_PASSWORD = 'Extradiction[]~'
)

mail = Mail(app)
db = SQLAlchemy(app)
class Teams(db.Model):
#sno,teamname,teamadmin,teamsize,teamCode
    sno = db.Column(db.Integer, primary_key = True)
    teamname = db.Column(db.String(80),unique = True, nullable = False)
    teamadmin = db.Column(db.String(80),unique = True, nullable = False)
    teamsize = db.Column(db.String(10),unique = True, nullable = False)
    teamCode = db.Column(db.String(80),unique = True, nullable = False)

class Request(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    teamadmin = db.Column(db.String(80),unique = True, nullable = False)
    teamname = db.Column(db.String(80),unique = True, nullable = False)
    teamsize = db.Column(db.String(10),unique = True, nullable = False)
    teamCode = db.Column(db.String(80),unique = True, nullable = False)
    useremail = db.Column(db.String(80),unique = True, nullable = False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about", methods = ['GET', 'POST'])
def about():
    teamList = db.engine.execute("SELECT * FROM teams")
    teamList = list(teamList)
    if request.method == 'POST':
        
        email = request.form.get('email')
        name = request.form.get('name')
        size = request.form.get('size')
        code = request.form.get('code')
        email2 = request.form.get('email2')
        print(teamList[int(email)-1])
        a = list(teamList[int(email)-1])
        print(a[2])
        print(email)
        print(name)
        print(size)
        print(email2)
        
#sno,teamname,teamadmin,teamsize,teamCode
        entry = Request(teamadmin = a[2], teamname = a[1],teamsize = a[3], teamCode = a[4], useremail = email2)

        db.session.add(entry)
        db.session.commit()
        mail.send_message('NEW TEAM ACCESS REQUEST', sender ='abcd@gmail.com', 
        recipients = [a[2]], 
        body = 'Hi ' + email2 + ' is requesting access for your team  ' + a[1])

    return render_template('about.html', teamList = teamList)


@app.route("/post")
def post():
    teamList = db.engine.execute("SELECT * FROM teams")
    teamList = list(teamList)
    return render_template('post.html', teamList = teamList)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        size = request.form.get('size')
        code = request.form.get('code')
#sno,teamname,teamadmin,teamsize,teamCode
        entry = Teams(teamname = name, teamadmin = email, teamsize = size, teamCode = code)
        db.session.add(entry)
        db.session.commit()


    return render_template('contact.html')
app.run(debug = True)