This module send a full PDF / HTML report of the last analysis to the selected Slack channel. Useful if you have isolated teams with no access to the malware lab.

![SlackReport](slackreport_message.png)

## Features

- PDF / HTML report.
- Privacy in communications via compressed reports with password.

## Requeriments

- Requests library
- Slack legacy token
- FAME API key
- For PDF reporting, legacy version of weasyprint 0.42.3 (last version with Python 2 support)
- 7z for compressed reports (usually, allready installed with FAME)

## TODO

- Preliminary proxy support.

## Configuration

- Example configuration

![Config](slackreport_config.png)