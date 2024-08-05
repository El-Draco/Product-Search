from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify
from flask_session import Session
import serpapi
import pdfkit
import requests
import json
from requests.auth import HTTPBasicAuth
import os
from werkzeug.utils import secure_filename
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["SECRET_KEY"] = 'radi aman riyas'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_description(img_filename):
    img = plt.imread(os.path.join('uploads', img_filename))
    encoded_img = base64.b64encode(img).decode('utf-8')
    print(encoded_img)
    payload = {
        "model": "llava3:34b",
        "prompt": "Provide a clear keyword description of the main product in this image to be used for a web search to find similar products.",
        "images": f"[{encoded_img}]"
    }
    response = requests.post(
        url="http://localhost:8000/api/generate",
        auth=HTTPBasicAuth("radi","radi"),
        data=json.dumps(payload)
    )
    return response.json().get("description", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['query']:
            query = request.form['query']
            print(query)
            if query:
                return redirect(url_for('results', query=query))
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join('uploads', filename))
                description = get_description(filename)
                return render_template('index.html', description=description)
    return render_template('index.html', description="")

@app.route('/results', methods=['GET', 'POST'])
def results():
    query = request.args.get('query')
    
    params = {
        "engine": "google",
        "google_domain": "google.ae",
        "q": query,
        "location": "Dubai,Dubai,United Arab Emirates",
        "gl": "ae",
        "cr": "countryAE",
        "api_key": "e7788240cff1f94267a8e201cf4857080e4a039fb499f4df1005f067a9e35c5b",
        "num": "10"
    }

    search = serpapi.search(params)
    result = search.as_dict()

    if 'shopping_results' in result:
        matches = result["shopping_results"]
    else:
        matches = []

    simplified_matches = [{
        "thumbnail": match.get("thumbnail"),
        "title": match.get("title"),
        "price": match.get("price"),
        "source": match.get("source"),
        "link": match.get("link")
    } for match in matches]

    session['matches'] = simplified_matches

    return render_template('results.html', matches=simplified_matches)

@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    matches = session.get('matches', [])
    rendered = render_template('pdf.html', matches=matches)
    pdf = pdfkit.from_string(rendered, False)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=search_results.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
