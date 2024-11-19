import os
import tempfile
from celery import shared_task
from .utils.crackHash import run_hashcat
from .models import CrackHashModel


@shared_task
def crack_hash_task(hash_file_data, wordlist_file_data, hash_algorithm):
    """
    Task to handle hash cracking using hashcat.
    """
    print(hash_algorithm)
    try:
        # create an entry in database
        task_record, created = CrackHashModel.objects.get_or_create(
            task_id=crack_hash_task.request.id,
            defaults={
                'hash_algorithm': hash_algorithm,
                'status': 'PROCESSING',
            }

        )

        # Create temporary files
        with tempfile.TemporaryDirectory() as tempdir:
            hash_file_path = os.path.join(tempdir, 'hash.txt')
            wordlist_file_path = os.path.join(tempdir, 'wordlist.txt')

            # Write the uploaded data to temporary files
            with open(hash_file_path, 'wb') as hash_file:
                hash_file.write(hash_file_data)

            with open(wordlist_file_path, 'wb') as wordlist_file:
                wordlist_file.write(wordlist_file_data)

            # Run hashcat to crack the hash
            result = run_hashcat(hash_file_path, wordlist_file_path, hash_algorithm)

            # If already cracked, show the password
            if result['status'] == 'already cracked':
                result = run_hashcat(hash_file_path, wordlist_file_path, hash_algorithm, show=True)
            # Update task status and result in the database
            if result['status'] == 'cracked':
                task_record.status = 'SUCCESS'
                task_record.cracked_password = result['password']
            else:
                task_record.status = 'FAILED'
                task_record.error_message = result.get('stderr', 'Unknown error')

            task_record.save()
            return result

    except Exception as e:
        CrackHashModel.objects.filter(task_id=crack_hash_task.request.id).update(
            status='FAILED',
            error_message=str(e)
        )
        raise
