from django.urls import path

from veterinary_clinic.views import HomePageView, AnimalList, DailyExaminations, DiagnosisOverview, VisitationsDiagnosisView, DiagnosisDetailView

urlpatterns = [
    path('animal-list/', AnimalList.as_view(), name='animal-list'),
    path('diagnosis-overview/', DiagnosisOverview.as_view(), name='diagnosis-overview'),
    path('daily-examinations/', DailyExaminations.as_view(), name='daily-examinations'),
    path('visitations-diagnosis/', VisitationsDiagnosisView.as_view(), name='visitations-diagnosis'),
    path('diagnosis/', DiagnosisDetailView.as_view(), name='diagnosis'),
    path('diagnosis/<int:pk>/detail/', DiagnosisDetailView.as_view(), name='diagnosis-detail'),
    path('', HomePageView.as_view(), name='home')
]