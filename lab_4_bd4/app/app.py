from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin , login_user, logout_user, login_required,current_user

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime





login_manager = LoginManager() # создаем экземпляр класса LoginManager  или login_manager = LoginManager(app)

app = Flask(__name__)
application = app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/lab_4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


login_manager.init_app(app)# иниц меняем сообщение и категории по умолчанию
login_manager.login_view = 'login'
login_manager.login_message = ' для доступа к данной странице необходима авторизация'
login_manager.login_message_category = 'warning'


app.config['SECRET_KEY'] = b'\xd4\x9c6\xe5\xc7\xa5V\xbb\xbbd\xab\x8b3\xc2"d'# ключ для шифрования сессии происходит автоматически

#class Roles(db.Model):
    #name = db.Column(db.String(25), unique=True, nullable=False)
    #description = db.Column(db.String(120), unique=True, nullable=False)
    
   

    #def __repr__(self):
        #return '<User %r>' % self.username

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(25), unique=False, nullable=False)
    first_name = db.Column(db.String(25), unique=False, nullable=False)
    middle_name = db.Column(db.String(25), unique=False, nullable=False)
    data = db.Column(db.DateTime, default = datetime.utcnow) # дата пишется автоматически
    

    def __repr__(self):# способ отображение изменён ( магическая функция)
        return '<User %r>' % self.login 

class Roless(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), unique=False, nullable=False)

    #user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #  привязать таблицы одна и таже роль может быть у разных юзеров


    def __repr__(self):
        return '<User %r>' % self.role
       







class User(UserMixin):# унаследованный от UserMixin в котором реализованы необходимые атрибуты (get_id и тд) вместо отределения вручную
    def __init__(self, user_id, login, password): # переопределяем метод init принимает др параметры
        super().__init__()# вызываем метод у род класса  UserMixin
        self.id = user_id# проставл значение атрибутов id
        self.login = login# проставл значение атрибутов login
        self.password = password# проставл значение атрибутов password



@login_manager.user_loader # обработка сессии
def load_user(user_id):# принимаем идентифмкатор текущего пользователя
    try:
        admin = Users.query.filter_by(id=user_id).first()# user_id это строковая переменная!!!
        usid = admin.id# выделяем id

        if usid == int(user_id):# user_id это блин строка
        
            return User(admin.id,admin.login,admin.password_hash)# что бы вернуть пользователя нужно создать обьект класса User() и передать ему данные пользователя

    except:
        flash('ошибка чтения из базы данных','danger')
        flash('создайте базу данных , таблицу и пользователя admin','danger')

    return None        




@app.route('/')
def index():
   
    

    return render_template('index.html', delete_footer=True)





@app.route('/login' , methods=('POST','GET'))# авторизуюсь данные из базы\ все работает
def login():
    if request.method == 'POST': #если метод POST
        login = request.form.get('login')# сохраняем значение логин
        password = request.form.get('password')#сохраняем значение пароль
        remember_me = request.form.get('remember_me') == 'on'# если галочка стоит то сохраняем True
        if login and password:# если есть логин и пароль 
            admin = Users.query.filter_by(login=login).first()
            adm = admin.password_hash
            log = admin.login
            

            if login == log and check_password_hash(adm,password):


        
                
                    user_object = User(admin.id,admin.login,admin.password_hash)
                    print (user_object)
                    login_user(user_object, remember=remember_me)
                #Flask-Login предоставляет функцию login_user(). Она принимает объект пользователя. В случае успеха возвращает True и устанавливает сессию. В противном случае — False.
                    print(login_user(user_object, remember=remember_me))
                    # login_user заносит в сессию информацию о текушем пользователе поэтому Flask определяет авторизирован пользователь или нет
                    flash('вы успешно вошли','success')# вы водим сообщение с категорией 

                    next = request.args.get('next')# из параметра 'next возвращается адрес страницы откуда пришел пользователь

                    return redirect (next or url_for('index')) # перенаправляется на эту страницу  

        flash('ВВедены не верные логин или пароль','danger') #   # вы водим сообщение с категорией 

    return render_template('login.html')#



