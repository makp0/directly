import streamlit as st
import zipfile
import os

def process_input_file(input_file):
    lines = input_file.getvalue().decode().split('\n')
    zipf = zipfile.ZipFile('output.zip', 'w')
    filepath = ""
    for line in lines:
        if line.startswith('--- '):
            filepath = line.replace('--- ', '')
            if not filepath.endswith('/'):  # directory
                zipf.writestr(filepath, "")
            else:  # file
                zipf.writestr(filepath, "")
        else:
            zipf.writestr(filepath, line + '\n')
    zipf.close()
    return 'output.zip'

st.title('Project Structure Generator')

uploaded_file = st.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    output_file_path = process_input_file(uploaded_file)
    if output_file_path:
        st.write('Download your zipped project structure:')
        st.markdown(f'<a href="{output_file_path}" download>Click here to download</a>', unsafe_allow_html=True)
