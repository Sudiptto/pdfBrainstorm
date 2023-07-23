from flask import Flask, render_template, request
import PyPDF2
from PyPDF2 import PdfReader
import openai
from passwords import *
import re



# Create the Flask application
app = Flask(__name__)
openai.api_key = openai_key


# openai

def text_chunk(txt_prompt):
    # Generate text using the OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the model to use
        prompt=txt_prompt,
        n=1,  # Limit to a single completion
        max_tokens=2000,  # Limit the generated text to around two thousand tokens
        truncation='only',  # Truncate the input text to fit within the model's token limit
    )

    # Get the generated text from the API response
    generated_text = response.choices[0].text.strip()

    # Print the generated text
    return generated_text


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

        

        #print(len(all_text))
        total_length = len(all_text)
        print(total_length)
        print(type(all_text))

        if total_length > 10000:
            print("This is to much instead we are using the first 10,000 characters")
            new_text = all_text[:10000] # first 10,000 characters
 
            print(len(new_text))
        #print(len(reader.pages))
        #print(all_text)

       
        """txt_prompt = f'Based on this text, only generate 5 relevant questions based on the text and only print out the 5 questions based on the text: {all_text}'
        val = text_chunk(txt_prompt)
        print(val)"""

        
        return f"File '{filename}' uploaded successfully!"
        
    else:
        return "No file was uploaded."
    

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)



# THIS WORKS ONLY FOR PDFS WHERE YOU CAN COPY AND PASTE THE TEXT NOT ON PDFS WHERE YOU HAVE TO TAKE PICTURES OF THE TEXT

    
print(len('sdsds'))