@app.route('/logout')# обработчик страницы выхода достаточно перейти на эту страницу и завершается сеанс
def logout():
    logout_user() #logout_user() во Flask-Login завершает сеанс пользователя, удаляя его идентификатор из сессии

    return redirect(url_for('index'))




@app.route('/users',methods=('POST','GET'))# читаем юзеров из базы и и перпеходим на создание или редактирование юзера
def users():
    if request.method == 'POST':
        
        print('1234')

        
        
    my_n = request.args.get('num', None)

    print(my_n)

    us=[]
    try:
        us = Users.query.all()
    except:
        flash('ошибка чтения из базы данных','danger')

    



    return render_template('users.html',users=us)    


@app.route('/new')
@login_required
def new():
    return render_template('new.html',user={}, roles='')  


@app.route('/crform', methods=('POST','GET')) # здесь правил записи пользователя
@login_required
def crform():
    my_num = request.args.get('re', None)# смотрим какого
    try:

        us_id = Users.query.filter_by(id=int(my_num)).first()# ищем его

    except:
        flash('Ошибка чтения из базы','danger')

    if request.method == 'POST':
        try:
            

            u_u=Users.query.filter_by(login=request.form['login']).first()
            u_u.login=request.form['login']
            u_u.password_hash=generate_password_hash(request.form['password'])
            u_u.last_name =request.form['last_name']
            u_u.first_name=request.form['first_name']
            u_u.middle_name =request.form['middle_name']

            db.session.commit()

            hash = generate_password_hash(request.form['password'])
            print(hash)
            #u = Users(login=request.form['login'],password_hash =hash, last_name =request.form['last_name'],first_name=request.form['first_name'],middle_name =request.form['middle_name'])
        
            #db.session.add(u)
        
            #db.session.commit()
            flash('данные добавлены в базу','success')
            
            return redirect(url_for('users'))
            
        except:

            db.session.rollback()
            flash('Ошибка добавления в базу данных','danger')
        


    return render_template('crform.html', usee=us_id) 






@app.route('/fusers',methods=('POST','GET'))# пытаюсь добавить нового юзера  работает!!!! нужно еще выбрать роль юзера и записать в отдельную таблицу
@login_required
def fusers():

    if request.method == 'POST':

        if Users.query.filter_by(login=request.form['login']).first() == None:

            try:
            
            
                hash = generate_password_hash(request.form['password'])
                print(hash)
                u = Users(login=request.form['login'],password_hash =hash, last_name =request.form['last_name'],first_name=request.form['first_name'],middle_name =request.form['middle_name'])
        
                db.session.add(u)
            #db.session.flush(u) ### Почему flush(u ошибку дает он же здесь должен быть!!!
            # добавление записи во вторую таблицу
            #p= Roless(role= =request.form['role'] , user_id = u.id  )
            #db.session.add(p)
            #db.session.flush(p)


                db.session.commit()
                flash('данные добавлены в базу','success')
            
                return redirect(url_for('users'))
            



            except:

                db.session.rollback()
                flash('Ошибка добавления в базу данных','danger')

        else:
                flash('пользователь существует','danger')
                return render_template('fusers.html')

              
    return render_template('fusers.html')




@app.route('/a')# здесь я создаю пользователя админ что бы он смог све редактировать
def indexa():




    try:


        dd=Users(login='admin', password_hash = generate_password_hash('123'), last_name ='admin',first_name ='adm',middle_name ='adm')
        db.session.flush(dd)
        db.session.add(dd)

        #uu=Roless(role ='admin',user_id=dd.id)
   
        #adm_1 = Users(login='admin', password_hash = '123', last_name ='Василий')
        #roles_1 = Roles(name='admin', description ='ad')
        #db.create_all()
        #db.session.add(roles_1)
        #db.session.flush(uu)
        #db.session.add(uu)

        
        db.session.commit()
    
        #admin = Users.query.filter_by(login='admin').first()

        return ('admin  с паролем добавлен в базу')

    except:

        db.session.rollback()
        return ('ошибка добавления в базу admin')        





@app.route('/add')# здесь я создаю таблицы( нужно две таблицы юзер и роли)
def add():


   
    db.create_all()

    return ('создаем таблицу Users')    



if __name__ == "__main__":
    app.run(debug=True)
