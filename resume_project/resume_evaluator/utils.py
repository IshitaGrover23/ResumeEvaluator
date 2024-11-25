import json
import PyPDF2 as pdf
import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    def extract_text_from_pdf(self, pdf_file):
        try:
            reader = pdf.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += str(page.extract_text())
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def build_prompt(self, resume_text, job_description):
        return f"""
        Hello Act Like a very skilled or very experienced Resume Reviewer
        with a deep understanding of tech field, software engineering, data science,
        data analyst and big data engineer. Your task is to evaluate the resume
        based on the given job description. You must consider the job market is
        very competitive and you should provide best assistance for improving the
        resumes. Assign the percentage Matching based on JD and a summary of
        the resume profile and suggestions to improve the resume with high accuracy.

        resume: {resume_text}
        description: {job_description}

        I want the response in one single string having the structure
        {{"JD Match":"%","Profile Summary":"", "Suggestions":[]}}
        """

    def analyze_resume(self, pdf_file, job_description):
        try:
            resume_text = self.extract_text_from_pdf(pdf_file)
            prompt = self.build_prompt(resume_text, job_description)
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")