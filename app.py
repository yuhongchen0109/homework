from application.application import app

from flask import Flask, render_template, request, redirect, url_for
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    generated_text = response['choices'][0]['message']['content'].strip()
    return render_template('index.html', response=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
