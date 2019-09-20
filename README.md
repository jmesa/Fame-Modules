# FAME modules

* [SlackReport](reporting/slackreport/)

Send a personalized HTML/PDF report of the last scan to the configured Slack channel. Weasyprint based.


* [SlackReportWK](reporting/slackreportwk/)

Send a full PDF report with images of the last scan, to the configured Slack channel.  Wkhtmltopdf based.

* [MailReport](reporting/mailreport/)

Send an HTML/PDF report of the last scan to the configured email account.

## Necesary requirements

Before you clone this repository, previously assure you have the following dependencies installed in your system:

- Weasyprint: 
```
https://weasyprint.readthedocs.io/en/latest/install.html#linux
```
- Wkhtmltopdf:
```
Ex: for Ubuntu 18 (bionic)
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
$ sudo apt install ./wkhtmltox_0.12.5-1.bionic_amd64.deb
```

And check any errors reference available in the READMEs of the modules.