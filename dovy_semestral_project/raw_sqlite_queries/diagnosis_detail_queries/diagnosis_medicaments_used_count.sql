SELECT medicament_name AS name, count(medicament_name) AS used_count FROM diagnosis_medicament_view
WHERE diagnosis_id = 1
GROUP BY name
ORDER BY used_count DESC;