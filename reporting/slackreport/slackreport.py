from __future__ import unicode_literals
import json

from fame.common.exceptions import ModuleInitializationError
from fame.common.exceptions import ModuleExecutionError

from fame.core.module import ReportingModule


try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

try:
    import WeasyPrint
    HAVE_WeasyPrint = True
except ImportError:
    HAVE_WeasyPrint = False

try:
    from defang import defang
    HAVE_DEFANG = True
except ImportError:
    HAVE_DEFANG = False


class SlackReport(ReportingModule):
    name = "slack_report"
    description = "Post report on Slack when an anlysis if finished."

    config = [
        {
            'name': 'channel',
            'type': 'str',
            'description': 'Slack channel(s) to share the report'
        },
        {
            'name': 'legacy_token',
            'type': 'str',
            'description': 'Legacy Token'
        },        
        {
            'name': 'fame_base_url',
            'type': 'str',
            'default': 'http://localhost:4200',
            'description': 'Base URL:PORT of your FAME instance, as you want it to appear in links.'
        },
        {
            'name': 'fame_api_key',
            'type': 'str',
            'description': 'API key of your FAME instance.'
        },        
        {
            'name': 'proxy',
            'type': 'str',
            'description': 'If you are behind a proxy, please provide it'
        },
        {
            'name': 'pdfreport',
            'type': 'bool',
            'default': False,
            'description': 'Enable PDF report instead of HTML'
        },        
    ]

    def initialize(self):
        if ReportingModule.initialize(self):
            if not HAVE_REQUESTS:
                raise ModuleInitializationError(self, "Missing dependency: requests")

            if not HAVE_DEFANG:
                raise ModuleInitializationError(self, "Missing dependency: defang")

            if not HAVE_WeasyPrint:
                raise ModuleInitializationError(self, "Missing dependency: WeasyPrint")                

            return True
        else:
            return False


    def done(self, analysis):
 
        url_analysis = "{0}/analyses/{1}".format(self.fame_base_url, analysis['_id'])
        
        response = requests.get(url_analysis, stream=True, headers={'X-API-KEY': self.fame_api_key})
        response.raise_for_status()


        if self.pdfreport:
        ### PDF
            HTML(file_obj=response.content).write_pdf('/tmp/test.pdf')
            report = {
              'file': '/tmp/test.pdf'
              }

            payload={
              "title":"{0}_report.pdf".format(analysis['_id']),
              "initial_comment": "Report of {0}\n<{1}/analyses/{2}|See the analysis on FAME>".format(
                defang(', '.join(analysis._file['names'])),
                self.fame_base_url,
                analysis['_id']
                ),
              "token":self.legacy_token, 
              "channels":self.channel, 
            }            
            r = requests.post("https://slack.com/api/files.upload", params=payload, files=report)            
            
        else:
        ### HTML
            report = {
              'file': ("{0}_report.html".format(analysis['_id']), response.content)
              }

            payload={
              "title":"{0}_report.html".format(analysis['_id']),
              "initial_comment": "Report of {0}\n<{1}/analyses/{2}|See the analysis on FAME>".format(
                defang(', '.join(analysis._file['names'])),
                self.fame_base_url,
                analysis['_id']
                ),
              "token":self.legacy_token, 
              "channels":self.channel, 
            }            
            r = requests.post("https://slack.com/api/files.upload", params=payload, files=report)