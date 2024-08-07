# Flask Search and PDF Generator Application

This Flask application allows users to perform a search using the SerpAPI, display the results, and generate a PDF file of the search results.

## Features

- Perform a search query using the SerpAPI.
- Display search results in a table format.
- Generate a PDF file of the search results.
- Server-side session storage using Flask-Session.

## Requirements

- Python 3.7+
- Flask
- Flask-Session
- SerpAPI
- pdfkit
- wkhtmltopdf (required by pdfkit)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Install `wkhtmltopdf`:
    - **Ubuntu**:
      ```bash
      sudo apt-get install wkhtmltopdf
      ```
    - **macOS**:
      ```bash
      brew install wkhtmltopdf
      ```
    - **Windows**:
      Download the installer from the [official site](https://wkhtmltopdf.org/downloads.html) and follow the instructions.
5. Create a .env file
    ```bash
    touch .env
    ```
## Configuration

1. Set up your SerpAPI key:
    - Sign up on [SerpAPI](https://serpapi.com/) to get your API key.
    - Replace the placeholder API key in `.env` with your actual API key:
      ```python
      SERP_API_KEY = "your_serpapi_key"
      ```

2. Configure Flask-Session in `.env`:
    ```python
    SECRET_KEY = 'your_secret_key'
    ```
3. Enter credentials for the LLM service
    ```bash
    LLM_USERNAME = "your_username"
    LLM_PASSWORD = "your_password"
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open your browser and go to `http://127.0.0.1:5000`.

3. Enter a search query and submit the form OR upload an image.

4. View the search results displayed in a table.

5. Click the "Generate PDF" button to download a PDF of the search results.

## Files

- `app.py`: Main application file containing the Flask routes and logic.
- `templates/index.html`: HTML template for the search form.
- `templates/results.html`: HTML template for displaying search results.
- `templates/pdf.html`: HTML template for generating the PDF.
- `requirements.txt`: List of required Python packages.
- `.env`: SERP API Key & Flask app secret
