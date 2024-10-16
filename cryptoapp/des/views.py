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
            return HttpResponse("Key must be exactly 8 bytes long.")

        ciphertext, iv = des_encrypt(message, key)
        return HttpResponse(f"Ciphertext: {ciphertext.hex()}<br>IV: {iv.hex()}")

    return render(request, 'des/encrypt.html')


def des_crack_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # ciphertext_file = request.FILES['ciphertext_file']
            # ciphertext = ciphertext_file.read()
            ciphertext = bytes.fromhex(form.cleaned_data['cipher_text'])
            iv = bytes.fromhex(form.cleaned_data['iv'])
            key = form.cleaned_data['key'].encode('utf-8') if form.cleaned_data['key'] else None
            dictionary_file = request.FILES.get('dictionary_file')

            if key:  # If key is provided, attempt to decrypt the message
                try:
                    decrypted_data = des_decrypt(ciphertext, key, iv)
                    return HttpResponse(
                        f"Decrypted message: {decrypted_data.decode('utf-8')}<br>Key: {key.decode('utf-8')}")
                except Exception as e:
                    return HttpResponse(f"Decryption failed with provided key: {key.decode('utf-8')}. Error: {e}")
            elif dictionary_file:  # If a dictionary file is uploaded, use dictionary attack
                decrypted_data, dictionary_key = des_dictionary_attack(ciphertext, iv, dictionary_file)
                if decrypted_data:
                    return HttpResponse(
                        f"Success! Decrypted message: {decrypted_data.decode('utf-8')}<br>Dictionary Key: {dictionary_key.decode('utf-8')}")
                else:
                    return HttpResponse("Dictionary attack failed. No valid key found.")
            else:  # Attempt to brute force the key
                decrypted_data, key = des_brute_force(ciphertext, iv)
                if decrypted_data:
                    return HttpResponse(
                        f"Success! Decrypted message: {decrypted_data.decode('utf-8')}<br>Key: {key.decode('utf-8')}")
                else:
                    return HttpResponse("Key not found.")

    else:
        form = FileUploadForm()

    return render(request, 'des/crack.html', {'form': form})