from django.shortcuts import render
from .forms import GenerateHash
from . import utils


# Create your views here.


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
                              {'form': GenerateHash(), "error": "Please provide either a salt or generate one."})
            if hash_salt_generate:
                hash_salt = "salt"

            try:
                if hash_type == "md5":
                    hashed = utils.hash_string_md5(plain_text, hash_salt)
                elif hash_type == "sha1":
                    hashed = utils.hash_string_sha1(plain_text, hash_salt)
                elif hash_type == "sha256":
                    hashed = utils.hash_string_sha256(plain_text, hash_salt)
                elif hash_type == "sha512":
                    hashed = utils.hash_string_sha512(plain_text, hash_salt)
                return render(request, "hash/result.html",
                              {"hashed": hashed, 'salt': hash_salt, 'algorithm': hash_type, 'success': True})
            except Exception as e:
                return render(request, "hash/result.html",
                              {"result": "An error occurred while hashing the text.", 'success': False})
    return render(request, "hash/generate.html", {"form": GenerateHash()})
