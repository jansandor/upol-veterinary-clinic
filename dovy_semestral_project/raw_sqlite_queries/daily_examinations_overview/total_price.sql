-- celkove cena vysetreni zvirat pro zadany datum
SELECT date, sum(price) AS total_price FROM veterinary_clinic_examination
WHERE date = '2021-01-02'
GROUP BY date;