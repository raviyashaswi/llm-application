from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from groqq import groqc
from storage import w_chat,r_chat
import os


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload directory: {UPLOAD_FOLDER}")

@app.route('/chat', methods=['POST'])
def chat():
    # --- CORRECTED LINE FOR user_message ---
    # Retrieve 'tag' from request.form, not request.files
    user_message = request.form.get('tag', '').strip()
    # ----------------------------------------
    w_chat("user",user_message)
    file_content = ""
    uploaded_filename = None

    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename != '':
            try:
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                uploaded_file.save(file_path)
                uploaded_filename = filename # Store for potential use
                print(f"File '{filename}' successfully saved to {file_path}")

                # --- UNCOMMENT AND FIX THIS IF YOU NEED FILE CONTENT ---
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    #print(f"Read {len(file_content)} characters from '{filename}'.")
                except Exception as e:
                    print(f"Warning: Could not read content from file '{filename}': {e}")
                    file_content = ""
                # -----------------------------------------------------

            except Exception as e:
                print(f"Error processing file upload: {e}")
                #return jsonify({'response': f"Failed to upload file: {e}"}), 400
        else:
            print("No file selected in the file input (filename was empty).")
    else:
        print("No 'file' key found in request.files (no file uploaded).")

    
    full_input = ""
    if file_content:
        full_input += f"File Content:{file_content}\n"
    if user_message:
        full_input += f"User Message: {user_message}"

    # Fallback if both are empty
    if not full_input.strip():
        full_input = "No specific query or file content provided."
        print("Warning: Received an empty request (no message, no file content).")

    print(f"User Message (from 'tag'): '{user_message}'") # Debug print
    print(f"Full input to AI: '{full_input}'") 
    try:
        bot_response = groqc(full_input) # Uncomment and properly handle groqc call
    except Exception as e:
        print(f"Error calling groqc: {e}")
        bot_response = f"An error occurred with AI processing: {e}"
    
    print(bot_response)
    bot_response = user_message
    w_chat("bot",bot_response)
    return jsonify({'all_chat': r_chat})

if __name__ == '__main__':
    app.run(debug=True)