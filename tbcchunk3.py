import os
import re
import json
import glob
from pathlib import Path
from bs4 import BeautifulSoup

def read_file_with_fallback_encoding(file_path, encodings=['utf-8', 'ISO-8859-1', 'Windows-1252']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read {file_path} with any of the specified encodings")

def chunk_html(input_file, output_dir):
    try:
        content = read_file_with_fallback_encoding(input_file)
    except ValueError as e:
        print(f"Error reading {input_file}: {str(e)}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    base_name = Path(input_file).stem
    output_data = []

    # Find all header tags (h1 to h6)
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Handle introduction (content before first header)
    intro_content = ''
    first_header = headers[0] if headers else None

    # Use soup instead of soup.body to handle cases where there's no body tag
    for elem in soup.children:
        if elem == first_header:
            break
        if isinstance(elem, BeautifulSoup) or elem.name:
            intro_content += str(elem)

    if intro_content.strip():
        output_data.append({
            "original_filename": base_name,
            "header_text": "Introduction",
            "local_header_href": "#introduction",
            "chunk_text": intro_content.strip()
        })

    # Process other chunks
    for i, header in enumerate(headers):
        header_text = header.get_text().strip()
        header_id = header.get('id', '')

        # If no id, create one from the header text
        if not header_id:
            header_id = re.sub(r'[^\w\s-]', '', header_text.lower())
            header_id = re.sub(r'[-\s]+', '-', header_id).strip('-')

        # Get content until next header or end of document
        chunk_content = ''
        for elem in header.next_siblings:
            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                break
            if isinstance(elem, BeautifulSoup) or elem.name:
                chunk_content += str(elem)

        output_data.append({
            "original_filename": base_name,
            "header_text": header_text,
            "local_header_href": f"#{header_id}",
            "chunk_text": str(header) + chunk_content
        })

    # Save to JSON file
    output_file = os.path.join(output_dir, f"{base_name}_chunks.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

def process_all_posts(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in glob.glob(os.path.join(input_dir, '*.htm')):
        print(f"Processing {file}...")
        chunk_html(file, output_dir)

# Usage
input_directory = '/Users/jta/a/doc/revit/tbc/git/a'
output_directory = '/tmp/tbcchunk'
process_all_posts(input_directory, output_directory)
