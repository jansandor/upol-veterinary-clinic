--  pocet aplikovanych leku dany den celkem
SELECT date, count(veterinary_clinic_medicament.name) AS meds_used_total FROM veterinary_clinic_examination
INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id
LEFT JOIN veterinary_clinic_examination_medicaments ON examination_id=veterinary_clinic_examination.id
LEFT JOIN veterinary_clinic_medicament ON medicament_id=veterinary_clinic_medicament.id
WHERE date = '2021-01-24';