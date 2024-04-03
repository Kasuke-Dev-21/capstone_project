from django import forms
from .models import Student, Map, Report

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname', 'lastname', 'age', 'level', 'strand', 'contact', 'mail_address']

class HazardReportForm(forms.Form):
    map = forms.ChoiceField(label="Location of the Hazard", choices=[])
    type = forms.ChoiceField(label="Type of Hazard", choices=[])
    location = forms.CharField(label="Additional Specifics", max_length=100)
    description = forms.CharField(label="Details of the Hazard", widget=forms.Textarea)
    status = forms.CharField(initial="Standby", widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['map'].choices = [(map_obj.id, map_obj.title) for map_obj in Map.objects.all()]
        self.fields['type'].choices = [(type_key, type_value) for type_key, type_value in Report.category.items()]

    def save(self):
        location = self.cleaned_data['location']
        description = self.cleaned_data['description']
        map_id = self.cleaned_data['map']
        map = Map.objects.get(id=map_id)
        type = self.cleaned_data['type']
        status = self.cleaned_data['status']
        hazard_report = Report.objects.create(location=location, description=description, map=map, type=type, status=status)
        return hazard_report