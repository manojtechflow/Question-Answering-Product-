from flask import Flask, render_template, request
import os
from text_digitization import pdf_converter
from document_store import run_elastic_search
from Prediction_main import main_pipeline 
from haystack.utils import print_answers
import traceback as tr
import time

document_store=''
app = Flask(__name__)

current_path = os.getcwd()
#initializing reader
inst = main_pipeline(None,None,None)

start_time = time.time()
try:

    model_path = os.path.join(current_path,r'Models\trained_roberta')
    inst.initializing_reader(model_path)
except: 
    print(tr.format_exc())

end_time = time.time()
execution_time = end_time - start_time

print("Execution time--------------------------------:", execution_time, "seconds")



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            infer_files = os.path.join(current_path, 'infer_files')
            file_path = os.path.join(infer_files, file.filename)
            #saving file in the above directory
            file.save(os.path.join(file_path))
            #converting pdf file to txt file for fitting in pipeline and saving it in same dir
            text_file_path = pdf_converter(file_path)
            #calling return document store for getting elastic search document store
            DocumentStore = run_elastic_search()
            #calling main retriever pipeline
            inst.retriever_pipeline(DocumentStore, text_file_path)
            message = 'File uploaded successfully'
            return render_template('index.html', message=message)
    return render_template('index.html', message='')

@app.route('/infer', methods=['POST'])
def infer():
    question = request.form.get('question')
    # Perform inference or any desired processing with the question
    # Store the output in a variable
    try:
        prediction = inst.query_prediction(question)
        return render_template('index.html', question1=prediction)
    except:
        print(tr.format_exc())
        return render_template('index.html', question1="Error while prediction")

if __name__ == '__main__':
    app.run(debug=True)
