import os, configparser, validators

class Config(object):
    # Initialise the global config
    config = configparser.ConfigParser()
    def __init__(self):
        # if doesnt exist, write default
        if not os.path.exists('./config.ini'):
            self.set_targets()
        else:
            self.config.read("./config.ini")

    def add_host(self, host, domain, target_url, interval_time):
        self.config[host] = {'domain': domain, 'target_url': target_url, 'interval_time': interval_time, 
                            'last_scan': '', 'target_ip': '', 'website_hash': ''}
        self.write_file()

    def set_targets(self):
        # Loop to create all the targets
        while True:
            host = input("<config> Enter a name for the host (this is what will be used in logging and future config changes):\n> ")

            # Check if the name already exists
            if self.config.has_section(host):
                print('[-] Error: A host with this name already exists!\n\n<config> Enter a new name for the host:\n> ')
            else:
                # Create new host
                domain = input("<config> Please enter a domain name to monitor (e.g. google.com or abc.net.au):\n>")
                validated_domain = validate(domain)
                if "[-] Error" in validated_domain:
                    continue
                else:
                    interval_time = input("<config> How long between scans? (minutes):\n> ")

            self.add_host(host, domain, validated_domain, interval_time)

            add_more = input('<config> Would you like to add another host? (y/n)\n>')
            if add_more.lower() != "y":
                break

    def write_file(self):
        self.config.write(open('config.ini', 'w'))
                

def validate(url):
    http_url = "http://" + url
    https_url = "https://" + url

    if validators.url(https_url):
        print("[+] Successful access to " + https_url)
        return https_url
    elif validators.url(http_url):
        print("[+] Successful access to " + http_url)
        return http_url
    else:
        error_msg = "[-] Error: Unable to reach domain specified..."
        print(error_msg)
        return error_msg

def print_targets(overseer_config):
    print('\n[+] Current Targets:')
    # Loop through config and print section titles
    for section in self.config.sections():
        print(' - ' + section)

def get_host_count(overseer_config):
    count = 0
    for section in self.config.sections():
        if "target_url" in section:
            count += 1
    return count

def update_config(overseer_config, host, domain, target_url, target_ip, interval_time, last_scan, website_hash):
        overseer_config.config[host] = {'target_url': target_url, 'domain': domain, 
                                        'target_ip': target_ip, 'interval_time': interval_time, 
                                        'last_scan': last_scan, 'website_hash': website_hash 
                                    }
        overseer_config.write_file()    
