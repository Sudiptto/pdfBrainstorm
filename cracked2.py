from flask import Flask, render_template, request
import fitz  # PyMuPDF
import re

# Create the Flask application
app = Flask(__name__)

# Define a route and its handler
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdfFile']
    if file:
        filename = file.filename
        print(f"Received file: {filename}")

        # Extract text from the uploaded PDF file
        pdf_text = extract_text_from_pdf(file)

        # Print the text content (you can also save it, process it, etc.)
        print(pdf_text)

        # Return the text content as a response to the client
        return 'Recieved'
    else:
        return "No file was uploaded."

def extract_text_from_pdf(file):
    pdf_text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf_document:
        num_pages = pdf_document.page_count
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            text = page.get_text()

            # Remove unnecessary slashes and newlines
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\/', '', text)

            pdf_text += text.strip()

    return pdf_text

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
