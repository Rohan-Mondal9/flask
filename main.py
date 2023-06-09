

from flask import Flask, render_template , request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

import json
from flask_mail import Mail
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
    
local_server=True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
db = SQLAlchemy(app)

class Application(db.Model):
    APP_ID = db.Column(db.Integer, primary_key=True)
    FULL_NAME = db.Column(db.String(50), nullable=False)
    PASSWORD = db.Column(db.String(20), nullable=False)
    EMAIL = db.Column(db.String(50), nullable=False)
    PHONE = db.Column(db.Integer , nullable=False)
    GENDER = db.Column(db.String(1), nullable=False)
    DOB=db.Column(db.Date , nullable=False)
    LANGUAGES= db.Column(db.String(50), nullable=False)
    ADDRESS= db.Column(db.String(50), nullable=False)
    HOBBIES= db.Column(db.String(50), nullable=False)
    GUARDIANS_NAME= db.Column(db.String(50), nullable=False)
    

@app.route("/")
def index():

    return render_template('index.html',params=params)

@app.route("/jee")
def jee():
    return render_template('jee.html',params=params)

@app.route("/redirect/<id>", methods=['GET'])
def redirect(id):
    Applicatio = Application.query.filter_by(APP_ID=id).first()
    return render_template('redirect.html', params=params, Applicatio=Applicatio)

@app.route("/apply", methods = ['GET', 'POST'])
def apply():
    
    if(request.method=='POST'):
        FNAM = request.form.get('Name')
        PAS= request.form.get('Password')
        E_MAIL = request.form.get('Email')
        PHn = request.form.get('Phone')
        GEN = request.form.get('GENDER')
        DOB=request.form.get('Dob')
        la1=" " if(request.form.get('Lang1')== None) else request.form.get('Lang1')+" "
        la2=" " if(request.form.get('Lang2')== None) else request.form.get('Lang2')+" "
        la3=" " if(request.form.get('Lang3')== None) else request.form.get('Lang3')+" "
        la4=" " if(request.form.get('Lang4')== None) else request.form.get('Lang4')+" "
        LANG=la1+la2+la3+la4
        ADD= request.form.get('Address')
        HOBB= request.form.get('Hobbies')
        G_NAME= request.form.get('GName')
        entry = Application(FULL_NAME=FNAM,PASSWORD =PAS, EMAIL=E_MAIL,PHONE=PHn,GENDER =GEN,DOB=DOB,LANGUAGES=LANG, ADDRESS= ADD,HOBBIES= HOBB, GUARDIANS_NAME=G_NAME  )
        db.session.add(entry)
        db.session.commit()
    las = db.session.query(Application).order_by(desc(Application.APP_ID)).first()
    return render_template('apply.html',params=params,las=las)

@app.route("/antiragging")
def antiragging():
    return render_template('antiragging.html',params=params)

@app.route("/govtrecog")
def govtrecog():
    return render_template('govtrecog.html',params=params)

@app.route("/wbjee")
def wbjee():
    return render_template('wbjee.html',params=params)

@app.route("/Scholarship")
def Scholarship():
    return render_template('Scholarship.html',params=params)




app.run(debug=True)


