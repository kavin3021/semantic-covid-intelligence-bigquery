# Semantic COVID-19 Intelligence with BigQuery AI

This repository contains the end-to-end implementation of the Semantic COVID-19 Intelligence project built for the BigQuery AI Hackathon 2025. The solution demonstrates how to generate vector embeddings, run semantic vector search, generate AI summaries, and analyze results using a combination of Python and BigQuery SQL.

---

## Overview

The project pipeline consists of four major steps:

1. **Embedding Generation**  
2. **Semantic Vector Search**  
3. **AI Summary Generation**  
4. **Results Analysis**

Each step is implemented with relevant scripts or SQL queries, described in detail below.

---

## 1. Embedding Generation (Python) - `01-embedding-generation.py`

This Python script performs the following:

- Queries COVID-19 data from BigQuery.
- Uses Vertex AI's Text Embedding model (`text-embedding-004`) to generate semantic embeddings in batches.
- Saves the generated embeddings alongside unique identifiers to a JSON Lines (`embeddings.jsonl`) file.
- This JSONL file is then uploaded to a Google Cloud Storage bucket.
- The uploaded file is imported into BigQuery as the `covid_with_embeddings` table under the `intellidoc_dataset`.

### How to run

- Ensure you have your Google Cloud credentials set up locally.
- Install required libraries listed in `requirements.txt`.
- Run the script:  python 01-embedding-generation.py
- Upload the generated `embeddings.jsonl` file to your Cloud Storage bucket.
- Import the file into BigQuery to create the `covid_with_embeddings` table.

---

## 2. Semantic Vector Search (SQL) - `02-vector-search.sql`

This SQL script implements semantic similarity search using cosine similarity between the query embedding and all record embeddings:

- Accepts a query vector (embedding) as input.
- Calculates cosine similarity between the query vector and COVID record embeddings.
- Returns the top N most semantically similar records.
- Results are stored in the `semantic_search_results` table.

### How to use

- Replace the placeholder query vector in the script with your actual query embedding array.
- Run the query in BigQuery to populate/update `semantic_search_results`.

---

## 3. AI Summary Generation (SQL) - `03-ai-summary-generation.sql`

This SQL script:

- Creates the `ai_covid_summaries_from_search` table.
- Generates AI-powered natural language summaries for the top semantic search results.
- Uses BigQuery ML’s generative AI function `ML.GENERATE_TEXT` with the `gemini_pro_model`.
- Input prompts are dynamically generated based on top semantic search matches.

### How to use

- Run this query in BigQuery after `semantic_search_results` is updated.
- It will generate summaries for the most relevant COVID records found.

---

## 4. Results Analysis (SQL) - `04-results-analysis.sql`

This SQL script:

- Joins semantic search results (`semantic_search_results`) with AI-generated summaries (`ai_covid_summaries_from_search`).
- Presents a ranked list of COVID records, their similarity scores, and AI summaries.
- Supports displaying meaningful, summarized search results suitable for dashboards or reports.

### How to use

- Run this query to retrieve combined semantic and AI results.
- Use the output for further analysis, visualization, or reporting.

---

## Project Workflow Summary

graph LR
A[01-embedding-generation.py (Python)] --> B[Upload embeddings.jsonl to GCS]
B --> C[Import embeddings.jsonl into BigQuery covid_with_embeddings]
C --> D[02-vector-search.sql: Perform semantic search]
D --> E[03-ai-summary-generation.sql: Generate AI summaries]
E --> F[04-results-analysis.sql: Query combined results]


---

## Setup & Requirements

- Google Cloud Project with BigQuery & Vertex AI enabled.
- Service account with permissions for BigQuery and Cloud Storage.
- Python 3.10+ environment with dependencies (see `requirements.txt`).
- Docker (optional) for containerizing backend API.
- Basic knowledge of SQL and Python.

---

## How to Run the Entire Pipeline

1. Run `01-embedding-generation.py` to generate and export embeddings.
2. Upload `embeddings.jsonl` to Cloud Storage and import it into BigQuery as `covid_with_embeddings`.
3. Run `02-vector-search.sql` to perform semantic search and store results in `semantic_search_results`.
4. Run `03-ai-summary-generation.sql` to generate AI summaries into `ai_covid_summaries_from_search`.
5. Run `04-results-analysis.sql` to analyze and present combined results.

---

## Notes

- Adjust query vectors in `02-vector-search.sql` dynamically for runtime searches.
- You may automate the pipeline with scheduled queries or orchestrations like Cloud Composer.
- Use the API backend built separately to run live queries calling these datasets.

---

## License & Acknowledgments

This project uses public data and Google’s Vertex AI and BigQuery ML models. See LICENSE file for details.

Thanks to the BigQuery AI Team for providing advanced AI capabilities within BigQuery.

---

For questions or help, contact: [Kavindhiran] - [kavindhiran97@gmail.com]
