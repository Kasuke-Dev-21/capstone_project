from django import forms
from .models import Student, Map, Report

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname', 'lastname', 'age', 'level', 'strand', 'contact', 'mail_address']

class HazardReportForm(forms.Form):
    MAP_CHOICES = [(map_obj.id, map_obj.title) for map_obj in Map.objects.all()]

    map = forms.ChoiceField(label="Location of the Hazard", choices=MAP_CHOICES)
    location = forms.CharField(label="Additional Specifics", max_length=100)
    description = forms.CharField(label="Details of the Hazard", widget=forms.Textarea)
    status = forms.CharField(initial="Standby", widget=forms.HiddenInput())

    def save(self):
        location = self.cleaned_data['location']
        description = self.cleaned_data['description']
        map_id = self.cleaned_data['map']
        map = Map.objects.get(id=map_id)
        status = self.cleaned_data['status']
        hazard_report = Report.objects.create(location=location, description=description, map=map, status=status)
        return hazard_report