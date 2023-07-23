from flask import Flask, render_template, request
import PyPDF2
from PyPDF2 import PdfReader
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
    # Do something with the uploaded file (e.g., save it, process it, etc.)
    # For this example, we'll just print the filename and return a success message.
    if file:
        filename = file.filename
        print(f"Received file: {filename}")
        
        reader = PyPDF2.PdfReader(file) 
        # Extract text from the PDF
        all_text = ""
        #print(reader.pages)
        for page in reader.pages:
            text = page.extract_text()

            # Remove unnecessary slashes and newlines
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\/', '', text)

            all_text += text.strip()
        print(len(reader.pages))
        print(all_text)

        return f"File '{filename}' uploaded successfully!"
        
    else:
        return "No file was uploaded."
    

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)


    
