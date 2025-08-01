import os
from groq import Groq

chunk_size = 1000
client = Groq(api_key="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")

def chunk_maker(message):
    if not message:
        return
    if len(message) <= chunk_size:
        yield message
    else:
        for i in range(0, len(message), chunk_size):
            yield message[i:i + chunk_size]

def groqc(user_message):
    chat_completion = None
    chunk_response = ''
    chunk_iterator = chunk_maker(user_message)
    
    for chunk in chunk_iterator:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": chunk_response+chunk,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            chunk_response = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error sending chunk to Groq API: {e}")
            return f"Error processing message: {e}"
    
    if chunk_response:
        return chunk_response
    else:
        return "No response from AI (message might have been empty)."


# Test the function
#print(groqc("what are the max number of lines and characters that you can take as input"))
#print(groqc("a" * 5900 + "write a line about letter 'b' dont mention anything about long string before"))
print(groqc("a" * 5900 + "count number of 'a'")) 