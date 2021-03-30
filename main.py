from flask import Flask,render_template,request,redirect,flash,json
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login,GameModel
import jsonify
 
app = Flask(__name__)
app.secret_key = 'xyz'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()
     

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/games')
@login_required
def games():
    return render_template('games.html')
 

@app.route('/add' ,methods = ['GET','POST'])
@login_required
def gamesAdd():
    if request.method == 'GET':
        return render_template('games_add.html')
 
    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        score = request.form['score']
        genre = request.form['genre']
        editors_choice=request.form['editors_choice']
        new_game = GameModel(title=title, platform=platform, score=score, genre = genre, editors_choice=editors_choice)
        db.session.add(new_game)
        db.session.commit()
        return redirect('/games')



@app.route('/update' ,methods = ['GET','POST'])
@login_required
def gamesUpdate():
    if request.method == 'GET':
        return render_template('games_update.html')
    

    if request.method == 'POST':
        gametitle =request.form['title']
        game = GameModel.query.filter_by(title=gametitle).first()
        if game:
            return render_template('games_search.html', game = game)
 
            if request.method == 'POST':
                    if request.form['title']:
                        title = request.form['title']
                    if request.form['platform']:
                        platform = request.form['platform']
                    if  request.form['score']:
                        score = request.form['score']
                    if  request.form['genre']:
                        genre = request.form['genre']
                    if request.form['editors_choice']:
                        editors_choice=request.form['editors_choice']
                    new_game = GameModel(title=title, platform=platform, score=score, genre = genre, editors_choice=editors_choice)
                    db.session.add(new_game)
                    db.session.commit()
                    return redirect('/games')





        return f"Game with title ={gametitle} Doesn't exist"




	
@app.route('/search/', methods = ['GET','POST'])
@login_required
def gamesSearch():
        if request.method == 'GET':
            return render_template('games_search.html')

        if request.method == 'POST':
            gametitle =request.form['title']
            game = GameModel.query.filter_by(title=gametitle).first()
            if game:
                flash('Game Found')
                #data={'title':game[0],'platform':game[1],'score':game[2],'genre':game[3],'editors_choice':game[4]}
                #data={}
                #data['title']=game[0]
                #data['platform']=game[1]
                #data=jsonify(game)
                #platform=GameModel.query.filter_by(title=gametitle).second()
                #score=GameModel.query.filter_by(title=gametitle).third()
                #genre=GameModel.query.filter_by(title=gametitle).fourth()
                #editors_choice=GameModel.query.filter_by(title=gametitle).fifth()
                db.session.commit()
                #return render_template('games_search.html',platform=platform,score=score,genre=genre,editors_choice=editors_choice,game=game)
                return render_template('games_search.html',game=game)

            else:
                flash("Game doesn't exist!")
                return render_template('games_search.html')
	

	
@app.route('/browse', methods = ['GET'])
@login_required
def gamesBrowse():
        game = GameModel.query.all()
        return render_template('games_browse.html',game = game,size=len(game))
	

@app.route('/delete', methods = ['GET','POST'])
@login_required
def gamesDelete():
    if request.method == 'GET':
        return render_template('games_delete.html')
    
    if request.method == 'POST':
        gametitle =request.form['title']
        game = GameModel.query.filter_by(title=gametitle).first()
        if game:
            flash('Game deleted from database')
            db.session.delete(game)
            db.session.commit()
            return render_template('games_delete.html')
        else:
            flash("Game doesn't exist!")
            return render_template('games_delete.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/games')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/games')
     
    return render_template('login.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/games')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = UserModel.query.filter_by(email=email).first()
		# if this returns a user, then the email already exists in database

        if user:
	    # if a user is found redirect back to signup page 
           flash('Email address already exists')
           return redirect('/register')

        # create new user with the form data.
        new_user = UserModel(email=email, username=username)
        new_user.set_password(password)


        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')
 
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
app.run(host='localhost', port=5000)
