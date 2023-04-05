import requests, argparse, sys, time
from bruteforce_ssh import *
from bruteforce_mysql import *
from wordlist import create_wordlist
from termcolor import colored


def main():

    parser = argparse.ArgumentParser(description="Brute force Hydra-forpoor")
    parser.add_argument("-p", "--protocol", help="protcol to use", default="ssh", type=str, required=True)
    parser.add_argument("-t", "--target", help="target to attack (IP or hostname)", required=True)
    parser.add_argument("-u", "--user", help="user to use", default="root", required=True)
    parser.add_argument("-P", "--port", help="port to use", type=int, required=True)
    parser.add_argument("-w", "--wordlist", help="wordlist path to use", required=True)
    parser.add_argument("-T", "--threads", help="number of threads to use", type=int, default=5, required=False)
    # parser.add_argument("-o", "--output", help="output file", default="output.txt", required=True)
    args = parser.parse_args()

    start = time.time()

    print(colored("[+] Starting SSH brute force attack", 'yellow'))

    if args.protocol == "ssh":

        output = brute_force_ssh(args.target, args.port, args.user, args.wordlist, start, args.threads)
        sys.exit(output)
    
    elif args.protocol == "mysql":
        output = brute_force_mysql(args.target, args.user, args.port, args.wordlist, start, args.threads)
        print(output)

    else:
        print("Protocol not supported")
        sys.exit(1)


if __name__ == '__main__':
    main()
