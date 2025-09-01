CREATE OR REPLACE TABLE `intellidoc-hackathon-2025.intellidoc_dataset.ai_covid_summaries` AS
WITH prompts AS (
  SELECT
    CONCAT('Summarize this COVID-19 data record: ', TO_JSON_STRING(t)) AS prompt,
    *
  FROM
    `intellidoc-hackathon-2025.intellidoc_dataset.covid_data` t
  LIMIT 20
)
SELECT
  prompt,
  JSON_VALUE(ml_generate_text_result, '$.candidates[0].content') AS ai_summary
FROM
  ML.GENERATE_TEXT(
    MODEL `intellidoc-hackathon-2025.intellidoc_dataset.gemini_pro_model`,
    TABLE prompts
  );

