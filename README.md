# llm-application

This project demonstrates how to use Groq LLM for processing and summarizing large text inputs by splitting them into manageable chunks and communicating with the Groq API. It also provides simple local chat storage functionality.

## Features

- **Chunked LLM Input:** The `groqq.py` script splits long user messages into chunks and sends them sequentially to the Groq API, enabling the handling of inputs longer than the model's prompt limit.
- **Groq API Integration:** Uses the Groq Python client to interact with the Llama-3.3-70b-versatile model.
- **Local Chat Storage:** The `storage.py` script enables simple reading and writing of chat history to a local JSON file, with timestamped entries.

## Usage

### Prerequisites

- Python 3.8+
- `groq` Python package (`pip install groq`)
- A valid Groq API key

### How it Works

#### groqq.py

- **`chunk_maker(message)`**: Splits messages into 1000-character chunks.
- **`groqc(user_message)`**: Sends each chunk to the Groq API, concatenating responses for a final output. Handles long messages gracefully.

To use:
```python
from groqq import groqc

response = groqc("your very long input string here")
print(response)
```

#### storage.py

- **`r_chat()`**: Reads chat history from `chats/chat.json`.
- **`w_chat(user, text)`**: Writes a chat entry to the file, timestamped.

To use:
```python
from storage import r_chat, w_chat

w_chat("user", "Hello!")
history = r_chat()
print(history)
```

### Example

```python
# Summarize a long text using Groq LLM
from groqq import groqc
long_text = "a" * 5900 + "count number of 'a'"
print(groqc(long_text))

# Store and retrieve chat history
from storage import w_chat, r_chat
w_chat("user", "Hi there!")
print(r_chat())
```

## File Structure

```
groqq.py      # Handles chunked LLM messaging
storage.py    # Simple chat storage in JSON
chats/
  chat.json   # Stores chat messages (auto-created)
```

## Notes

- Make sure to set your Groq API key in `groqq.py`.
- The chat storage system is basic and for local use only.



## Author

[raviyashaswi](https://github.com/raviyashaswi)
