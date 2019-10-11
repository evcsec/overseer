import smtplib
import requests
from slack import WebClient
from .date import get_current_datetime
from .logger import write_log


def send_web_alert(url, error_message):
    current_time = get_current_datetime()
    try:
        request = requests.post(url, data={
            'Error': error_message,
            'Action': 'error',
            'Time': current_time
        })
        if request.status_code != '200':
            return 0
        else:
            return 1
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


def send_slack_message(system_config, message):
    slack_token = system_config.systemconfig.get('Slack', 'slack_token')
    channel = system_config.systemconfig.get('Slack', 'channel')

    sc = WebClient(slack_token)
    sc.api_call('chat.postMessage', channel=channel,
                text=message, username='Overseer Bot',
                icon_emoji=':robot_face:')


def send_email(system_config, error_message):
    smtp_url = system_config.systemconfig.get('Email', 'smtp_url')
    send_from_email = system_config.systemconfig.get('Email',
                                                     'send_from_email')
    send_to_email = system_config.systemconfig.get('Email', 'send_to_email')
    username = system_config.systemconfig.get('Email', 'username')
    password = system_config.systemconfig.get('Email', 'password')

    server = smtplib.SMTP(smtp_url, 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(send_from_email, send_to_email, error_message)
    server.quit()
