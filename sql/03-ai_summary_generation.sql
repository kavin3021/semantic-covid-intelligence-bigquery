CREATE OR REPLACE TABLE `intellidoc-hackathon-2025.intellidoc_dataset.ai_covid_summaries_from_search` AS
WITH prompts AS (
  SELECT
    CONCAT('Summarize this COVID-19 data for: ', unique_id) AS prompt,
    sr.*
  FROM
    `intellidoc-hackathon-2025.intellidoc_dataset.semantic_search_results` sr
  ORDER BY
    cosine_similarity DESC
  LIMIT 20
)
SELECT
  prompt,
  JSON_VALUE(ml_generate_text_result, '$.candidates[0].content') AS ai_summary,
  unique_id,
  cosine_similarity
FROM
  ML.GENERATE_TEXT(
    MODEL `intellidoc-hackathon-2025.intellidoc_dataset.gemini_pro_model`,
    TABLE prompts
  );
