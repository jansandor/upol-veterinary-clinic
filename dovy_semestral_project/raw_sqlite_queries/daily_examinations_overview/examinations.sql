-- vysetreni zvirat pro zadany datum
SELECT date, veterinary_clinic_animal.id AS animal_id, name AS animal_name, price FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id
WHERE date = '2021-01-02';