from flask import Flask, render_template, request
import PyPDF2
import re
import openai
from passwords import *

# Create the Flask application
app = Flask(__name__)
openai.api_key = openai_key


# openai


# KEEP HIDDEN FOR NOW AS TO NOT USE THE OPENAI API
"""def text_chunk(txt_prompt):
    # Generate text using the OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the model to use
        prompt=txt_prompt,
        n=1,  # Limit to a single completion
        max_tokens=200,  # Limit the generated text to around 200 tokens (AI LIMIT)
    )

    # Get the generated text from the API response
    generated_text = response.choices[0].text.strip()

    # Split the generated text into individual questions (you need to adjust this part based on the actual response format)
    questions = generated_text.split("\n")

    return questions"""

# Create a login

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')

# Define a route and its handler
@app.route('/')
def hello():
    return render_template('main.html')

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
        for page in reader.pages:
            text = page.extract_text()

            # Remove unnecessary slashes and newlines
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\/', '', text)

            all_text += text.strip()
        print(all_text)
        # Limit the text to 8000 characters (you can adjust this if needed)
        if len(all_text) > 8000:
            all_text = all_text[:8000]

            # KEEP HIDDEN FOR NOW NOT TO WASTE API SPACE

        """txt_prompt = f'Based on this text, only generate 5 relevant questions based on the text and only print out the 5 questions based on the text: {all_text}'
        questions = text_chunk(txt_prompt)"""

        # Render the questions.html template and pass the generated questions to the template
        #print(type(questions))
        #print(questions)

        questions =  ['backyard, where various relatives of different nationalities used to celebrate holidays with lots of food and decorations.', '', '1. What fundamental changes occurred in Paterson, New Jersey on the day President Kennedy was shot? ', '2. How was President Kennedy viewed by the new immigrant inhabitants of El Building? ', '3. What was the emotional impact of the cold winter day on the narrator? ', '4. What inspired the narrator in the midst of her gloomy surroundings? ', "5. How was the narrator's view of Eugene's house different from its previous inhabitants?"]
        return render_template('questions.html', questions=questions)
        
    else:
        return "No file was uploaded."


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
