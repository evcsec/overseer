# Overseer
A multi-threaded, multi website monitoring tool to monitor and detect changes to website contents, server IP addresses and availability changes. Alerting to be brought into this tool to push alerts in a series of manners, rather than just terminal logging.
This tool is a collaboration between two projects: [Monitaur](https://github.com/evcsec/monitaur) and [WebCompare](https://github.com/evcsec/webcompare).

# Motivation
To build a tool that can detect and alert on website take overs, defacements and downtimes in availability. There are services out there that already do this, but most are not free and open.

# Vision
Future releases of Overseer will include:
- Visual change detection
- Alerts to email, and the ability to push data into monitoring solutions
- Dockerisation
- Monitoring machine statistics (Load, I/O, CPU, Memory, Disk, etc.)
- Project Dashboard (Charts and alert handling)

# Contribution
Everyone is welcome to commit and work with the authors to add functionality. This is a beginner friendly repository, so feel free to contact the authors, or dive straight in.

# How to use
On first execution `python3 overseer.py` you will be asked to add:
| Config Item | Description | Example |
| --- | --- | ---|
| Hostname | The name of the monitor. | google |
| Domain | The website address, without http/https. | google.com |
| Scan interval | The time between scans, in minutes. | 1 |

# Credits
@evcsec
@snags141

# License
GNU General Public License v3