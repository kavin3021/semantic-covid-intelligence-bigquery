import os
import pandas as pd
from google.cloud import bigquery
import vertexai
from vertexai.language_models import TextEmbeddingModel
import time

# Your GCP settings
PROJECT_ID = 'intellidoc-hackathon-2025'
LOCATION = 'us-central1'
BQ_DATASET = 'intellidoc_dataset'
BQ_TABLE = 'covid_data'

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load the latest public embedding model
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

# BigQuery client
bq_client = bigquery.Client(project=PROJECT_ID)

def query_bigquery():
    query = f"""
    SELECT
      CONCAT(Country_Region, '_', Continent, '_', WHO_Region) AS unique_id,
      *,
      CONCAT('COVID-19 data record: ', TO_JSON_STRING(t)) AS text
    FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}` t
    LIMIT 100
    """
    df = bq_client.query(query).to_dataframe()
    return df

def main():
    print("Querying data from BigQuery...")
    df = query_bigquery()

    print("Generating embeddings...")
    embeddings = []
    # Batch processing is more efficient, let's process 5 rows at a time
    BATCH_SIZE = 5
    DELAY_SECONDS = 10 
    
    for i in range(0, len(df), BATCH_SIZE):
        batch_texts = df['text'][i:i + BATCH_SIZE].tolist()
        try:
            batch_embeddings = embedding_model.get_embeddings(batch_texts)
            embeddings.extend([e.values for e in batch_embeddings])
            print(f"Processed batch {i // BATCH_SIZE + 1}...")
        except Exception as e:
            print(f"Error generating embedding for batch starting at index {i}")
            print(f"Error details: {e}")
            embeddings.extend([None] * len(batch_texts)) 
        
        time.sleep(DELAY_SECONDS)

    if len(embeddings) < len(df):
        embeddings.extend([None] * (len(df) - len(embeddings)))

    print("Saving embeddings to JSONL...")
    df['embedding'] = embeddings
    df_to_save = df[['unique_id', 'embedding']].dropna()

    # Change to JSONL format
    df_to_save.to_json('embeddings.jsonl', orient='records', lines=True)
    print("Saved embeddings.jsonl successfully.")

if __name__ == '__main__':
    main()
