import subprocess
import re


def run_dictionary(hash_value, wordlist, hash_algorithm='0'):
    try:
        command = [
            'hashcat', '-m', hash_algorithm, '-a', '0', hash_value, wordlist
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        stdout = result.stdout
        stderr = result.stderr
        show = False
        if "--show" in stdout:
            show = True
            command.append("--show")
            result = subprocess.run(command, capture_output=True, text=True)
            stdout = result.stdout
            stderr = result.stderr

        # Determine if the password was cracked
        if "Cracked" in stdout or show:
            # Extract the cracked password from the output
            match = re.search(r"([a-fA-F\d]{32}):(\S+)", stdout)
            if match:
                cracked_hash = match.group(1)
                cracked_password = match.group(2)
                return {
                    "status": "cracked",
                    "hash": cracked_hash,
                    "hash_type": hash_algorithm,
                    "password": cracked_password,
                    "stdout": stdout,
                    "stderr": stderr
                }
        elif "Exhausted" in stdout:
            return {
                "status": "not cracked",
                "stdout": stdout,
                "stderr": stderr
            }
        # If neither "Cracked" nor "Exhausted" found, return the raw output
        return {
            "status": "unknown",
            "stdout": stdout,
            "stderr": stderr
        }

    except Exception as e:
        return str(e)


# def run_brute(hash_value, hash_algorithm='0', show=False):

