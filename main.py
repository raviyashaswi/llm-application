from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from groqq import groqc
from storage import w_chat,r_chat
from pypdf import PdfReader
import io

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.form.get('tag', '').strip()
    file_content = ""

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename != '':
            try:
                filename = secure_filename(uploaded_file.filename)
                extension = filename.rsplit('.', 1)[1].lower()

                print(f"File '{filename}',{extension} successfully received")

                try:
                    if extension == "txt":
                        file_content = uploaded_file.read().decode('utf-8')
                    elif extension == "pdf":
                        pdf_bytes = io.BytesIO(uploaded_file.read())
                        reader = PdfReader(pdf_bytes)
                        file_content = ""
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            file_content += page.extract_text()   
                        #print(full_content)


                except Exception as e:
                    print(f"Warning: Could not read content from file '{filename}': {e}")
                    file_content = ""

            except Exception as e:
                print(f"Error processing file upload: {e}")
        else:
            print("No file selected in the file input (filename was empty).")

    
    
    full_input = ""
    if file_content:
        full_input += f"File Content:{file_content}\n\n"
    if user_message:
        full_input += f"User Message: {user_message}"

    if not full_input.strip():
        full_input = "No specific query or file content provided."
        print("Warning: Received an empty request (no message, no file content).")

    #print(f"Full input to AI: '{full_input}'") 
    try:
        
        #w_chat("user",user_message)
        bot_response = groqc(full_input)
        #w_chat("bot",bot_response)
    except Exception as e:
        print(f"Error calling groqc: {e}")
        bot_response = f"An error occurred with AI processing: {e}"
    d = jsonify({'r': bot_response})
    #print(bot_response)
    return d

if __name__ == '__main__':
    app.run(debug=True)