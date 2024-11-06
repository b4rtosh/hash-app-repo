from django.http import HttpResponse
from django.shortcuts import render
from .forms import GenerateHash, VerifyHash, CrackHash
from .utils import utils, crackHash
import tempfile
import os


def generate_hash_view(request):
    if request.method == "POST":
        form = GenerateHash(request.POST)
        if form.is_valid():
            plain_text = form.cleaned_data.get("plain_text")
            hash_type = form.cleaned_data.get("hash_type")
            hash_salt = form.cleaned_data.get("hash_salt") if form.cleaned_data.get("hash_salt") else ""
            hash_salt_generate = form.cleaned_data.get("hash_salt_generate")
            if hash_salt and hash_salt_generate:
                return render(request, "hash/generate.html",
                              {'form': form, "error": "Please provide either a salt or generate one."})
            if hash_salt_generate:
                hash_salt = "salt"

            try:
                hashed = utils.generate_hash(plain_text, hash_type, hash_salt)
                return render(request, "hash/result.html",
                              {'result': "Success! Here is message:", "hashed": hashed, 'salt': hash_salt, 'algorithm': hash_type, 'success': True})
            except Exception as e:
                return render(request, "hash/result.html",
                              {"result": "An error occurred while hashing the text.", 'success': False})
        else:
            return render(request, "hash/generate.html", {"form": form, "error": "Invalid form data."})
    return render(request, "hash/generate.html", {"form": GenerateHash()})


def verify_hash_view(request):
    if request.method == 'POST':
        form = VerifyHash(request.POST)
        if form.is_valid():
            plain_text = form.cleaned_data.get("plain_text")
            hash_type = form.cleaned_data.get("hash_type")
            hash_salt = form.cleaned_data.get("hash_salt") if form.cleaned_data.get("hash_salt") else ""
            hash_text = form.cleaned_data.get("hash_text")
            try:
                hashed = utils.generate_hash(plain_text, hash_type, hash_salt)
                if hashed == hash_text:
                    return render(request, "hash/result.html",
                                  {"result": "The hash matches the text.", 'algorithm': hash_type, 'success': True})
                else:
                    return render(request, "hash/result.html",
                                  {"result": "The hash does not match the text.", 'algorithm': hash_type, 'success': False})
            except Exception as e:
                return render(request, "hash/verify.html",
                              {"result": "An error occurred while hashing the text.", 'success': False})
        else:
            return render(request, "hash/verify.html", {"form": form, "error": "Invalid form data."})
    return render(request, "hash/verify.html", {"form": VerifyHash()})


def crack_hash_view(request):
    if request.method == 'POST':
        form = CrackHash(request.POST, request.FILES)
        if form.is_valid():
            hash_value = request.FILES['hash_value_file']
            wordlist = request.FILES['wordlist_file']
            hash_algorithm = form.cleaned_data.get("hash_type")

            # create a temporary directory to store the uploaded files
            temp_dir = tempfile.gettempdir()
            hash_file_path = os.path.join(temp_dir, hash_value.name)
            wordlist_file_path = os.path.join(temp_dir, wordlist.name)

            #  write the uploaded files to the temporary directory
            with open(hash_file_path, 'wb+') as hash_file:
                for chunk in hash_value.chunks():
                    hash_file.write(chunk)

            with open(wordlist_file_path, 'wb+') as wordlist_file:
                for chunk in wordlist.chunks():
                    wordlist_file.write(chunk)

            result = crackHash.run_hashcat(hash_file_path, wordlist_file_path, hash_algorithm)

            os.remove(hash_file_path)
            os.remove(wordlist_file_path)
            if result.status == 'cracked':
                return render(request, 'hash/crack_result.html',
                          {'password': result.password, 'algorithm': result.hash_type, 'success': True,
                           'hash': result.hash})

    else:
        form = CrackHash()
    return render(request, 'hash/crack.html', {'form': form})