from cProfile import label

from django import forms


class GenerateHash(forms.Form):
    plain_text = forms.CharField(max_length=100, label="Enter the text to hash")
    hash_type = forms.ChoiceField(choices=[('md5', 'MD5'), ('sha1', 'SHA1'), ('sha256', 'SHA256'), ('sha512', 'SHA512')],
                                  label="Select the hash type")
    hash_salt = forms.CharField(max_length=100, label="Enter the salt (optional)", required=False)
    hash_salt_generate = forms.BooleanField(label="Generate salt (optional)", required=False)
