This module send a full HTML report of the last analysis to the selected slack channel (or channels). Useful if you have isolated teams with no access to the malware lab.

- Preliminary poryx support.
- PDF report, instead of HTML based.

It was based on previous slack module https://github.com/certsocietegenerale/fame_modules/blob/master/reporting/slack.py

## Requeriments

- requests
- slack legacy token
- channel(s)
- FAME API key

## Configuration

- For localhost instances, please use localhost:port

	> http://localhost:4200