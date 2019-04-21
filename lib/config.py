import os
import configparser
import validators


class SystemConfig(object):
    systemconfig = configparser.ConfigParser()

    def __init__(self):
        if not os.path.exists('./system.ini'):
            self.setup_system_config()
        else:
            self.systemconfig.read("./system.ini")

    def setup_system_config(self):
        # Setup Slack, Email and Webhost config
        print("[+] Enter 'y' or 'n' for each of the following:")
        get_slack = input("<config> Would you like to configure Slack?\n> ")
        get_email = input("<config> Would you like to configure Email Alerts?\n> ")
        get_web = input("<config> Would you like to configure Web listener?\n> ")

        if get_slack == 'y':
            slack_token = input("<slack config> Please enter Slack Token:\n>")
            channel = input("<slack config> Please enter Channel to post alert to:\n>")
            self.add_slack_config(slack_token, channel)

        if get_email == 'y':
            smtp_url = input("<email config> Please enter your SMTP URL:\n>")
            username = input("<email config> Please enter your SMTP Username:\n>")
            send_from_email = input("<email config> Please enter your email address:\n>")
            send_to_email = input("<email config> Please enter the email you would like to alerts sent to:\n>")
            password = input("<email config> Please enter your email password:\n>")
            self.add_email_config(smtp_url, username, send_from_email, send_to_email, password)

        if get_web == 'y':
            webhost = input("<webhost config> Please enter your web listener URL:\n>")
            self.add_web_config(webhost)
        
        get_chrome_driver = input("<config> Would you like to use Chrome Driver for Visual Change Detection?\n>")
        get_gecko_driver = input("<config> Would you like to use Gecko Driver for Visual Change Detection?\n>")
        if get_chrome_driver == 'y':
            driver_location = input("<chrome config> Please enter Chrome Driver location (i.e. /Applications/ChromeDriver):\n>")
            self.add_visual_driver("chrome", driver_location)
        elif get_gecko_driver == 'y':
            driver_location = input("<gecko config> Please enter Gecko Driver location (i.e. /Applications/GeckoDriver):\n>")
            self.add_visual_driver("gecko", driver_location)
        else:
            self.add_visual_driver("Nil", "N/A")

    def add_slack_config(self, slack_token, channel):
        self.systemconfig['Slack'] = {'slack_token': slack_token, 'channel': channel}
        self.write_file()
    
    def add_email_config(self, smtp_url, username, send_from_email, send_to_email, password):
        self.systemconfig['Email'] = {'smtp_url': smtp_url, 'send_from_email': send_from_email,
                            'send_to_email': send_to_email, 'username': username, 'password': password}
        self.write_file()

    def add_visual_driver(self, driver_type, driver_location):
        self.systemconfig['Visual'] = {'driver_type': driver_type, 'driver_location': driver_location}
        self.write_file()

    def add_web_config(self, url):
        self.systemconfig['Webhost'] = {'url': url}
        self.write_file()

    def write_file(self):
        self.systemconfig.write(open('system.ini', 'w'))


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
        self.config[host] = {'domain': domain, 'target_url': target_url,
                             'interval_time': interval_time, 'last_scan': '',
                             'target_ip': '', 'website_hash': ''}
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


def update_config(overseer_config, host, domain, target_url, target_ip,
                  interval_time, last_scan, website_hash):
        overseer_config.config[host] = {'target_url': target_url,
                                        'domain': domain,
                                        'target_ip': target_ip,
                                        'interval_time': interval_time,
                                        'last_scan': last_scan,
                                        'website_hash': website_hash
                                        }
        overseer_config.write_file()
