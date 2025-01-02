from flask import Flask, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
import random
import io
from flask_cors import CORS
import base64
import sys

app = Flask(__name__)
CORS(app)

# Define fixed symbols array
symbols_array = ['*', '#', '@', '$', '&', '%']

# Define available patterns
patterns_array = ['X', '+', '-', '%']

def generate_pattern(target_pattern):
    size = 7
    pattern = ''
    chosen_symbol = random.choice(symbols_array)
    
    if target_pattern.upper() == 'X':
        for i in range(size):
            for j in range(size):
                if j == i or j == (size-1-i):
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
                    
    elif target_pattern.upper() == '+':
        for i in range(size):
            for j in range(size):
                if i == size//2 or j == size//2:
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
            
    elif target_pattern.upper() == '-':
        for i in range(size):
            for j in range(size):
                if i == size//2:
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
            
    elif target_pattern == '%':
        for i in range(size):
             for j in range(size):
            # Modified conditions for tighter spacing
                 if j == i or (i == 1 and j == size-2) or (i == size-2 and j == 1):
                    pattern += chosen_symbol
                 else:
                     pattern += ' '
        pattern += '\n'
    
    return pattern

def generate_random_pattern():
    size = 7
    pattern = ''
    chosen_symbol = random.choice(symbols_array)
    target_pattern = random.choice(patterns_array)
    
    if target_pattern == 'X':
        for i in range(size):
            for j in range(size):
                if j == i or j == (size-1-i):
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
    
    elif target_pattern == '+':
        for i in range(size):
            for j in range(size):
                if i == size//2 or j == size//2:
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
    
    elif target_pattern == '-':
        for i in range(size):
            for j in range(size):
                if i == size//2:
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
    
    elif target_pattern == '%':
        for i in range(size):
            for j in range(size):
                if j == i or i == 0 and j == size-1 or i == size-1 and j == 0:
                    pattern += chosen_symbol
                else:
                    pattern += ' '
            pattern += '\n'
    
    return pattern

def pattern_to_image(pattern):
    scale = 40  # Reduced for serverless
    size = 7 * scale
    padding = scale
    total_size = size + (2 * padding)
    
    image = Image.new('RGB', (total_size, total_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Use default font only
    font = ImageFont.load_default()
    
    lines = pattern.split('\n')
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != ' ':
                x = padding + (j * scale)
                y = padding + (i * scale)
                draw.text((x, y), char, fill=(0, 0, 0), font=font)
    
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'healthy'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        pattern_type = path if path else random.choice(patterns_array)
        if pattern_type.upper() not in [p.upper() for p in patterns_array]:
            return jsonify({'error': 'Invalid pattern type'}), 400
            
        pattern = generate_pattern(pattern_type)
        img_str = pattern_to_image(pattern)
        return jsonify({
            'status': 'success',
            'image': f'data:image/png;base64,{img_str}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Remove debug mode
if __name__ == '__main__':
    app = app.wsgi_app
    app.run(debug=False, port=3000)
