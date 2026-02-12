import flask
import psycopg2
from flask import render_template, request, redirect, url_for

app = flask.Flask(__name__)

# Database configuration (supports both local and Kubernetes)
import os

db_config = {
    'database': os.getenv('POSTGRES_DB', 'userdb'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432'))
}

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        return None

def init_db():
    """Initialize database table"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    gender VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")

@app.route('/')
def index():
    """Display registration form and list of users"""
    conn = get_db_connection()
    users = []
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, email, gender, created_at FROM users ORDER BY created_at DESC')
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching users: {e}")
    
    return render_template('index.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    name = request.form.get('name')
    email = request.form.get('email')
    gender = request.form.get('gender')
    
    if not all([name, email, gender]):
        return "All fields are required!", 400
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (name, email, gender) VALUES (%s, %s, %s)',
                (name, email, gender)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ User registered: {name}")
        except psycopg2.IntegrityError:
            return "Email already exists!", 400
        except Exception as e:
            return f"Error: {e}", 500
    
    return redirect(url_for('index'))

@app.route('/info')
def info():
    """Info page"""
    return render_template('info.html')

# Initialize database on module load (works in all environments)
try:
    init_db()
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")
    print("Database will be initialized on first request")
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
