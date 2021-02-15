-- select pouze datumu, ve kterych probehla nejaka vysetreni z vybraneho rozsahu datumu
SELECT date FROM veterinary_clinic_examination
WHERE date BETWEEN '2021-01-01' AND '2021-03-01'
GROUP BY date
ORDER BY date;