from django.shortcuts import render
from .forms import GenerateHash, VerifyHash, CrackHash
from .tasks import crack_hash_task
from .utils import utils
from .models import CrackHashModel


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
                # Generate a random salt
                hash_salt = utils.generate_salt()

            try:
                hashed = utils.generate_hash(plain_text, hash_type, hash_salt)
                return render(request, "hash/result.html",
                              {'result': "Success! Here is message:", "hashed": hashed, 'salt': hash_salt,
                               'algorithm': hash_type, 'success': True})
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
                                  {"result": "The hash does not match the text.", 'algorithm': hash_type,
                                   'success': False})
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
            hash = request.FILES['hash_value_file']
            wordlist = request.FILES['wordlist_file']
            hash_algorithm = form.cleaned_data.get("hash_type")
            hash_salt = form.cleaned_data.get("hash_salt") if form.cleaned_data.get("hash_salt") else ""
            print(hash_algorithm)
            #       read data from files
            hash_file_data = hash.read()
            wordlist_file_data = wordlist.read()

            #       call Celery task
            task = crack_hash_task.delay(hash_file_data, wordlist_file_data, hash_algorithm, hash_salt=hash_salt)
            if task.status == 'FAILED':
                return render(request, 'hash/crack_result.html', {
                    'success': False,
                    'error': task.error_message,
                })
            return render(request, 'hash/crack_result.html', {
                'success': True,
                'task_id': task.id,
                'message': 'Task has been queued successfully. Check the task status for updates.'
            })

    return render(request, 'hash/crack.html', {'form': CrackHash()})


def task_results_view(request):
    tasks = CrackHashModel.objects.all().order_by('-created_at')

    return render(request, 'hash/task_results.html', {'tasks': tasks})
