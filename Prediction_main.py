from haystack.nodes import FARMReader
from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor
from haystack.nodes import BM25Retriever
import traceback as tr
import os
import time

class main_pipeline:
    
    def __init__(self, retriever, reader, document_store):
        self.retriever = retriever
        self.reader = reader
        self.document_store = document_store
    
    def initializing_reader(self,model_path):
        try:
            self.reader = FARMReader(model_name_or_path=model_path, use_gpu=True)
        except:
            print("Error occured while model loading: ",tr.format_exc())
    
    def retriever_pipeline(self,DocumentStore,txt_dir):
        #assigining document_store to this instance of the class
        try:
            self.document_store = DocumentStore
            #initializing pipeline
            indexing_pipeline = Pipeline()
            text_converter = TextConverter()
            preprocessor = PreProcessor(
                clean_whitespace=True,
                clean_header_footer=True,
                clean_empty_lines=True,
                split_by="word",
                split_length=200,
                split_overlap=20,
                split_respect_sentence_boundary=True,
            )
            indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
            indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
            indexing_pipeline.add_node(component=self.document_store, name="DocumentStore", inputs=["PreProcessor"])

            #loading text file
            indexing_pipeline.run_batch(file_paths=[txt_dir])

            #laoding retriever
            self.retriever = BM25Retriever(document_store=self.document_store)
        except:
            print(tr.format_exc())

    def query_prediction(self,query):
        try:
            start_time = time.time()
            querying_pipeline = Pipeline()
            querying_pipeline.add_node(component=self.retriever, name="Retriever", inputs=["Query"])
            querying_pipeline.add_node(component=self.reader, name="Reader", inputs=["Retriever"])
            prediction = querying_pipeline.run(
                query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
            )
            ans = prediction['answers'][0]
            end_time = time.time()
            execution_time = end_time - start_time
            format_prediction = 'Query:'+str(prediction['query'])+"\n\n"+'Answer: '+str(ans.answer)+'\n\n'+'Context: '+str(ans.context)+'\n\n'+'Confidence Score: '+str(ans.score)
            print(format_prediction)
            return format_prediction
        except:
            print(tr.format_exc())
            return ""



