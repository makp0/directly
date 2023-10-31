import streamlit as st
import zipfile
import os
from io import BytesIO, StringIO

def serialize_zip(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        file_names = zip_ref.namelist()
        serialized_content = ""
        for file_name in file_names:
            with zip_ref.open(file_name) as file:
                file_content = file.read().decode()
                serialized_content += f"--- {file_name} ---\n{file_content}\n"
        return serialized_content

def deserialize_to_zip(serialized_text):
    lines = serialized_text.split('\n')
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        filepath = ""
        content = ""
        for line in lines:
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

option = st.radio('Choose an option', ('Serialize', 'Deserialize'))

if option == 'Serialize':
    uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")
    if uploaded_file is not None:
        serialized_content = serialize_zip(uploaded_file)
        st.text_area('Serialized Content', value=serialized_content, height=400, key='serialized_content')
        st.button('Select Text', on_click=lambda: st.session_state['serialized_content'].select_all())
elif option == 'Deserialize':
    serialized_text = st.text_area('Paste Serialized Content Here', height=400)
    if serialized_text:
        zip_buffer = deserialize_to_zip(serialized_text)
        st.download_button(label='Download ZIP file', data=zip_buffer, file_name='output.zip')
