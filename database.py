import sqlite3

DB_NAME = "educational_tool.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdfs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                filepath TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mcqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_id INTEGER,
                question TEXT,
                options TEXT,
                answer TEXT
            )
        ''')
        self.conn.commit()

    def add_pdf(self, filename, filepath):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO pdfs (filename, filepath) VALUES (?, ?)', (filename, filepath))
        self.conn.commit()

    def get_last_pdf_id(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM pdfs ORDER BY id DESC LIMIT 1')
        return cursor.fetchone()[0]

    def get_pdf(self, pdf_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM pdfs WHERE id = ?', (pdf_id,))
        return cursor.fetchone()

    def save_mcqs(self, pdf_id, mcqs):
        cursor = self.conn.cursor()
        for mcq in mcqs:
            cursor.execute('INSERT INTO mcqs (pdf_id, question, options, answer) VALUES (?, ?, ?, ?)',
                           (pdf_id, mcq['question'], str(mcq['options']), mcq['answer']))
        self.conn.commit()

    def get_progress(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT question, options, answer FROM mcqs')
        return cursor.fetchall()
