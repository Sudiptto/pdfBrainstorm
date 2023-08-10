from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import PyPDF2
import re
import openai
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from passwords import *

# Create the Flask application
app = Flask(__name__)
#openai.api_key = openai_key
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


#BAM summer 2023 keys

openai.api_key = bam_key
openai.api_base = "https://bsmp2023.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"
OPENAI_MODEL = "gpt-35-turbo"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# SET UP DATABASE CLASS
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# SET UP DATABASE CLASS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# KEEP HIDDEN FOR NOW AS TO NOT USE THE OPENAI API
# KEEP HIDDEN FOR NOW, USER MR HALE KEY
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


# BAM API AI USAGE
def question_gen(txt_prompt):
  response = openai.ChatCompletion.create(
    engine=OPENAI_MODEL,
    messages=[
      {
        "role": "system",
        "content": "You are a top level PDF extractor and question creator"
      },
      {
        "role": "user",
        "content": txt_prompt
      },
    ])
  
  generated_text = response['choices'][0]['message']['content']

  questions = generated_text.split("\n") # turn the string to a list
  return questions

# Create a login

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #if username == 
        usern = User.query.filter_by(username=username).first()
        if usern:
            print("Works")
            #user = 'sd'
            #login_user(remember=True)
            #user = User.query.filter_by(username=username).first()
            if check_password_hash(usern.password, password):
                login_user(usern, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('hello'))
            else:
                flash('Right username, wrong password. Email biswassudiptto@gmail.com for a password!', category='error')
            #return redirect(url_for('hello'))
        else:
            flash("Denied: Wrong username or password. If you don't have an account, please contact biswassudiptto@gmail.com", 'error')
            #print('None')
    return render_template('login.html')

# Define a route and its handler
@app.route('/main')
@login_required
def hello():
    return render_template('main.html')

# ISSUE

@app.route('/issue')
@login_required
def issue():
    return render_template('issue.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['pdfFile']
    numb_question = request.form.get('num_questions')
    number_question = int(numb_question)
    type_question = request.form.get('education-level')
    print(type_question)
    print(number_question)
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
        #print(all_text)
        # Limit the text to 8000 characters (you can adjust this if needed)
        if len(all_text) > 8000:
            all_text = all_text[:8000]

            # KEEP HIDDEN FOR NOW NOT TO WASTE API SPACE
        if number_question > 0 and number_question < 30:
            txt_prompt = f'Based on this text, only generate {number_question} relevant questions based on the text. Make sure the difficulty of the questions are at a {type_question} level and only print out the {number_question} questions based on the text: {all_text}  '
            questions = question_gen(txt_prompt) # use chatgpt
            print(questions)
            #print(type(questions))
            # Render the questions.html template and pass the generated questions to the template
            #print(type(questions))
            #print(questions)

            #questions =  ['backyard, where various relatives of different nationalities used to celebrate holidays with lots of food and decorations.', '', '1. What fundamental changes occurred in Paterson, New Jersey on the day President Kennedy was shot? ', '2. How was President Kennedy viewed by the new immigrant inhabitants of El Building? ', '3. What was the emotional impact of the cold winter day on the narrator? ', '4. What inspired the narrator in the midst of her gloomy surroundings? ', "5. How was the narrator's view of Eugene's house different from its previous inhabitants?"]
            return render_template('questions.html', questions=questions)
        elif number_question < 1:
            return render_template('issue.html')
        elif number_question > 30:
            print("To many questions add between 1 - 10 question, subject to change as API usage increases! ")
        
    else:
        return "No file was uploaded."



# Run the app if this script is executed directly
if __name__ == '__main__':
    with app.app_context():
        # All of this code below is to add in a new user
        """username = usernamee
        password1 = password1
        new_user = User(username=username, password=generate_password_hash(password1, method = "sha256"))
        db.session.add(new_user)"""
        db.session.commit()
        db.create_all()  # Create the database tables
    #db.create_all()
    app.run(debug=True)
    
