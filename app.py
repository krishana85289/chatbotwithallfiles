# app.py
from flask import Flask
from dotenv import load_dotenv
from file_upload_blueprint import file_upload_blueprint
from chain import qa_api_blueprint
from flask import Flask, render_template
import os
app = Flask(__name__)
load_dotenv()
os.getenv("GOOGLE_API_KEY")

app.register_blueprint(file_upload_blueprint)
app.register_blueprint(qa_api_blueprint)
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=False)
