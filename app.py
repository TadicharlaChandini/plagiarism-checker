import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import difflib
from difflib import SequenceMatcher
import re

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'py', 'java', 'c', 'cpp', 'js', 'html', 'css'}

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create required folders
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('stored_docs'):
    os.makedirs('stored_docs')

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create uploads table
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            uploaded_file TEXT,
            comparison_file TEXT,
            similarity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from file
def extract_text_from_file(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    text = ''
    if ext == 'txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    elif ext == 'pdf':
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif ext == 'docx':
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text
    elif ext in ['py', 'java', 'c', 'cpp', 'js', 'html', 'css']:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    return text

# Tokenize code
def tokenize_code(content):
    content = re.sub(r'(?m)#.*$', '', content)
    content = re.sub(r'(?m)//.*$', '', content)
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    tokens = re.findall(r'\b\w+\b|[^\s\w]', content)
    return ' '.join(tokens)

# Check plagiarism
def check_plagiarism(content, stored_folder='stored_docs'):
    results = []
    tokenized_content = tokenize_code(content)

    for fname in os.listdir(stored_folder):
        fpath = os.path.join(stored_folder, fname)
        if os.path.isfile(fpath) and allowed_file(fname):
            stored_text = extract_text_from_file(fpath)
            stored_tokens = tokenize_code(stored_text)
            similarity = SequenceMatcher(None, tokenized_content, stored_tokens).ratio()
            results.append((fname, round(similarity * 100, 2)))

    return sorted(results, key=lambda x: x[1], reverse=True)

# Home
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return 'Username already exists.'
        finally:
            conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))


    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

# Upload Route
@app.route('/upload', methods=['GET', 'POST'], endpoint='upload')
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('upload.html')

    # Only runs if POST
    main_file = request.files.get('file')
    if not main_file or main_file.filename == '' or not allowed_file(main_file.filename):
        return "Invalid main file type."

    main_filename = secure_filename(main_file.filename)
    main_filepath = os.path.join(app.config['UPLOAD_FOLDER'], main_filename)
    main_file.save(main_filepath)
    main_text = extract_text_from_file(main_filepath)
    filetype = main_filename.rsplit('.', 1)[1].lower()

    stored_path = os.path.join('stored_docs', main_filename)
    with open(stored_path, 'w', encoding='utf-8') as f:
        f.write(main_text)

    compare_file = request.files.get('compare_file')
    compare_text = None
    compare_filename = None
    similarity = None
    diff_html = None

    if compare_file and compare_file.filename != '' and allowed_file(compare_file.filename):
        compare_filename = secure_filename(compare_file.filename)
        compare_filepath = os.path.join(app.config['UPLOAD_FOLDER'], compare_filename)
        compare_file.save(compare_filepath)
        compare_text = extract_text_from_file(compare_filepath)

        token1 = tokenize_code(main_text)
        token2 = tokenize_code(compare_text)
        similarity = round(SequenceMatcher(None, token1, token2).ratio() * 100, 2)

        token_lines1 = token1.split()
        token_lines2 = token2.split()

        diff_html = difflib.HtmlDiff().make_table(
            token_lines1,
            token_lines2,
            fromdesc=main_filename,
            todesc=compare_filename,
            context=True,
            numlines=2
        )

    results = check_plagiarism(main_text)

    user_id = session.get('user_id')
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO uploads (user_id, uploaded_file, comparison_file, similarity) VALUES (?, ?, ?, ?)',
        (user_id, main_filename, compare_filename, similarity)
    )
    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        filename=main_filename,
        text=main_text,
        compare_filename=compare_filename,
        compare_text=compare_text,
        similarity=similarity,
        results=results,
        filetype=filetype,
        diff_html=diff_html
    )
# View upload history
@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('history.html')
    conn = get_db_connection()
    uploads = conn.execute('SELECT * FROM uploads WHERE user_id = ? ORDER BY id DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', uploads=uploads)

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

