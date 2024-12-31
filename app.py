from flask import Flask, redirect , render_template ,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=("sqlite:///database1.sqlite")
app.config[ "SECRET_KEY"]='this is secret'
db=SQLAlchemy(app)

class Users(db.Model,UserMixin  ):
    id=db.Column(db.Integer,  primary_key=True)
    user=db.Column(db.String(30),nullable=False)
    password=db.Column(db.String(80),nullable=False)

@app.route('/')
def home():
     return render_template('home.html')

@app.route('/signin',methods=['POST','GET']  )
def signin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
       

        hashed_password = generate_password_hash(password)
        new_user=Users(user=email,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
    return render_template('signin.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=Users.query.filter_by(user=email).first()
        if user and check_password_hash(user.password, password):
            return 'Wellcome back'
        else:
            return'invalid password or email'


    return render_template('login.html')






with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)
           