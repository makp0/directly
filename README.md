# Directly [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://directly.streamlit.app)
![Directly Icon](icon.png)

Directly is a Streamlit app designed to streamline the process of serializing and deserializing project structures. It compresses a project structure into a single text file, or expands the text file back to a zipped project structure, making it easy to convert projects into a format feedable to ChatGPT.

## Unique Value

- **ChatGPT Ready**: Directly compresses project structures into a concise text format, making it easy to input into models like ChatGPT for conversation-based code reviews or discussions.
- **Bi-directional Conversion**: Easily toggle between a serialized text file and a zipped project structure with a user-friendly interface.

## Features

- **Serialize**: Convert a zipped project structure into a single formatted text file.
- **Deserialize**: Convert a formatted text file back into a zipped project structure.

## Usage

1. Launch the Directly app by visiting [https://directly.streamlit.app](https://directly.streamlit.app).
2. Choose between `Serialize` and `Deserialize` options.
3. For Serialization:
   - Upload a ZIP file containing your project structure.
   - Copy the generated formatted text.
4. For Deserialization:
   - Paste the formatted text into the text area.
   - Download the generated ZIP file containing your project structure.

## Installation

Before running Directly, you need to have Streamlit installed on your machine. Follow these steps to install Streamlit:

1. Ensure you have Python 3.6 - 3.8 installed on your machine. You can download Python from [here](https://www.python.org/downloads/).
2. Install Streamlit using pip:

```bash
pip install streamlit
```

## Development

Clone the repository:

```bash
git clone https://github.com/yourusername/directly.git
cd directly
```

Run the app locally:

```bash
streamlit run app.py
```

## License

[MIT License](LICENSE)
