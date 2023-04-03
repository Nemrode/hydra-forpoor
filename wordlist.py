import os

def create_wordlist(wordlist_path):
    """Get the path of the wordlist and return a list of words """

    cwd = os.getcwd()

    if wordlist_path[0] != "/":
        wordlist_path = os.getcwd() + "/" + wordlist_path
    elif wordlist_path[0] == "." and wordlist_path[1] == "/":
        wordlist_path = os.getcwd() + wordlist_path[1:]
    else:
        wordlist_path = wordlist_path

    wordlist = open(wordlist_path, "r")
    wordlist = wordlist.readlines()
    wordlist = [word.strip() for word in wordlist]
    
    return wordlist