from flask import Flask , render_template , request
from src.helper import download_hugging_face_embeddingd
from langchain.vectorstores import Pinecone  
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

api_key = os.environ.get('PINECONE_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

embeddings = download_hugging_face_embeddingd()

serverless =os.environ.get('SERVERLESS') or True

from pinecone import Pinecone
api_key = os.environ.get('PINECONE_API_KEY') or PINECONE_API_KEY
pc = Pinecone(api_key = PINECONE_API_KEY)

from pinecone import ServerlessSpec, PodSpec

if serverless:
    spec = ServerlessSpec(cloud="aws" , region="us-east-1")
    
else:
    spec = PodSpec(environment="us-east-1")

index_name = 'medicalchat'

import time

existing_indexes =[
    index_info["name"] for index_info in pc.list_indexes()
]
if index_name not in existing_indexes:
    pc.create_index(
        index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 
    
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
        
index =pc.Index(index_name)
time.sleep(1)

index.describe_index_stats()

{
    'dimension': 384 ,
    'index_fullness' :0.0,
    'namespaces' :{'':{'vector_count':7020}},
    'total_vector_count' :7020
}

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens':512,
                            'temperature':0.8})


docsearch = PineconeVectorStore.from_existing_index(index_name,embeddings)

from langchain.chains import RetrievalQA
from langchain_core.callbacks.manager import AsyncCallbackManagerForChainRun
from typing import *

class RetrievalQASourceDocument(RetrievalQA):
    def __init__(self, llm, chain_type="stuff", retriever=None, **kwargs):
        super().__init__(llm=llm, chain_type=chain_type, retriever=retriever, **kwargs)

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional[AsyncCallbackManagerForChainRun] = None) -> Dict[str, Any]:
        query = inputs["query"]
        _run_manager = run_manager or AsyncCallbackManagerForChainRun.get_noop_manager()
        
        # Get relevant documents
        retriever_results = await self.retriever.aget_relevant_documents(query, _run_manager.get_child())
        
        # Create result dictionary
        result = {
            "result": query,
            "source_documents": retriever_results
        }
        
        return result
    
#If any Error occured remove the above code of class RetrievalQASourceDocument(RetrievalQA)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    # return_source_document=True,
    chain_type_kwargs=chain_type_kwargs
    )

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])




if __name__ == '__main__':
    app.run(host="0.0.0.0" , port=5000 ,debug=True)

    
    
