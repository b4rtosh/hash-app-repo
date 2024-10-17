from cProfile import label

from django import forms

class FileUploadForm(forms.Form):
    # ciphertext_file = forms.FileField(label="Ciphertext File")
    cipher_text = forms.CharField(max_length=100, label="Ciphertext")
    iv = forms.CharField(max_length=16, label="IV (Initialization Vector, in hex)")
    key = forms.CharField(max_length=8, required=False, label="Key (optional, 8 bytes)")
    dictionary_file = forms.FileField(label='Dictionary File (Optional)', required=False)
    charset = forms.CharField(max_length=100, required=False, label="Charset (Optional, default: lowercase letters)")
