import pinecone
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
import uvicorn
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
app = FastAPI()


pinecone.init(api_key='ed813bf2-489b-4a03-9178-748a791f4581', environment='us-east-1-aws')

import pandas as pd
data = pd.read_csv("questions.csv")


from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')


index = pinecone.Index('question-search')


question_list = []
for i,row in data.iterrows():
  question_list.append(
      (
        str(row['id']),
        model.encode(row['question1']).tolist(),
        {
            'is_duplicate': int(row['is_duplicate']),
            'question1': row['question1']
        }
      )
  )
  if len(question_list)==50 or len(question_list)==len(data):
    index.upsert(vectors=question_list)
    question_list = []



@app.post("/predict")

def predict(query: str):
  xq = model.encode([query]).tolist()
  result = index.query(xq, top_k=4, includeMetadata=True)
  return [x['metadata']['question1'] for x in result['matches']]
