from flask import Flask, request

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        
        # Save the uploaded files to a temporary directory
        uploaded_file_paths = []
        for file in files:
            file_path = "/tmp/{}".format(file.filename)
            file.save(file_path)
            uploaded_file_paths.append(file_path)

        # Process the uploaded files using your custom loader
        loader = DirectoryLoader(uploaded_file_paths, loader_cls=CSVLoader, show_progress=True)
        documents = loader.load()

        # Do something with the loaded documents

        # Clean up: Delete the temporary files
        for file_path in uploaded_file_paths:
            os.remove(file_path)

    return {"documents": documents}

if __name__ == '__main__':
    app.run(debug=True)
