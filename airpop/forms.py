from django import forms
from django.core.validators import FileExtensionValidator

class Datasetform(forms.Form):
        file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
