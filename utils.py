from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
import sqlite3

def create_pdf(content, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    story = []
    
    title_style = styles['Title']
    if 'diet' in filename.lower():
        title = "Personalized Diet Plan"
    else:
        title = "Personalized Workout Plan"
    story.append(Paragraph(title, title_style))
    story.append(Paragraph("<br/><br/>", styles['Normal']))
    
    paragraphs = content.split('\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para, styles['Normal']))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def validate_username(username):
    """Validate username: 3-20 characters, alphanumeric"""
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def validate_password(password):
    """Validate password: 
    - At least 8 characters
    - Contains at least one uppercase, one lowercase, one number
    """
    return (len(password) >= 8 and 
            re.search(r'[A-Z]', password) and 
            re.search(r'[a-z]', password) and 
            re.search(r'\d', password))

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()

def insert_user(username, password):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def verify_user(username, password):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_history(user_id, action):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (user_id, action) VALUES (?, ?)', (user_id, action))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT action, timestamp FROM history WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    history = c.fetchall()
    conn.close()
    return history