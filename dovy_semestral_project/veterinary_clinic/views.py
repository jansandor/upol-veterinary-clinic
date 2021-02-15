from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from veterinary_clinic.forms import DateRangeInputForm, AnimalGroupInputForm, AnimalOwnerYearInputForm, DiagnosisSelectForm
from veterinary_clinic.custom_queries import animals_owners_examinationCount_totalPrice_between, diagnosis_by_animal_group
from veterinary_clinic.custom_queries import visitations_diagnosis_by_year_and_animal_or_owner
from veterinary_clinic.custom_queries import diagnosis_description, diagnosis_indications_count, diagnosis_medicaments_used_count
from veterinary_clinic.custom_queries import examinations_dates, examinations_within_date, total_examination_price
from veterinary_clinic.custom_queries import total_examinations, total_medicaments_used, medicaments_used_for_animals
from veterinary_clinic.models import Diagnosis
import datetime
# TODO kdyz prejdu ze stranky A na stranku B a pak zpatky a na strance A skoncil dotaz tak, ze nebyly nalezeny zaznamy, msg zustane zobrazena
# chtelo by to v get asi popovat msg z kontextu, ale nechci to ted komplikovat, pac to je spis takove provizorni reseni
# zatim vyreseno self.context.clear() v get()

# TODO pokud diagnoza je v DB, ale nebyla jeste indikovana pri vysetreni, nelze zobrazit detail
# neprirazene diagnozy se v ramci reseni v DB nevyskytuji

class HomePageView(TemplateView):
    template_name = 'veterinary_clinic/home.html'


class AnimalList(TemplateView):
    template_name = 'veterinary_clinic/animal-list.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.clear()     
        date_input_form = DateRangeInputForm()
        self.context['date_input_form'] = date_input_form
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        date_input_form = DateRangeInputForm(request.POST)
        if date_input_form.is_valid():
            self.context['date_input_form'] = date_input_form
            start_date = date_input_form.cleaned_data['start_date']
            end_date = date_input_form.cleaned_data['end_date']
            records = animals_owners_examinationCount_totalPrice_between(start_date, end_date)
            self.context['records'] = records
            if records.__len__() == 0:
                self.context['msg'] = "Pro zadanou kombinaci nebyly nalezeny žádné záznamy."
            return render(request, self.template_name, self.context)
        else:
            self.context.clear()
            self.context['date_input_form'] = date_input_form
            return render(request, self.template_name, self.context)        


class DiagnosisOverview(TemplateView):
    template_name = 'veterinary_clinic/diagnosis-overview.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.clear()
        animal_group_input_form = AnimalGroupInputForm()
        self.context['animal_group_input_form'] = animal_group_input_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        animal_group_input_form = AnimalGroupInputForm(request.POST)
        if animal_group_input_form.is_valid():
            self.context['animal_group_input_form'] = animal_group_input_form
            animal_group = animal_group_input_form.cleaned_data['animal_group']
            records = diagnosis_by_animal_group(animal_group.name)
            self.context['records'] = records
            if records.__len__() == 0:
                self.context['msg'] = "Pro zadanou kombinaci nebyly nalezeny žádné záznamy."
            return render(request, self.template_name, self.context)


class DailyExaminations(TemplateView):
    template_name = 'veterinary_clinic/daily-examinations.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.clear()     
        date_input_form = DateRangeInputForm()
        self.context['date_input_form'] = date_input_form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        date_input_form = DateRangeInputForm(request.POST)
        if date_input_form.is_valid():
            self.context['date_input_form'] = date_input_form
            start_date = date_input_form.cleaned_data['start_date']
            end_date = date_input_form.cleaned_data['end_date']
            dates = examinations_dates(start_date, end_date)  
            self.context['dates'] = dates            
            examinations = []
            prices = []
            examinations_counts = []
            medicaments_used_counts = []
            medicaments_animals = []
            for date in dates:
                examinations.append(examinations_within_date(date[0].strftime("%Y-%m-%d")))
                prices.append(total_examination_price(date[0].strftime("%Y-%m-%d")))
                examinations_counts.append(total_examinations(date[0].strftime("%Y-%m-%d")))
                medicaments_used_counts.append(total_medicaments_used(date[0].strftime("%Y-%m-%d")))
                medicaments_animals.append(medicaments_used_for_animals(date[0].strftime("%Y-%m-%d")))
            # animals_names =          
            self.context['examinations'] = examinations
            self.context['prices'] = prices
            self.context['examinations_counts'] = examinations_counts
            self.context['medicaments_used_counts'] = medicaments_used_counts
            self.context['medicaments_animals'] = medicaments_animals
            return render(request, self.template_name, self.context)
        else:
            self.context.clear()
            self.context['date_input_form'] = date_input_form
            return render(request, self.template_name, self.context)   


class VisitationsDiagnosisView(TemplateView):
    template_name = 'veterinary_clinic/visitations-diagnosis.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.clear()
        self.context['input_form'] = AnimalOwnerYearInputForm()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        input_form = AnimalOwnerYearInputForm(request.POST)
        if input_form.is_valid():
            self.context['input_form'] = input_form
            animal = input_form.cleaned_data['animal']
            owner = input_form.cleaned_data['owner']
            year = input_form.cleaned_data['year']
            if not animal:
                records = visitations_diagnosis_by_year_and_animal_or_owner(year, owner_fullname=owner.__str__())
            elif not owner:
                records = visitations_diagnosis_by_year_and_animal_or_owner(year, animal_name=animal.name)
            else:
                records = visitations_diagnosis_by_year_and_animal_or_owner(year, animal.name, owner.__str__())
            self.context['records'] = records
            if records.__len__() == 0:
                self.context['msg'] = "Pro zadanou kombinaci nebyly nalezeny žádné záznamy."
            return render(request, self.template_name, self.context)
        else:
            self.context.clear()
            self.context['input_form'] = input_form
            return render(request, self.template_name, self.context)

class DiagnosisDetailView(TemplateView):
    template_name = 'veterinary_clinic/diagnosis-detail.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.clear()
        self.context['data_present'] = False
        self.context['input_form'] = DiagnosisSelectForm()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        input_form = DiagnosisSelectForm(request.POST)
        if input_form.is_valid():
            self.context['input_form'] = input_form
            diagnosis = input_form.cleaned_data['diagnosis']
            description = diagnosis_description(diagnosis.pk)
            indications_count = diagnosis_indications_count(diagnosis.pk)
            medicaments = diagnosis_medicaments_used_count(diagnosis.pk)
            # ! nepredpoklada se, ze v DB je diagnoza neprirazena vysetreni
            meds_used_total = 0
            for i in range(medicaments.__len__()):
                if medicaments[i].get('name') != None:
                    meds_used_total = meds_used_total + 1
            self.context['no_meds_used_count'] = indications_count[0].get('indications_count') - meds_used_total
            self.context['diagnosis_description'] = description[0]
            self.context['diagnosis_indications_count'] = indications_count[0]
            self.context['medicaments'] = medicaments
            self.context['data_present'] = True
            return render(request, self.template_name, self.context)
        else:
            self.context.clear()
            self.context['data_present'] = False
            self.context['input_form'] = input_form
            return render(request, self.template_name, self.context)
