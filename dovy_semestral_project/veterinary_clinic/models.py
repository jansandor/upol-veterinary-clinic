from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Medicament(models.Model):
    name = models.CharField(_("Jméno"), max_length=60)
    in_stock = models.IntegerField(_("skladem"))

    def __str__(self):
        return self.name

# class Diagnosis(models.Model):
#     description = models.TextField(_("diagnóza"))

class AnimalOwner(models.Model):
    name = models.CharField(_("jméno"), max_length=60)

    def __str__(self):
        return self.name


class AnimalGroup(models.Model):
    name = models.CharField(_("jméno"), max_length=60)

    def __str__(self):
        return self.name


class Animal(models.Model):
    #owner = models.OneToOneField(AnimalOwner, on_delete=models.CASCADE)
    name = models.CharField(_("jméno"), max_length=60)
    # examinations = models.ForeignKey(Examination, verbose_name=_("vyšetření"), on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(AnimalGroup, verbose_name=_("skupina"), on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(AnimalOwner,verbose_name=_("majitel"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Examination(models.Model):
    # diagnosis = models.OneToOneField(Diagnosis, verbose_name=_("diagnóza"), on_delete=models.CASCADE)
    diagnosis = models.TextField(_("diagnóza"))
    price = models.DecimalField(_("cena"), decimal_places=2, max_digits=12)
    date = models.DateTimeField(_("datum vyšetření"))
    medicaments = models.ForeignKey(Medicament, verbose_name=_("podané léky"), on_delete=models.CASCADE, null=True, blank=True)
    animal = models.ForeignKey(Animal, verbose_name=_("zvíře"), on_delete=models.CASCADE)

    def __str__(self):
        return f'Vyšetření {self.animal.__str__()} {self.date}'



    






    








