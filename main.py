from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from urllib.parse import quote_plus, unquote_plus

class Item(BaseModel):
    input: str
    type: str

app = FastAPI()

@app.post("/api/encode")
def encode(item: Item):
    input_data = item.input
    encoding_type = item.type
    if not input_data:
        raise HTTPException(status_code=400, detail="No input data provided")

    if encoding_type == 'base64':
        # Convert to bytes and encode to Base64
        encoded = base64.b64encode(input_data.encode()).decode()
    elif encoding_type == 'binary':
        # Binary encode
        encoded = ' '.join(format(ord(i), '08b') for i in input_data)
    elif encoding_type == 'url':
        # URL Encode
        encoded = quote_plus(input_data)
    elif encoding_type == 'hex':
        # Hexadecimal encode
        encoded = input_data.encode().hex()
    elif encoding_type == 'morse':
        # Morse encode
        morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.',
                      'D': '-..', 'E': '.', 'F': '..-.',
                      'G': '--.', 'H': '....', 'I': '..',
                      'J': '.---', 'K': '-.-', 'L': '.-..',
                      'M': '--', 'N': '-.', 'O': '---',
                      'P': '.--.', 'Q': '--.-', 'R': '.-.',
                      'S': '...', 'T': '-', 'U': '..-',
                      'V': '...-', 'W': '.--', 'X': '-..-',
                      'Y': '-.--', 'Z': '--..', '1': '.----',
                      '2': '..---', '3': '...--', '4': '....-',
                      '5': '.....', '6': '-....', '7': '--...',
                      '8': '---..', '9': '----.', '0': '-----',
                      ', ': '--..--', '.': '.-.-.-', '?': '..--..',
                      '/': '-..-.', '-': '-....-', '(': '-.--.',
                      ')': '-.--.-', ' ': '/'}
        encoded = ' '.join(morse_code[i.upper()] for i in input_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid encoding type")

    return {'encoded': encoded}

@app.post("/api/decode")
def decode(item: Item):
    input_data = item.input
    decoding_type = item.type
    if not input_data:
        raise HTTPException(status_code=400, detail="No input data provided")

    if decoding_type == 'base64':
        # Decode from Base64
        decoded = base64.b64decode(input_data).decode()
    elif decoding_type == 'binary':
        # Binary decode
        decoded = ''.join([chr(int(i, 2)) for i in input_data.split()])
    elif decoding_type == 'url':
        # URL Decode
        decoded = unquote_plus(input_data)
    elif decoding_type == 'hex':
        # Hexadecimal decode
        decoded = bytes.fromhex(input_data).decode()
    elif decoding_type == 'morse':
        # Morse decode
        morse_code = {'.-': 'A', '-...': 'B', '-.-.': 'C',
                      '-..': 'D', '.': 'E', '..-.': 'F',
                      '--.': 'G', '....': 'H', '..': 'I',
                      '.---': 'J', '-.-': 'K', '.-..': 'L',
                      '--': 'M', '-.': 'N', '---': 'O',
                      '.--.': 'P', '--.-': 'Q', '.-.': 'R',
                      '...': 'S', '-': 'T', '..-': 'U',
                      '...-': 'V', '.--': 'W', '-..-': 'X',
                      '-.--': 'Y', '--..': 'Z', '.----': '1',
                      '..---': '2', '...--': '3', '....-': '4',
                      '.....': '5', '-....': '6', '--...': '7',
                      '---..': '8', '----.': '9', '-----': '0',
                      '--..--': ',', '.-.-.-': '.', '..--..': '?',
                      '-..-.': '/', '-....-': '-', '-.--.': '(',
                      '-.--.-': ')', '/': ' '}
        decoded = ''.join(morse_code[i] for i in input_data.split())
    else:
        raise HTTPException(status_code=400, detail="Invalid decoding type")

    return {'decoded': decoded}
