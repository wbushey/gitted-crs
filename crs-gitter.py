# coding=utf-8
import os
import urllib
import urllib2
import json
import datetime

# Fetches CRS PDFs from sources and commits them to the repo

crs_reports_dir = 'crs-reports/'
open_crs_url = 'https://opencrs.com/api/reports/list.json' 

def openCrsFetcher():
    """
        Fetches CRS PDFs from Open CRS.
    """
    # 1.) Hit https://opencrs.com/api/reports/list.json?key=<KEY>&page=1
    # 2.) Add each record to a dict keyed by date
    # 3.) Goto 1; page++ until fetch is empty
    open_crs_key = os.environ['OPENCRSKEY']
    decoder = json.JSONDecoder()
    page = 0
    reports = dict()
    while True:
        page += 1
        args = urllib.urlencode({'key':open_crs_key,'page':page})
        response = urllib2.urlopen(open_crs_url, args)
        content = respond.read()
        fetched_reports = decoder.decode(content)
        break if not reports
        for fetched_report in fetched_reports:
            rd = datetime.strftime(fetched_report['releasedate'], '%Y-%m-%d')
            if rd in reports:
                reports[rd].append(fetched_report)
            else:
                reports[rd] = [fetched_report]

    # 4.) Starting with oldest, in ascending order:
    #   1.) Download the PDF from the provided URL
    #   2.) saveInGit()
    for report_list in sorted(reports):
        for report in report_list:
            response = urllib2.urlopen(report['download_url'])
            file_content = response.read()
            file_name = '%s.pdf' % report['ordercode']
            saveInGit(file_content, file_name)
        
def saveInGit(file_content, file_name):
    """
        Saves the provided file at the provided file name, then commits the
        save to the repo.
    """
    # 1.) If file_name exists:
    #   1.)overwrite it, 
    #   2.) Commit an update to the file_name
    # else:
    #   1.) Create and save a new file
    #   2.) Commit the new file

