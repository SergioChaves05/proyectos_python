import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_super_secreta' # Necesario para las sesiones
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# --- CONFIGURACIÓN FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Si no estás logueado, te manda aquí

DB_NAME = "twitter.db"

# --- CLASE USUARIO (Para Flask-Login) ---
class User(UserMixin):
    def __init__(self, id, username, profile_pic):
        self.id = id
        self.username = username
        self.profile_pic = profile_pic

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['profile_pic'])
    return None

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- INICIALIZAR BBDD (AHORA CON 2 TABLAS) ---
def init_db():
    conn = get_db_connection()
    # Tabla Usuarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_pic TEXT
        )
    ''')
    # Tabla Tweets (Con Foreign Key que apunta al usuario)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- RUTAS ---

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    # JOIN MÁGICO: Unimos tabla tweets con users para saber el nombre y foto del autor
    query = '''
        SELECT tweets.id, tweets.texto, tweets.fecha, tweets.user_id, users.username, users.profile_pic 
        FROM tweets 
        JOIN users ON tweets.user_id = users.id 
        ORDER BY tweets.id DESC
    '''
    tweets = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', tweets=tweets)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Gestión de Foto
        file = request.files['foto']
        filename = 'default.png' # Foto por defecto
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Encriptar contraseña (HASHING)
        pass_hash = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password, profile_pic) VALUES (?, ?, ?)',
                         (username, pass_hash, filename))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            flash("Ese usuario ya existe")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        # Verificamos si existe y si la contraseña coincide con el Hash
        if user and check_password_hash(user['password'], password):
            usuario_obj = User(user['id'], user['username'], user['profile_pic'])
            login_user(usuario_obj)
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    texto = request.form['texto']
    if texto:
        conn = get_db_connection()
        # Insertamos usando el ID del usuario logueado (current_user.id)
        conn.execute('INSERT INTO tweets (user_id, texto) VALUES (?, ?)', 
                     (current_user.id, texto))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:tweet_id>')
@login_required
def delete(tweet_id):
    conn = get_db_connection()
    # Solo borramos si el tweet pertenece al usuario actual
    conn.execute('DELETE FROM tweets WHERE id = ? AND user_id = ?', (tweet_id, current_user.id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)