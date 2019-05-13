# Overseer
A multi-threaded, multi website monitoring tool to monitor and detect changes to website contents, server IP addresses and availability changes. Alerting to be brought into this tool to push alerts in a series of manners, rather than just terminal logging.
This tool is a collaboration between two projects: [Monitaur](https://github.com/evcsec/monitaur) and [WebCompare](https://github.com/evcsec/webcompare).

# Motivation
To build a tool that can detect and alert on website take overs, defacements and downtimes in availability. There are services out there that already do this, but most are not free and open.

# Vision
Future releases of Overseer will include:
- Dockerisation
- Pretty output
- Read CSV input for configuration
- Rebust output handling
- Create Project Dashboard (Charts, uptime reporting, changes detected over time overview and improved alert handling)

# Contribution
Everyone is welcome to commit and work with the authors to add functionality. This is a beginner friendly repository, so feel free to contact the authors, or dive straight in.

# How to use
On first execution `python3 overseer.py` you will be asked to add the system configuration, then the website configuration.

| Config Item | Description | Example |
| --- | --- | --- |
| Slack Integration Choice | If you want to set up Slack integration for alerting. | 'y' for yes, 'n' for no |
| Email Integration Choice | If you want to set up Email integration for alerting. | 'y' for yes, 'n' for no |
| Webhook Integration Choice | If you want to set up Webhoot integration for alerting. | 'y' for yes, 'n' for no |
| Slack Token | The token created by Slack. | xxxx-tokenid |
| Slack Channel | The name of the slack channel. | overseer |
| SMTP Server | The domain name of the smtp server. | smtp.gmail.com |
| SMTP Username | The username of the smtp server connection. | user@service.com or solo-username |
| Your Email | The email used for sending alerts. | user@service.com |
| Your Recipient Email | The email you want the alerts to be sent to. | user@service.com |
| SMTP Password | The password of the smtp server connection. | *********** |
| ChromeDriver Choice | If you want to use ChromeDriver to take website screenshots. | 'y' for yes, 'n' for no |
| Gecko Driver Choice | If you want to use Gecko Driver to take website screenshots. | 'y' for yes, 'n' for no |
| Gecko Driver or Chrome Driver Location | The location of the executable on the system for either driver. | /Applications/ChromeDriver |
| Hostname | The name of the monitor. | google |
| Domain | The website address, without http/https. | google.com |
| Scan interval | The time between scans, in minutes. | 1 |

# First Run
Some screenshots to assist you throughout executing the first run of Overseer are below, with commentary. You can use the sample configuration files provided in the project as a base, and modify this directly to skip this upfront configuration.
![Start Overseer and follow the prompts, entering your choice of integration](/img/SettingUpEmailConfig.png?raw=true)
![Setup Visual Driver](/img/SettingUpVisualDriver.png?raw=true)
![Setup Your Website Monitor](/img/SettingUpWebsiteConfig.png?raw=true)

Your configuration should look similar to this from the above information.
![System Configuration](/img/SampleSystemConfiguration.png?raw=true)
![Website Configuration](/img/ExampleWebsiteSetup.png?raw=true)


# Credits
@evcsec
@snags141

# License
GNU General Public License v3
