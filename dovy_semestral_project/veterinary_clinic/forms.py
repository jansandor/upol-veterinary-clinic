from django import forms
from django.utils.translation import gettext_lazy as _
from veterinary_clinic.models import Animal, AnimalGroup, AnimalOwner, Diagnosis


class DateRangeInputForm(forms.Form):
    start_date = forms.DateField(label=_("Od"), widget=forms.SelectDateWidget)
    end_date = forms.DateField(label=_("Do"), widget=forms.SelectDateWidget)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError(_("Pro zvolený interval nelze vrátit žádnou hodnotu."))
        else:
            return cleaned_data

class AnimalGroupInputForm(forms.Form):
    animal_group = forms.ModelChoiceField(AnimalGroup.objects.all(), label=_("Skupina zvířat"), empty_label=None)

class YearSelectDateWidget(forms.SelectDateWidget):
    template_name = 'veterinary_clinic/select_date.html'
        
import datetime

class AnimalOwnerYearInputForm(forms.Form):
    YEAR_CHOICES = [(r,r) for r in range(datetime.date.today().year, datetime.date.today().year + 10)]

    animal = forms.ModelChoiceField(Animal.objects.all().order_by('name'), label=_("Zvíře"), required=False)
    owner = forms.ModelChoiceField(AnimalOwner.objects.all().order_by('surname'), label=_("Majitel"), required=False)
    year = forms.ChoiceField(label=_("Rok"), choices=YEAR_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        animal = cleaned_data.get("animal")
        owner = cleaned_data.get("owner")
        if not animal and not owner:
            raise forms.ValidationError(_("Je třeba vybrat zvíře a/nebo vlastníka."))
        else:
            return cleaned_data

class DiagnosisSelectForm(forms.Form):
    diagnosis = forms.ModelChoiceField(Diagnosis.objects.all().order_by('id'), label=_("Diagnóza"), empty_label=None)