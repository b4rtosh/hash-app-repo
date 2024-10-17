from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from .utils import des_encrypt, des_brute_force, des_decrypt, des_dictionary_attack


def des_encrypt_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        key = request.POST.get('key').encode('utf-8')

        # Ensure key length is 8 bytes
        if len(key) != 8:
            return render(request, 'des/encrypt.html', {'warning': "Key must be exactly 8 bytes long."})
        try:
            ciphertext, iv = des_encrypt(message, key)
            return render(request, 'des/result.html',
                      {'result': f"Success! Encrypted message: {ciphertext.hex()}",
                       'key': f"IV: {iv.hex()}", 'success': True})
        except Exception as e:
            return render(request, 'des/result.html',
                      {'result': f"Encryption failed with provided key: {key.decode('utf-8')}.",
                       'success': False})
    return render(request, 'des/encrypt.html')


def des_decrypt_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # ciphertext_file = request.FILES['ciphertext_file']
            # ciphertext = ciphertext_file.read()
            ciphertext = bytes.fromhex(form.cleaned_data['cipher_text'])
            iv = bytes.fromhex(form.cleaned_data['iv'])
            key = form.cleaned_data['key'].encode('utf-8') if form.cleaned_data['key'] else None
            dictionary_file = request.FILES.get('dictionary_file')
            charset = form.cleaned_data['charset'] if form.cleaned_data['charset'] else 'abcdefghijklmnopqrstuvwxyz'

            if key:  # If key is provided, attempt to decrypt the message
                try:
                    decrypted_data = des_decrypt(ciphertext, key, iv)
                    return render(request, 'des/result.html',
                                  {'result': f"Success! Decrypted message: {decrypted_data.decode('utf-8')}",
                                   'key': f"Provided Key: {key.decode('utf-8')}", 'success': True})
                except Exception as e:
                    return render(request, 'des/result.html',
                                  {'result': f"Decryption failed with provided key: {key.decode('utf-8')}.",
                                   'success': False})
            elif dictionary_file:  # If a dictionary file is uploaded, use dictionary attack
                try:
                    decrypted_data, dictionary_key = des_dictionary_attack(ciphertext, iv, dictionary_file)
                    if decrypted_data:
                        return render(request, 'des/result.html',
                                      {'result': f"Success! Decrypted message: {decrypted_data.decode('utf-8')}",
                                       'key': f"Dictionary Key: {dictionary_key.decode('utf-8')}", 'success': True})
                except Exception as e:
                    return render(request, 'des/result.html',
                                  {'result': f"Dictionary attack failed. No valid key found.", 'success': False})
            else:  # Attempt to brute force the key
                try:
                    decrypted_data, key = des_brute_force(ciphertext, iv, charset)
                    if decrypted_data:
                        return render(request, 'des/result.html',
                                      {'result': f"Success! Decrypted message: {decrypted_data.decode('utf-8')}",
                                       'key': f"Brute force key: {key.decode('utf-8')}", 'success': True})
                except Exception as e:
                    return render(request, 'des/result.html',
                                  {'result': f"Brute force attack failed. Key not found.", 'success': False})

    else:
        form = FileUploadForm()

    return render(request, 'des/crack.html', {'form': form})
