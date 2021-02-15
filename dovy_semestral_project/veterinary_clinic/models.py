from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.

class Medicament(models.Model):
    name = models.CharField(_("jméno"), max_length=60)
    # in_stock = models.IntegerField(_("skladem"))

    def __str__(self):
        return self.name

# class Diagnosis(models.Model):
#     description = models.TextField(_("diagnóza"))

class AnimalOwner(models.Model):
    name = models.CharField(_("jméno"), max_length=60)
    surname = models.CharField(_("příjmení"), max_length=60)\

    def __str__(self):
        return f'{self.name} {self.surname}'


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

class Diagnosis(models.Model):
    name = models.CharField(_("název"), max_length=60)
    description = models.TextField(_("popis"))

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('diagnosis-detail', args=[str(self.pk)])

    def __str__(self):
        return self.name

class Examination(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.SET_NULL, null=True, verbose_name=_("diagnóza"))
    price = models.DecimalField(_("cena"), decimal_places=2, max_digits=12)
    date = models.DateField(_("datum vyšetření"))
    medicaments = models.ManyToManyField(Medicament, blank=True, verbose_name=_("podané léky"))
    animal = models.ForeignKey(Animal, verbose_name=_("zvíře"), on_delete=models.CASCADE)

    def __str__(self):
        return f'Vyšetření zvířete {self.animal.__str__()} dne {self.date}'
