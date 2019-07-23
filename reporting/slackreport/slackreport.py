from __future__ import unicode_literals
import json
import os

from fame.common.exceptions import ModuleInitializationError
from fame.common.exceptions import ModuleExecutionError

from fame.core.module import ReportingModule
from fame.common.config import fame_config
from fame.core.config import Config


try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

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
            'name': 'url',
            'type': 'str',
            'description': 'Incoming webhook URL.'
        },
        {
            'name': 'channel',
            'type': 'str',
            'description': 'Slack channel to share the report'
        },
        {
            'name': 'legacy_token',
            'type': 'str',
            'description': 'Legacy Token'
        },        
        {
            'name': 'fame_base_url',
            'type': 'str',
            'description': 'Base URL of your FAME instance, as you want it to appear in links.'
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
    ]

    def initialize(self):
        if ReportingModule.initialize(self):
            if not HAVE_REQUESTS:
                raise ModuleInitializationError(self, "Missing dependency: requests")

            if not HAVE_DEFANG:
                raise ModuleInitializationError(self, "Missing dependency: defang")

            return True
        else:
            return False


    def done(self, analysis):
 
        ### use localhost
        fame_local_instance = "http://localhost:4200"
        url_analysis = "{0}/analyses/{1}".format(fame_local_instance, analysis['_id'])
        #url_analysis = "{0}/analyses/{1}".format(self.fame_base_url, analysis['_id'])

        response = requests.get(url_analysis, stream=True, headers={'X-API-KEY': self.fame_api_key})
        response.raise_for_status()

        try:
            print fame_config.api_key
        except ModuleExecutionError, e:
            self.log("error", fame_config.api_key)
            self.log("debug", fame_config.api_key)

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