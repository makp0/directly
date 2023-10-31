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

st.title('Project Structure Generator/Serializer')

option = st.radio('Choose an option', ('Serialize', 'Deserialize'))

if option == 'Serialize':
    uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")
    if uploaded_file is not None:
        serialized_content = serialize_zip(uploaded_file)
        st.text_area('Serialized Content', value=serialized_content, height=400)
elif option == 'Deserialize':
    serialized_text = st.text_area('Paste Serialized Content Here', height=400)
    if serialized_text:
        zip_buffer = deserialize_to_zip(serialized_text)
        st.download_button(label='Download ZIP file', data=zip_buffer, file_name='output.zip')

if __name__ == '__main__':
    st.run()
