SELECT
  unique_id,
  cosine_similarity,
  ai_summary
FROM
  `intellidoc-hackathon-2025.intellidoc_dataset.ai_covid_summaries_from_search`
ORDER BY
  cosine_similarity DESC
LIMIT 20;
