from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def animals_owners_examinationCount_totalPrice_between(start_date, end_date):
    cursor = connection.cursor()
    sql = "SELECT veterinary_clinic_animal.name AS animal_name, veterinary_clinic_animalgroup.name AS animal_group_name, count(animal_id) AS total_examinations, sum(price) AS total_price, veterinary_clinic_animalowner.name AS owner_name, veterinary_clinic_animalowner.surname AS owner_surname FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON veterinary_clinic_animal.id = animal_id INNER JOIN veterinary_clinic_animalgroup ON veterinary_clinic_animalgroup.id=group_id INNER JOIN veterinary_clinic_animalowner ON veterinary_clinic_animalowner.id = owner_id WHERE date BETWEEN %s AND %s GROUP BY animal_name ORDER BY animal_name"
    cursor.execute(sql, [start_date, end_date])
    records = dictfetchall(cursor)
    return records

def diagnosis_by_animal_group(group):
    cursor = connection.cursor()
    sql = "SELECT veterinary_clinic_diagnosis.name, veterinary_clinic_diagnosis.description, count(veterinary_clinic_diagnosis.name) AS diagnosis_count FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_diagnosis ON veterinary_clinic_examination.diagnosis_id=veterinary_clinic_diagnosis.id INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id INNER JOIN veterinary_clinic_animalgroup ON veterinary_clinic_animalgroup.id=group_id WHERE veterinary_clinic_animalgroup.name = %s GROUP BY veterinary_clinic_diagnosis.id ORDER BY diagnosis_count DESC"
    cursor.execute(sql, [group])
    records = dictfetchall(cursor)
    return records

def visitations_diagnosis_by_year_and_animal_or_owner(year, animal_name='', owner_fullname=''):
    cursor = connection.cursor()
    sql = "SELECT date, veterinary_clinic_animal.name AS animal_name, veterinary_clinic_animalowner.name || ' ' || veterinary_clinic_animalowner.surname AS owner_fullname, veterinary_clinic_diagnosis.name AS diagnosis, description FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id INNER JOIN veterinary_clinic_animalowner ON owner_id=veterinary_clinic_animalowner.id INNER JOIN veterinary_clinic_diagnosis ON diagnosis_id=veterinary_clinic_diagnosis.id WHERE strftime('%%Y', date) = %s AND CASE WHEN %s <> '' AND %s <> '' THEN animal_name = %s AND owner_fullname = %s WHEN %s <>'' THEN animal_name = %s WHEN %s = '' THEN owner_fullname = %s END"
    cursor.execute(sql, [year, animal_name, owner_fullname, animal_name, owner_fullname, animal_name, animal_name, animal_name, owner_fullname])
    records = dictfetchall(cursor)
    return records

def diagnosis_description(id):
    cursor = connection.cursor()
    sql = "SELECT diagnosis_description AS description FROM diagnosis_medicament_view WHERE diagnosis_id = %s LIMIT 1"
    cursor.execute(sql, [id])
    records = dictfetchall(cursor)
    return records

def diagnosis_indications_count(id):
    cursor = connection.cursor()
    sql = "SELECT count(*) AS indications_count FROM diagnosis_medicament_view WHERE diagnosis_id = %s"
    cursor.execute(sql, [id])
    records = dictfetchall(cursor)
    return records

def diagnosis_medicaments_used_count(id):
    cursor = connection.cursor()
    sql = "SELECT medicament_name AS name, count(medicament_name) AS used_count FROM diagnosis_medicament_view WHERE diagnosis_id = %s GROUP BY name ORDER BY used_count DESC"
    cursor.execute(sql, [id])
    records = dictfetchall(cursor)
    return records

def examinations_dates(start_date, end_date):
    cursor = connection.cursor()
    sql = "SELECT date FROM veterinary_clinic_examination WHERE date BETWEEN %s AND %s GROUP BY date ORDER BY date"
    cursor.execute(sql, [start_date, end_date])
    records = cursor.fetchall() #dictfetchall(cursor)
    return records

def examinations_within_date(date):
    cursor = connection.cursor()
    sql = "SELECT date, veterinary_clinic_animal.id AS animal_id, name AS animal_name, price FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id WHERE date = %s"
    cursor.execute(sql, [date])
    records = dictfetchall(cursor)
    return records

def total_examination_price(date):
    cursor = connection.cursor()
    sql = "SELECT date, sum(price) AS total_price FROM veterinary_clinic_examination WHERE date = %s GROUP BY date"
    cursor.execute(sql, [date])
    records = dictfetchall(cursor)
    return records

def total_examinations(date):
    cursor = connection.cursor()
    sql = "SELECT date, count(DISTINCT veterinary_clinic_examination.id) AS total_examinations FROM veterinary_clinic_examination WHERE date = %s"
    cursor.execute(sql, [date])
    records = dictfetchall(cursor)
    return records

def total_medicaments_used(date):
    cursor = connection.cursor()
    sql = "SELECT date, count(veterinary_clinic_medicament.name) AS meds_used_total FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id LEFT JOIN veterinary_clinic_examination_medicaments ON examination_id=veterinary_clinic_examination.id LEFT JOIN veterinary_clinic_medicament ON medicament_id=veterinary_clinic_medicament.id WHERE date = %s"
    cursor.execute(sql, [date])
    records = dictfetchall(cursor)
    return records

def medicaments_used_for_animals(date):
    cursor = connection.cursor()
    sql = "SELECT date, animal_id, veterinary_clinic_medicament.name AS medicament FROM veterinary_clinic_examination INNER JOIN veterinary_clinic_animal ON animal_id=veterinary_clinic_animal.id LEFT JOIN veterinary_clinic_examination_medicaments ON examination_id=veterinary_clinic_examination.id LEFT JOIN veterinary_clinic_medicament ON medicament_id=veterinary_clinic_medicament.id WHERE date = %s"
    cursor.execute(sql, [date])
    records = dictfetchall(cursor)
    return records
