--denní výpisy vyšetření s uvedením aplikovaných léků a cen vyšetření ve zvoleném časovém termínu (od data po datum) včetně příslušných denních součtů
SELECT *
FROM veterinary_clinic_examination
LEFT JOIN veterinary_clinic_examination_medicaments ON veterinary_clinic_examination.id=examination_id
LEFT JOIN veterinary_clinic_medicament ON medicament_id=veterinary_clinic_medicament.id
INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id
INNER JOIN veterinary_clinic_diagnosis ON diagnosis_id=veterinary_clinic_diagnosis.id
WHERE date BETWEEN '2021-01-02' AND '2021-03-01'
ORDER BY veterinary_clinic_examination.id;