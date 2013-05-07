# coding=utf-8
import os
import subprocess
import urllib
import urllib2
import json
import datetime as dt
from sh import git

# Fetches CRS PDFs from sources and commits them to the repo

crs_reports_dir = './crs-reports'
open_crs_url = 'https://opencrs.com/api/reports/list.json' 
os.environ['GIT_AUTHOR_NAME'] = "Congressional Research Service"
# One day we should put an email for CRS here
os.environ['GIT_COMMITTER_NAME'] = "Bill Bushey"
os.environ['GIT_COMMITTER_EMAIL']= "wbushey@gmail.com"

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
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(args)
        response = urllib2.urlopen('%s?%s' % (open_crs_url, args))
        content = response.read()
        fetched_reports = decoder.decode(content)
        if not fetched_reports: break
        for fetched_report in fetched_reports:
            rd = dt.datetime.strptime(fetched_report['releasedate'], '%Y-%m-%d')
            if rd in reports:
                reports[rd].append(fetched_report)
            else:
                reports[rd] = [fetched_report]

    # 4.) Starting with oldest, in ascending order:
    #   1.) Download the PDF from the provided URL
    #   2.) saveInGit()
    for report_date in sorted(reports):
        for report in reports[report_date]:
            print "Getting %s" % report['ordercode']
            response = urllib2.urlopen(report['download_url'])
            file_content = response.read()
            file_name = '%s.pdf' % report['ordercode']
            saveInGit(file_content, file_name, report_date)
        
def saveInGit(file_content, file_name, report_date):
    """
        Saves the provided file at the provided file name, then commits the
        save to the repo.
    """
    file_path = "/".join(crs_reports_dir,file_name)
    existed = os.path.isfile(file_path) 
    if existed:
        # TODO Check that this specific version of this file isn't already
        # in the comment history
        pass
    with open(file_path, 'w') as f:    
        f.write(file_content)
        f.close()
    gitAdd(file_name, crs_reports_dir)
    if existed:
        # TODO Set the commit date to be the CRS release date
        gitCommit(file_name, crs_reports_dir, '%s was updated' % file_name,
                    report_date)
    else:
        gitCommit(file_name, crs_reports_dir, 'Added %s' % file_name,
                    report_date)
        
        
        
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
    file_path = "%s/%s" % (repo_dir, filename)
    git("add", file_path)

def gitCommit(filename, repo_dir, message, date=None):
    """                                                                         
        Commits whatever is currently staged
    """
    args = ['commit', '-m', message]
    if date:
        args.append('--date="%s"' % date.strftime("%Y-%m-%d 00:00:00"))
    git (args)

if __name__ == '__main__':
    openCrsFetcher()
