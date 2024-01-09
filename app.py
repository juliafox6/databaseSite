from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime

# инициализация приложения и базы данных
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainDB.db'
db = SQLAlchemy(app)

# инициализация менеджера авторизации
login_manager = LoginManager()
login_manager.login_view = 'login_post'
login_manager.init_app(app)


# загрузка конкретного пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# начало описания таблиц базы данных

# таблица пользователей
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    isartist = db.Column(db.Boolean, nullable=False)
    artist_specialization = db.Column(db.String(50))
    artist_exp = db.Column(db.Integer)
    customer_company = db.Column(db.String(100))
    customer_sphere = db.Column(db.String(50))
    about = db.Column(db.Text, nullable=False)


# таблица заказов
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey(User.id))
    about = db.Column(db.Text, nullable=False)


# таблица выполненных работ
class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    customer = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    about = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)


# функции рендера страниц и форм


@app.route("/")
def index():
    return render_template("index.html", current_user=current_user.is_authenticated)


@app.route("/artists.html")
def artists():
    users = User.query.filter_by(isartist=True).all()
    return render_template("artists.html", users=users, current_user=current_user.is_authenticated)


@app.route("/completes.html")
def completes():
    works = Work.query.order_by(Work.id.desc()).all()
    authors = User.query.order_by(User.id.desc()).all()
    return render_template("completes.html", works=works, authors=authors, current_user=current_user, authenticated=current_user.is_authenticated)


@app.route("/requests.html")
def requests():
    requests = Request.query.order_by(Request.id.desc()).all()
    authors = User.query.order_by(User.id.desc()).all()
    return render_template("requests.html", current_user=current_user, authenticated=current_user.is_authenticated, requests=requests, authors=authors)


@app.route("/profile.html")
@login_required
def profile():
    if current_user.isartist:
        requests = Request.query.filter_by(artist=current_user.id).all()
        works = Work.query.filter_by(artist=current_user.id).all()
    else:
        requests = Request.query.filter_by(customer=current_user.id).all()
        works = Work.query.filter_by(customer=current_user.id).all()
    
    users = User.query.order_by(User.id.desc()).all()
    
    return render_template("profile.html", current_user=current_user, requests=requests, works=works, users=users)


# публикация готовой работы
@app.route("/post_work.html", methods=['POST', 'GET'])
@login_required
def post_work():
    requests = Request.query.filter_by(artist=current_user.id).all()
    if request.method == 'POST':
        id = int(request.form['choose'])
        print(id)
        current_work = Request.query.filter_by(id=id).first()
        name = current_work.name
        date = datetime.utcnow()
        customer = current_work.customer
        artist = current_work.artist
        about = current_work.about
        url = request.form['link']
        
        new_work = Work(name=name, date=date, customer=customer, artist=artist, about=about, url=url)
        
        try:
            db.session.add(new_work)
            db.session.delete(current_work)
            db.session.commit()
            return redirect('completes.html')
        except:
            flash('Произошла ошибка при добавлении запроса')
            return redirect(url_for(post_work))
        
    return render_template("post_work.html", requests=requests)


# публикация заказа
@app.route("/post_request.html", methods=['POST', 'GET'])
@login_required
def post_request():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        about = request.form['info']
        customer = current_user.id
        
        new_request = Request(name=name, number=number, customer=customer, about=about)
        
        try:
            db.session.add(new_request)
            db.session.commit()
            return redirect('requests.html')
        except:
            flash('Произошла ошибка при добавлении запроса')
            return redirect(url_for(post_request))
        
    return render_template("post_request.html")


# форма регистрации
@app.route("/signup.html", methods=['POST', 'GET'])
def signup_post():
    if request.method == "POST":
        surname = request.form['surname']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        occupation = request.form['occupation']
        specialization = request.form['specialization']
        exp = request.form['exp']
        company = request.form['company']
        sphere = request.form['sphere']
        about = request.form['about']
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Пользователь с таким e-mail адресом уже зарегистрирован')
            return redirect(url_for('signup_post'))
    
        isartist = False
        if occupation == 'artist':
            isartist = True
        
        new_user = User(email=email, password=generate_password_hash(password), surname=surname, name=name, phone=phone, isartist=isartist, artist_specialization=specialization, artist_exp=exp, customer_company=company, customer_sphere=sphere, about=about)
    
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('login.html')
        except:
            return redirect('signup.html')
    else:
        return render_template("signup.html")
    

# форма авторизации
@app.route("/login.html", methods=['POST', 'GET'])
def login_post():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form['remember'] else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Проверьте введённые данные')
            return redirect('login.html')
        
        login_user(user, remember=remember) 
        return redirect('profile.html')
        
    else:
        return render_template("login.html")
    
    
@app.route("/requests.html/<int:id>", methods=['POST', 'GET'])
def request_detail(id):
    requestik = Request.query.get(id)
    users = User.query.order_by(User.id.desc()).all()
    
    if request.method == 'POST':
        try:
            db.session.query(Request).filter(Request.id == requestik.id).update({Request.artist: current_user.id}, synchronize_session=False)
            db.session.commit()
            return(redirect('/requests.html'))
        except:
            return(redirect('/requests.html'))
    
    return render_template("request.html", requestik=requestik, users=users, current_user=current_user, authenticated=current_user.is_authenticated)


@app.route("/completes.html/<int:id>")
def complete_detail(id):
    work = Work.query.get(id)
    users = User.query.order_by(User.id.desc()).all()
    return render_template("case.html", work=work, users=users, authenticated=current_user.is_authenticated)


@app.route("/artists.html/<int:id>")
def artist_detail(id):
    userr = User.query.get(id)
    works = Work.query.filter_by(artist=userr.id).all()
    users = User.query.order_by(User.id.desc()).all()
    return render_template("user.html", user=userr, authenticated=current_user.is_authenticated, works=works, users=users)


@app.route("/artists.html/<int:id1>/works/<int:id2>")
def artist_detail_work(id1, id2):
    users = User.query.order_by(User.id.desc()).all()
    work = Work.query.get(id2)
    return render_template("case_in_profile.html", users=users, authenticated=current_user.is_authenticated, work=work)


# функция выхода из профиля
@app.route('/logout.html')
@login_required
def logout():
    logout_user()   
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

# запуск базы
# py
# from app import app, db
# app.app_context().push()
# db.create_all()
