# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os

def B12(filepath):
    if not filepath.startswith('/data'):
        raise PermissionError("Access outside /data is not allowed.")
    return True

def no_delete(filepath):
    if os.path.exists(filepath):
        raise PermissionError("Deleting files is not allowed.")

# B3: Fetch Data from an API
def B3(url, save_path):
    B12(save_path)  # Security check
    no_delete(save_path)  # Prevent accidental deletion
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    B12("/data/repo")  # Ensuring it's within /data
    import subprocess
    subprocess.run(["git", "clone", repo_url, "/data/repo"], check=True)
    subprocess.run(["git", "-C", "/data/repo", "commit", "-m", commit_message], check=True)

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    B12(db_path)  # Security check
    B12(output_filename)  # Ensure output stays within /data
    no_delete(output_filename)  # Prevent accidental deletion

    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    
    with open(output_filename, 'w') as file:
        file.write(str(result))
    
    return result

# B6: Web Scraping
def B6(url, output_filename):
    B12(output_filename)  # Security check
    no_delete(output_filename)  # Prevent accidental deletion
    
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(result)

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    B12(image_path)  # Security check
    B12(output_path)  # Security check
    no_delete(output_path)  # Prevent accidental deletion
    
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

# B8: Audio Transcription
def B8(audio_path):
    import openai
    B12(audio_path)  # Security check

    with open(audio_path, 'rb') as audio_file:
        return openai.Audio.transcribe("whisper-1", audio_file)

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    B12(md_path)  # Security check
    B12(output_path)  # Security check
    no_delete(output_path)  # Prevent accidental deletion
    
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())

    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    import pandas as pd
    data = request.json
    csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']

    B12(csv_path)  # Security check
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    
    return jsonify(filtered.to_dict(orient='records'))
