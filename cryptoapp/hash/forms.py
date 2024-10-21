from cProfile import label

from django import forms


class GenerateHash(forms.Form):
    plain_text = forms.CharField(max_length=100, label="Enter the text to hash")
    hash_type = forms.ChoiceField(choices=[('md5', 'MD5'), ('sha1', 'SHA1'), ('sha256', 'SHA256'), ('sha512', 'SHA512')],
                                  label="Select the hash type")
    hash_salt = forms.CharField(max_length=100, label="Enter the salt (optional)", required=False)
    hash_salt_generate = forms.BooleanField(label="Generate salt (optional)", required=False)


class VerifyHash(forms.Form):
    plain_text = forms.CharField(max_length=100, label="Enter the text to hash")
    hash_type = forms.ChoiceField(
        choices=[('md5', 'MD5'), ('sha1', 'SHA1'), ('sha256', 'SHA256'), ('sha512', 'SHA512')],
        label="Select the hash type")
    hash_salt = forms.CharField(max_length=100, label="Enter the salt (optional)", required=False)
    hash_text = forms.CharField(max_length=100, label="Enter the hash to verify")


class CrackHash(forms.Form):
    hash_value_file = forms.FileField(label="Select the hash file", required=True,
                                 help_text="The file should contain the hash value to crack")
    wordlist_file = forms.FileField(label="Select the wordlist file", required=True)
    hash_type = forms.ChoiceField(
        choices=[('0', 'MD5'), ('100', 'SHA1'), ('1400', 'SHA256'), ('sha512', 'SHA512')],
        label="Select the hash type")
