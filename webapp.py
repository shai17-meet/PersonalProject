from flask import * 
from flask import session as login_session
from model import *

app = Flask(__name__)
app.secret_key="MY_SUPER_SECRET_KEY"

engine = create_engine('sqlite:///forum.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def verify_password(email, password):
	user= session.query(User).filter_by(email=email).first()
	if not user or not user.verify_password(password):
		return False
	else:
		return True

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		if email is None or password is None:
			flash("Missing Arguments")
			return redirect(url_for(login))
		if verify_password(email, password):
			user=session.query(User).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % user.name)
			login_session['name']=user.name
			login_session['email']=user.email
			login_session['id']=user.id
			return redirect(url_for('homepage'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newUser', methods = ['GET','POST'])
def newUser():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if name is None or email is None or password is None:
            flash("Your form is missing arguments")
            return redirect(url_for('newUser'))
        if session.query(User).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newUser'))
        user = User(name = name, email=email, password = password)
        session.add(user)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('homepage'))
    else:
        return render_template('newUser.html')


@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/newThread', methods = ['GET','POST'])
def newThread():
	if 'id' in login_session:
	    if request.method == 'POST':
	        thread_title = request.form['title']
	        thread_content = request.form['thread_content']
	        if thread_title is None or thread_content is None:
	            flash("Your form is missing arguments")
	            return redirect(url_for('newThread'))
	        thread =Thread(title = thread_title, text= thread_content, user_id=login_session['id'])
	        session.add(thread)
	        session.commit()
	        flash("Thread Added Successfully!")
	        return redirect(url_for('threads'))
	    else:
			return render_template('newThread.html')
	else:
		flash("You must log in to view this page")
		return redirect(url_for('login'))

@app.route('/threads')
def threads():
	threads=session.query(Thread).order_by(Thread.timestamp.desc()).all()
	return render_template('threads.html', threads=threads)

@app.route('/threadpage/<int:thread_id>')
def threadpage(thread_id):
	thread= session.query(Thread).filter_by(id=thread_id).one()
	return render_template('threadpage.html', thread=thread)

@app.route('/logout')
def logout():
	if 'id' not in login_session:
		flash("You must be logged in to be able to log out")
		return redirect(url_for('login'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("logged out successfully")
	return redirect(url_for('homepage'))



if __name__ == '__main__':
    app.run(debug=True)
