from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from flask import session
import sys
import news
import copy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/Techblog'
app.config['SECRET_KEY']='i'

db=SQLAlchemy(app)
Unamec = ""
class CreateTable(db.Model):
    __tablename__='new_user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30),nullable=False)
    username = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    article1 = db.Column(db.String(5000),nullable=True)
    article2 = db.Column(db.String(5000),nullable=True)
    article3 = db.Column(db.String(5000),nullable=True)

@app.route('/new',methods=['GET','POST'])
def new():
    if request.method=='POST':
        fname = request.form['fullname']
        uname = request.form['username']
        pwd = request.form['password']
        if fname==None or uname==None or pwd==None:
            return render_template('error.html')
        else:
            insert_data=CreateTable(fullname = fname, username = uname, password = pwd) 
            try:
                db.session.add(insert_data)
                db.session.commit()
                return redirect('/login')
            except:
                db.session.rollback()
                db.session.flush()
                return render_template('error.html')
    return render_template('newuser.html')

def copyname(name):
    Unamec=name

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['username']
        pwd=request.form['password']
        if uname!=None and pwd!=None:
            save_to_database=db.session
            luser=CreateTable.query.filter_by(username=uname).first()
            try:
                if luser.password==pwd:
                    session['logged_in']=True
                    global Unamec
                    Unamec=uname
                    return render_template('home1.html', data=Unamec)
            except Exception as e:
                return render_template('error.html')
    return render_template('login.html')

@app.route('/contribute',methods =['GET','POST'])
def contribute():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        if request.method=='POST':
            art1 = request.form['blodges']
            global Unamec
            luser=CreateTable.query.filter_by(username=Unamec).first()
            if luser.article1 == None:
                try:
                    luser.article1=art1
                    db.session.commit()
                    return render_template('home1.html', data=Unamec)
                except:
                    db.session.rollback()
                    db.session.flush()
                    return render_template('error.html')
            elif luser.article2 == None:
                try:
                    luser.article2=art1
                    db.session.commit()
                    return render_template('home1.html',data=Unamec)
                except:
                    db.session.rollback()
                    db.session.flush()
                    return render_template('error.html')
            else:
                try:
                    luser.article3=art1
                    db.session.commit()
                    return render_template('home1.html',data=Unamec)
                except:
                    db.session.rollback()
                    db.session.flush()
                    return render_template('error.html')
        return render_template('contribute.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('home.html')
    
    else:
        global Unamec
        return render_template('home1.html', data = Unamec)

@app.route('/google')
def google():
    r_url,r_title=news.Google()
    return render_template('blogspotgoogle.html',ht_url=r_url,ht_title=r_title)

@app.route('/apple')
def apple():
    r_url,r_title=news.Apple()
    return render_template('blogspotapple.html',ht_url=r_url,ht_title=r_title)

@app.route('/tesla')
def tesla():
    r_url,r_title=news.Tesla()
    return render_template('blogspottesla.html',ht_url=r_url,ht_title=r_title)

@app.route('/dash')
def dash():
    return render_template('dashboard.html', users=CreateTable.query.all() )

@app.route('/show')
def show():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        global Unamec
        return render_template('show.html',user=CreateTable.query.filter_by(username=Unamec).first())

@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    Unamec = ""
    return index()

if __name__=='__main__':
    db.create_all()
    app.run(port=8080, debug=True)