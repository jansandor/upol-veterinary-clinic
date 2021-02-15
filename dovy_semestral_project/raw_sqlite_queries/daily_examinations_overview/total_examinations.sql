-- celkovy pocet vysetreni pro vybrany den
SELECT date, count(DISTINCT veterinary_clinic_examination.id) AS total_examinations
FROM veterinary_clinic_examination
WHERE date = '2021-01-02';