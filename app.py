from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from mcq_generator import generate_mcqs_from_pdf
from web_scraper import scrape_supplementary_data
from database import Database

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = Database()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded!", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file!", 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            db.add_pdf(filename, filepath)
            return redirect(url_for('generate_mcqs', pdf_id=db.get_last_pdf_id()))
    return render_template('upload.html')

@app.route('/generate/<int:pdf_id>')
def generate_mcqs(pdf_id):
    pdf_info = db.get_pdf(pdf_id)
    if not pdf_info:
        return "PDF not found!", 404
    mcqs = generate_mcqs_from_pdf(pdf_info['filepath'])
    supplementary_data = scrape_supplementary_data(pdf_info['filename'])
    db.save_mcqs(pdf_id, mcqs)
    return render_template('questions.html', mcqs=mcqs, supplementary_data=supplementary_data)

@app.route('/progress')
def progress():
    progress_data = db.get_progress()
    return render_template('progress.html', progress=progress_data)

if __name__ == '__main__':
    app.run(debug=True)
