from flask import Flask, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
import random
import io
from flask_cors import CORS

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

def pattern_to_image(pattern, filename='pattern.png'):
    scale = 80  # Slightly reduced from 100
    size = 7 * scale
    padding = scale
    total_size = size + (2 * padding)
    
    # Create base image
    image = Image.new('RGB', (total_size, total_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add gradient background
    for y in range(total_size):
        for x in range(total_size):
            color = int(255 * (1 - y/total_size * 0.1))
            draw.point((x, y), fill=(color, color, color))
    
    # Try multiple regular (non-bold) system fonts
    font = None
    possible_fonts = [
        "C:\\Windows\\Fonts\\arial.ttf",  # Regular Arial
        "C:\\Windows\\Fonts\\consola.ttf",  # Regular Consolas
        "C:\\Windows\\Fonts\\segoeui.ttf"  # Regular Segoe UI
    ]
    
    for font_path in possible_fonts:
        try:
            font = ImageFont.truetype(font_path, scale)
            break
        except OSError:
            continue
            
    if font is None:
        font = ImageFont.load_default()
    
    # Draw pattern (without shadow)
    lines = pattern.split('\n')
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != ' ':
                x = padding + (j * scale)
                y = padding + (i * scale)
                draw.text((x, y), char, fill=(0, 0, 0), font=font)
    
    # Save high quality
    image.save(filename, 'PNG', quality=100, dpi=(600, 600))
    return image

@app.route('/')
def index():
    # Generate random pattern and display image directly
    pattern_type = random.choice(patterns_array)
    pattern = generate_pattern(pattern_type)
    image_bytes = io.BytesIO()
    pattern_image = pattern_to_image(pattern)
    pattern_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return send_file(image_bytes, mimetype='image/png')

@app.route('/<pattern_type>')
def get_pattern(pattern_type):
    try:
        pattern = generate_pattern(pattern_type)
        image_bytes = io.BytesIO()
        pattern_image = pattern_to_image(pattern)
        image_bytes.seek(0)
        return send_file(image_bytes, mimetype='image/png')
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)