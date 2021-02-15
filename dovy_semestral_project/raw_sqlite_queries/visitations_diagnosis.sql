-- přehled návštěv a diagnóz pro vybrané zvíře nebo vlastníka ve zvoleném roce
SELECT date, veterinary_clinic_animal.name AS animal_name,
veterinary_clinic_animalowner.name || ' ' || veterinary_clinic_animalowner.surname AS owner_fullname,
veterinary_clinic_diagnosis.name AS diagnosis, description
FROM veterinary_clinic_examination
INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id
INNER JOIN veterinary_clinic_animalowner ON owner_id=veterinary_clinic_animalowner.id
INNER JOIN veterinary_clinic_diagnosis ON diagnosis_id=veterinary_clinic_diagnosis.id
WHERE strftime('%%Y', date) = %s
AND CASE
	WHEN %s <> '' AND %s <> '' THEN animal_name = %s AND owner_fullname = %s
	WHEN %s <>'' THEN animal_name = %s
	WHEN %s = '' THEN owner_fullname = %s END"