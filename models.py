from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class GameModel(db.Model):
    __tablename__ ='games'
	
    title=db.Column(db.String(100))
    platform=db.Column(db.String(100))
    score=db.Column(db.Float)
    genre=db.Column(db.String(100))
    editors_choice=db.Column(db.String(100))
  

    def setEntry(self,title,platform,score,genre,editors_choice):
        self.title=title
        self.platform=platform
        self.score=score
        self.genre=genre
        self.editors_choice=editors_choice
  

    def __repr__(self):
        return f"{self.title,self.platform,self.score,self.genre,self.editors_choice}" 
 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
