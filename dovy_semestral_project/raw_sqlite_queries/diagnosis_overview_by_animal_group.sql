-- přehled diagnóz podle četnosti u zvolené skupiny zvířat (psi, kočky, …)
SELECT veterinary_clinic_diagnosis.name, veterinary_clinic_diagnosis.description, count(veterinary_clinic_diagnosis.name) AS diagnosis_count
FROM veterinary_clinic_examination
INNER JOIN veterinary_clinic_diagnosis ON veterinary_clinic_examination.diagnosis_id=veterinary_clinic_diagnosis.id
INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id
INNER JOIN veterinary_clinic_animalgroup ON veterinary_clinic_animalgroup.id=group_id
WHERE veterinary_clinic_animalgroup.name='Psi'
GROUP BY veterinary_clinic_diagnosis.id
ORDER BY diagnosis_count DESC;