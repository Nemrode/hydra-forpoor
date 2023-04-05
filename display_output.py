from termcolor import colored

def display_output(user, password, success):
    """
    Display the result of the brute force attack in the terminal
    """

    pattern = f"{user} : {password}"
    size = len(pattern)

    # Add multiple dote util the size of the pattern is 50
    while size < 50:
        pattern += "."
        size += 1

    if success == True:
        print(colored("[+] ", "green") + pattern + colored(" Success", "green"))
    else:
        print(colored("[+] ", "yellow") + pattern + colored(" Failed", "red"))
