from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask_session import Session
import serpapi
import pdfkit
import requests
import json
from requests.auth import HTTPBasicAuth
import os
from werkzeug.utils import secure_filename
import base64
import cv2
import base64
from dotenv import load_dotenv

load_dotenv()

# Get credentials from environment variables
SERP_API_KEY = os.getenv('SERP_API_KEY')
LLM_USERNAME = os.getenv('LLM_USERNAME')
LLM_PASSWORD = os.getenv('LLM_PASSWORD')

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
@TODO
1. add cart
2. add quantity
3. navigation
4. select/deselect specific items
5. improve ui
6. package to docker

"""

def get_description(img_filename):
    img = cv2.imread(os.path.join('uploads', img_filename))
    jpg_img = cv2.imencode('.jpg', img)
    b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
    payload = {
        "model": "llava:34b",
        "prompt": "You're an interior design specialist. You're provided an image of an interior design item and you're required to describe it using clear keywords that include the item type, shape, color shade,\
              material, etc... Your output should be sufficient to find the exact item when performing google shopping search. OUTPUT ONLY KEYWORDS. ",
        "images": [f"{b64_string}"],
        "stream": False
    }
    response = requests.post(
        url="http://localhost:8000/api/generate",
        auth=HTTPBasicAuth(LLM_USERNAME,LLM_PASSWORD),
        data=json.dumps(payload)
    )
    print(response.content)
    return response.json()["response"]

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
        "api_key": f"{SERP_API_KEY}",
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
