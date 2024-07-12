import os
import re
import json
import glob
from pathlib import Path

def chunk_markdown(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content at all headers, including those with HTML anchors
    chunks = re.split(r'^(#{1,6}(?:<a\s+name="\d+"></a>)?\s+.+)$', content, flags=re.MULTILINE)

    base_name = Path(input_file).stem
    output_data = []

    # Handle introduction (content before first header)
    if chunks[0].strip():
        output_data.append({
            "original_filename": base_name,
            "header_text": "Introduction",
            "local_header_href": "#introduction",
            "chunk_text": chunks[0].strip()
        })

    # Process other chunks
    for i in range(1, len(chunks), 2):
        header = chunks[i].strip()
        content = chunks[i+1].strip() if i+1 < len(chunks) else ""

        # Extract header level, text, and href
        header_match = re.match(r'^(#{1,6})(?:<a\s+name="(\d+)"></a>)?\s+(.+)$', header)
        if header_match:
            header_level = len(header_match.group(1))
            anchor_id = header_match.group(2)
            header_text = header_match.group(3)

            # Use existing anchor if present, otherwise create one
            if anchor_id:
                href = f"#{anchor_id}"
            else:
                href = "#" + re.sub(r'[^\w\s-]', '', header_text.lower())
                href = re.sub(r'[-\s]+', '-', href).strip('-')

            output_data.append({
                "original_filename": base_name,
                "header_text": header_text,
                "local_header_href": href,
                "chunk_text": f"{header}\n\n{content}"
            })

    # Save to JSON file
    output_file = os.path.join(output_dir, f"{base_name}_chunks.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

def process_all_posts(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in glob.glob(os.path.join(input_dir, '*.md')):
        print(f"Processing {file}...")
        chunk_markdown(file, output_dir)

# Usage
input_directory = '/Users/jta/a/doc/revit/tbc/git/a'
output_directory = '/tmp/tbcchunk'
process_all_posts(input_directory, output_directory)
