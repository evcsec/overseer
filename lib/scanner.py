from bs4 import BeautifulSoup
from .date import get_current_datetime, get_time_diff
from .config import update_config
from .logger import write_log
from .visualiser import detect_visual_changes
from .alerts import send_email
from .alerts import send_slack_message
import requests
import time
import socket
import hashlib
import os


def monitor(system_config, overseer_config, config_section):
    while True:
        # Run Website Scan and Port Scan
        domain = overseer_config.config.get(config_section, 'domain')
        target_url = overseer_config.config.get(config_section, 'target_url')
        target_ip = overseer_config.config.get(config_section, 'target_ip')
        interval_time = overseer_config.config.get(config_section,
                                                   'interval_time')
        last_scan = overseer_config.config.get(config_section, 'last_scan')
        website_hash = overseer_config.config.get(config_section,
                                                  'website_hash')

        detect_visual_changes(system_config, config_section, target_url)
        server_ip = port_scan(config_section, domain, target_ip)
        scan_hash = web_scan(config_section, target_url, website_hash)
        if scan_hash:
            scan_time = get_current_datetime()
        update_config(overseer_config, config_section, domain,
                      target_url, server_ip, interval_time,
                      scan_time, scan_hash)
        time.sleep(int(interval_time)*60)


def port_scan(host, domain, saved_ip):
    # Set common web ports to scan
    ports = ['80', '443', '8000', '8443', '8080', '5443', '8008', '8888']

    # Configure default timeout period for port scans (float)
    socket.setdefaulttimeout(5)  # was 1.5
    target_ip = socket.gethostbyname(domain)
    if target_ip != saved_ip:
        error_string = (host + " has detected an IP conflict. Original:" +
                        saved_ip + ", New:" + target_ip)
        write_log(host, 'Error', error_string)
        print("[-] Error: " + error_string)
    else:
        information_string = ("[+] Host: " + host +
                              " translates to " + target_ip)
        write_log(host, 'Information', information_string)

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.connect_ex((target_ip, int(port)))
        if result == 0:
            print("\t[+] Host: " + host + " - Port {}:\tOpen".format(port))

        sock.shutdown(1)
        sock.close()
    print("[+] Host: " + host + " port scan has completed.")

    return target_ip


def web_scan(host, url, website_hash):
    # Initiate a scan on the given URL
    try:
        # Set the headers like we are a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)' +
                          ' AppleWebKit/537.36 (KHTML, like Gecko)' +
                          ' Chrome/39.0.2171.95 Safari/537.36'
            }
        response = requests.get(url, headers=headers)
        write_log(host, 'Status Response', 'status_code = ' +
                  str(response.status_code))
        print("[+] Status code for " + host + " = " +
              str(response.status_code))
        if str(response.status_code) == "200":
            scan_hash = hash_website(str(response.json))
            # Run hash checks for the website
            if scan_hash == website_hash:
                print('[+] Website Hash for ' + host + ' is unchanged.')
            else:
                print('[-] Error: Website hash for ' + host + ' has changed!')
                print('\t[-] Scan hash = ' + scan_hash)
                print('\t[-] Stored hash = ' + website_hash)
                write_log(host, 'Error', "Hash collision detected")
            # Run soup checks for the website
            scan_contents = html_diff(host, str(response.text))
            if scan_contents:
                print('[-] Error: Website difference detected for ' +
                      host + "!")
                write_log(host, 'Error', "Difference in HTML")
            return scan_hash
    except requests.exceptions.Timeout:
        error_string = "[-] Error: Timeout..."
        write_log(host, 'Error', error_string)
        print(error_string)
    except requests.exceptions.TooManyRedirects:
        error_string = "[-] Error: Too many redirects..."
        write_log(host, 'Error', error_string)
        print(error_string)
    except requests.exceptions.RequestException as e:
        print("[-] Error: An exception has occurred...")
        exception_args = e.args[0]
        error_string = str(exception_args)
        write_log(host, 'Error', error_string)
        print("[-] Exception Error: " + error_string)
        print(e)


def hash_website(website_contents):
    hash_object = hashlib.sha256(website_contents.encode('utf-8')).hexdigest()
    return hash_object


def html_diff(host, website_contents):
    diff = ""
    # Parse current website contents
    soup = BeautifulSoup(website_contents, "html.parser")
    if os.path.exists("log/" + host + "/scans/" + host + ".temp"):
        with open("log/" + host + "/scans/" +
                  host + ".temp", "w") as current_html:
            current_html.write(str(soup))
            current_html.close()
    else:
        with open("log/" + host + "/scans/" +
                  host + ".temp", "a") as current_html:
            current_html.write(str(soup))
            current_html.close()

    if os.path.exists("log/scans/" + host + ".html"):
        with open("log/scans/" + host + ".html", "r") as previous_html:
            previous_contents = previous_html.readlines()

        with open("log/" + host + "/scans/" + host +
                  ".temp", "r") as current_html:
            current_contents = current_html.readlines()

        diff = difflib.HtmlDiff(previous_contents, current_contents)

        # Clean up. move current html to saved html and close files
        current_html.close()
        previous_html.close()

    open("log/" + host + "/scans/" + host +
         ".html", "w").writelines([l for l in open("log/" + host +
                                                   "/scans/" + host +
                                                   ".temp", "r").readlines()])

    if diff:
        return diff
    else:
        return False
