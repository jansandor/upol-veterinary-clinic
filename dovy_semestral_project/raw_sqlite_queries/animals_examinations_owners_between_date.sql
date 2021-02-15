/*
pro zvolený časový interval (od data po datum) výpis zvířat, která byla v té době vyšetřována,
s výpisem jejich majitelů, počtu vyšetření a celkovou účtovanou cenu
*/
SELECT veterinary_clinic_animal.name AS animal_name, veterinary_clinic_animalgroup.name AS animal_group_name, count(animal_id) AS total_examinations, sum(price) AS total_price, veterinary_clinic_animalowner.name AS owner_name
FROM veterinary_clinic_examination
INNER JOIN veterinary_clinic_animal ON veterinary_clinic_animal.id = animal_id
INNER JOIN veterinary_clinic_animalgroup ON veterinary_clinic_animalgroup.id = group_id
INNER JOIN veterinary_clinic_animalowner ON veterinary_clinic_animalowner.id = owner_id
WHERE date BETWEEN '2021-01-01' AND '2023-12-31'
GROUP BY animal_name
ORDER BY animal_name;