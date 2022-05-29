from django.forms import forms


class StudentBulkUploadForm(forms.ModelForm):
  class Meta:
    fields = ("csv_file",)