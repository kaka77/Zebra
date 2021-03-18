from design.banner import banner
from design.clear import clear

from lib.manager import connection_checker

import argparse

def main():
    clear()
    banner()

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help="Target URL", type=str)
    parser.add_argument('-p', help="Target Port", type=int, default=443)
    args = parser.parse_args()

    connection_checker(args)


if __name__ == "__main__":
    main()