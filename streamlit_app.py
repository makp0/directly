import streamlit as st
import zipfile
import os
from io import BytesIO, StringIO

def serialize_zip(uploaded_file, metadata=None):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        file_names = zip_ref.namelist()
        serialized_content = ""
        if metadata:
            serialized_content += f"=== METADATA ===\n{metadata}\n=== METADATA ===\n"
        for file_name in file_names:
            with zip_ref.open(file_name) as file:
                try:
                    file_content = file.read().decode('utf-8')
                except UnicodeDecodeError as e:
                    st.warning(f'Error decoding file {file_name}: {e}. This file will be skipped.')
                    continue  # Skip to the next file
                serialized_content += f"--- {file_name} ---\n{file_content}\n"
        return serialized_content

def deserialize_to_zip(serialized_text):
    lines = serialized_text.split('\n')
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        filepath = ""
        content = ""
        in_metadata_section = False
        for line in lines:
            if line.startswith('=== METADATA ==='):
                in_metadata_section = not in_metadata_section
                continue  # Skip metadata lines
            if in_metadata_section:
                continue  # Skip lines inside the metadata section
            if line.startswith('--- '):
                if filepath:  # save previous file content
                    zip_ref.writestr(filepath, content)
                filepath = line.replace('--- ', '').replace(' ---', '')
                content = ""
            else:
                content += line + '\n'
        if filepath:  # save last file content
            zip_ref.writestr(filepath, content)
    zip_buffer.seek(0)
    return zip_buffer

st.set_page_config(page_title="Directly", page_icon="https://github.com/makp0/directly/blob/main/icon.png?raw=true", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title('Directly: Project Structure Generator/Serializer')

st.sidebar.header('Manual')
st.sidebar.write("""
Directly is designed to simplify the process of converting a project structure into a compressed, text format and back. This format is optimized for feeding into models like ChatGPT.

### Usage:
1. **Serialization**:
    - Select the 'Serialize' option.
    - Zip your project directory and upload the ZIP file.
    - Copy the serialized text generated in the text area below.

2. **Deserialization**:
    - Select the 'Deserialize' option.
    - Paste the serialized text into the text area below.
    - Download the resulting ZIP file containing your project structure.

### ChatGPT Interaction:
The serialized text format is ideal for interacting with OpenAI's ChatGPT. You can feed the serialized text directly to ChatGPT to discuss or review code within a conversational context.

### Format:
The serialization format is simple. Each file's content is prefixed with a line containing the file's path, enclosed in '---'. For example:

```
--- path/to/file.txt ---
File content here
```

This format ensures a clear separation between files while keeping the serialized text compact and easy to parse.
""")

option = st.radio('Choose an option', ('Deserialize', 'Serialize'))

if 'serialized_text' not in st.session_state:
    st.session_state['serialized_text'] = """\
--- src/main.py ---
print("Hello, World!")

--- README.md ---
# Sample Project
This is a sample project structure.

--- .gitignore ---
*.pyc
"""

instruction = (
    "## Instructions for ChatGPT:\n"
    "Everything should be outputed as a single txt. Each file's content is prefixed by a line with the file's path enclosed in '---', for example:\n"
    "```\n"
    "--- path/to/file1.txt ---\n"
    "File content 1 here\n"
    "--- path/to/file2.txt ---\n"
    "File content 2 here\n"
    "```\n"
    "Please respond using the same format to add, modify, or discuss the code. "
)

if option == 'Serialize':
    uploaded_file = st.file_uploader("Upload A Project Archive", type="zip")
    if uploaded_file is not None:
        include_instruction = st.checkbox("Include Instruction for ChatGPT", value=True)
        metadata = instruction if include_instruction else None
        serialized_content = serialize_zip(uploaded_file, metadata)
        st.code(serialized_content, language='markdown')
elif option == 'Deserialize':
    serialized_text = st.text_area('Paste Serialized Content Here', value=st.session_state['serialized_text'], height=400)
    st.session_state['serialized_text'] = serialized_text
    if serialized_text:
        zip_buffer = deserialize_to_zip(serialized_text)
        st.download_button(label='Download ZIP file', data=zip_buffer, file_name='output.zip')


