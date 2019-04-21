#!/usr/bin/python3
# import sys
from lib.config import Config, SystemConfig
from lib.watcher import threader


def overseer():
    print_banner()
    system_config = SystemConfig()
    overseer_config = Config()

    threader(system_config, overseer_config)


def print_banner():
    print("""                                                                                         
     _____   _____ _ __ ___  ___  ___ _ __ 
    / _ \ \ / / _ \ '__/ __|/ _ \/ _ \ '__|
   | (_) \ V /  __/ |  \__ \  __/  __/ |   
    \___/ \_/ \___|_|  |___/\___|\___|_|    
                                                                                   
[+] A multithreaded, multi-website monitoring and protection tool created by @evcsec and @snags141
    """)

if __name__ == '__main__':
    overseer()
