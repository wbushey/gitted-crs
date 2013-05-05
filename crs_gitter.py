# coding=utf-8
import os
import subprocess
import urllib
import urllib2
import json
import datetime

# Fetches CRS PDFs from sources and commits them to the repo

crs_reports_dir = 'crs-reports/'
open_crs_url = 'https://opencrs.com/api/reports/list.json' 
GIT_USER_NAME = "Bill Bushey"
GIT_USER_EMAIL = "wbushey@gmail.com"

def openCrsFetcher(page_limit=float("infinity")):
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
    while page < page_limit:
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
    for report_date in sorted(reports):
        for report in reports(report_date):
            response = urllib2.urlopen(report['download_url'])
            file_content = response.read()
            file_name = '%s.pdf' % report['ordercode']
            saveInGit(file_content, file_name, report_date)
        
def saveInGit(file_content, file_name, report_date):
    """
        Saves the provided file at the provided file name, then commits the
        save to the repo.
    """
    file_path = crs_reports_dir + file_name
    existed = os.path.isfile(file_path) 
    if existed:
        # TODO Check that this specific version of this file isn't already
        # in the comment history
        pass
    with f = open(file_path, 'w'):    
    f.write(file_content)
    f.close()
    gitAdd(file_name, crs_reports_dir)
    if existed:
        # TODO Set the commit date to be the CRS release date
        gitCommit(file_name, crs_reports_dir, '%s was updated' % file_name,
                    report_date)
    else:
        gitCommit(file_name, crs_reports_dir, 'Added %s' % file_name)
        
        
        
    # 1.) If file_name exists:
    #   1.)overwrite it, 
    #   2.) Commit an update to the file_name
    # else:
    #   1.) Create and save a new file
    #   2.) Commit the new file

def gitAdd(filename, repo_dir):
    """                                                                         
        Adds the provided filename to the git stage,
    """
    cmd = ['git',
            '-c', 'user.name=\'' + GIT_USER_NAME + '\'',
            '-c', 'user.email=\'' + GIT_USER_EMAIL + '\'',
            'add', filename]
    subprocess.check_call(cmd, cwd=REPO_DIR)

def gitCommit(filename, repo_dir, message, date=None):
    """                                                                         
        Commits whatever is currently staged
    """
    cmd = ['git',
            '-c', 'user.name=\'' + GIT_USER_NAME + '\'',
            '-c', 'user.email=\'' + GIT_USER_EMAIL + '\'',
            'commit', '-m', message]
    if date:
        cmd.append('--date="%s"' % date.strftime("%m/%d/%Y"))
    subprocess.check_call(cmd, cwd=REPO_DIR)
