import subprocess


def run_hashcat(hash_value, wordlist, hash_algorithm='0'):
    try:
        result = subprocess.run(
            [
                'hashcat', '-m', hash_algorithm, '-a', '0', hash_value, wordlist, '--force', '-D', '1',
                '--software-only'
            ],
            capture_output=True, text=True
        )
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"  # Return the output from Hashcat
    except Exception as e:
        return str(e)
