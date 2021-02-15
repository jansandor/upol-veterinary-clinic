from django.contrib import admin

from veterinary_clinic.models import Animal, AnimalGroup, AnimalOwner, Examination, Medicament, Diagnosis
# Register your models here.

admin.site.register(Animal)
admin.site.register(AnimalGroup)
admin.site.register(AnimalOwner)
admin.site.register(Examination)
admin.site.register(Medicament)
admin.site.register(Diagnosis)