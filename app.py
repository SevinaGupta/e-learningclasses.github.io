from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,UserMixin,current_user
from datetime import datetime
import sqlite3
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.secret_key="nikhil@123" 
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)





class Sign(UserMixin,db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.TEXT(50))
    password = db.Column(db.TEXT())
    phone = db.Column(db.INTEGER())
    last_name=db.Column(db.TEXT(100))
    first_name=db.Column(db.TEXT(100))
    state=db.Column(db.TEXT(100))
    DOB=db.Column(db.TEXT(20))
    date=db.Column(db.TEXT(10),index = True,default=datetime.now) 
    address = db.Column(db.TEXT(100))  

@login_manager.user_loader
def user_loader(userid):
  return Sign.query.get(userid)      
  
         
  def __repr__(self):
    return self.userid
    
@app.route('/')
def home():
   return render_template('index.html')  
@app.route('/frame')
def frame():
  return render_template('frame.html')
@app.route('/courses') 
def course():  
  return render_template('courses.html')

@app.route('/setting')
def edit():
  return render_template('edit.html')
@app.route('/editsuccess',methods=['GET','POST'])   
def success():
  if request.method=='POST':
    current_user.first_name= request.form.get('fnaam')
    current_user.last_name= request.form.get('lname')
    current_user.phone= request.form.get('phoneno')
    current_user.address= request.form.get('add')
    current_user.state= request.form.get('state')
    current_user.DOB= request.form.get('dob')
    current_user.password= request.form.get('password')
    fname=current_user.first_name
    lname=current_user.last_name
    phone=current_user.phone
    add=current_user.address
    state=current_user.state
    dob=current_user.DOB
    pas=current_user.password
    sob = Sign()
    
    db.session.commit()
    flash('YOU ARE SUCCESSFULLY UPDATED YOUR PROFILE','success')
    return render_template("profile.html",fname=fname,lname=lname,state=state,dob=dob,add=add,phone=phone)
  
@app.route('/login')
def login():
  return render_template('form.html')
@login_required
@app.route('/frame',methods=['GET', 'POST'])
def form():
    if request.method=='POST':
        userid = request.form.get('UserId')
        pas = request.form.get('password')
        if userid and pas:
            user = Sign.query.filter_by(password=pas,userid=userid).first()
            if user:
              login_user(user, remember=True)
              flash('YOU ARE LOGGED IN SUCCESSFULLY','success')
              return redirect(url_for('frame'))
            else:
              flash('PLEASE ENTER VALID USERID OR PASSWORD','success')
              return redirect(url_for('login'))

            
    return render_template('index.html',title="login")
#@login_required
@app.route("/home")
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/thankyou',methods=["GET","POST"]) 
def signin():
    if request.method == 'POST':
       userid = request.form.get('userid')
       pas = request.form.get('password')
       phone = request.form.get('phoneno')
       add = request.form.get('add')
       fname=request.form.get('fname')
       lname=request.form.get('lname')
       state=request.form.get('state')
       dob=request.form.get('dob')
        # not none
       sob = Sign(first_name=fname,last_name=lname,userid=userid,password=pas,phone=phone, address=add,state=state,DOB=dob)
       db.session.add(sob)
       db.session.commit()

        
       return render_template('profile.html', phone=phone,add=add,fname=fname,lname=lname,state=state,dob=dob)


       if (userid and pas and add and fname and lname and dob):
        flash('THANKYOU FOR SIGN UP,YOU ARE SUCCESS SIGN UP!!','success')
        return render_template('index.html',fname=fname)
       else:
         flash('PLEASE FILL ALL REQUIRMENTS','danger')     
@login_required
@app.route('/profile')
def profile():
  fname=current_user.first_name
  lname = current_user.last_name
  state = current_user.state
  dob = current_user.DOB
  add = current_user.address
  phone = current_user.phone
  return render_template('profile.html',fname=fname,lname=lname,state=state,dob=dob,add=add,phone=phone)

if __name__ == '__main__':          
	app.run(debug=True)