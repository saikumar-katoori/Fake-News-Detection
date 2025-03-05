from flask import Flask, render_template, request
import google.generativeai as genai
import easyocr
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Google Gemini API key and setup
GOOGLE_API_KEY = "AIzaSyBht2cqljIEqxARV4h_IZI0PHBBZ8rlF0Y"
genai.configure(api_key=GOOGLE_API_KEY)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_with_easyocr(image_path):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image_path)
    text = " ".join([item[1] for item in result])
    return text

def check_news_accuracy(news_text):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Analyze the credibility of the following news article. 
    Provide an accuracy score (0-100%) and determine if it's real or fake based on known sources.
    Consider the major and trusted news sources like WHO, PubMed, uptodate, medscape, national health institutions etc when making your decision.
    Also mention from which source you have taken the information (Only very much trusted source).
    News: {news_text}

    Response format:
    - News accuracy Score: XX%
    - Verdict: Real or Fake
    - Explanation: (Why is it real/fake?)
    - Source: (Which source did you use to verify the information? only mention the website name, dont provide the link)
    """

    response = model.generate_content(prompt)
    return response.text

@app.route("/", methods=["GET", "POST"])
def home():
    news_result = None
    if request.method == "POST":
        news_text = request.form.get('news_text', '').strip()
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            news_text = extract_text_with_easyocr(filepath)
            os.remove(filepath)  # Remove the file after processing
        elif not news_text:
            return render_template('index.html', error="Please enter news text or upload a valid image file.")

        if news_text:
            result = check_news_accuracy(news_text)
            news_result = result.split("\n")

    return render_template('index.html', news_result=news_result)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
