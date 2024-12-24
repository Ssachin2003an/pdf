from PyPDF2 import PdfReader
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_mcqs_from_text(text):
    question_generator = pipeline("text2text-generation", model="google/t5-small-qa-qg")
    sentences = text.split('.')
    mcqs = []
    for sentence in sentences[:10]:  # Limit to 10 questions
        try:
            result = question_generator(f"generate questions: {sentence}", max_length=512, num_return_sequences=1)
            question = result[0]['generated_text']
            mcqs.append({
                "question": question,
                "options": ["Option A", "Option B", "Option C", "Option D"],  # Placeholder distractors
                "answer": "Option A"  # Placeholder correct answer
            })
        except Exception as e:
            print(f"Error generating question: {e}")
    return mcqs

def generate_mcqs_from_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return generate_mcqs_from_text(text)
