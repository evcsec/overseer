import smtplib, requests, date
from slackclient import SlackClient
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

def send_slack_message(slack_token, message, channel):
    token = slack_token
    sc = SlackClient(token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='Overseer Bot',
                icon_emoji=':robot_face:')

def send_email(smtp_url, send_from_email, send_to_email, password, error_message): 
    server = smtplib.SMTP(smtp_url, 587)
    server.starttls()
    server.login(send_from_email, password)
    msg = error_message
    server.sendmail(send_from_email, send_to_email, msg)
    server.quit()