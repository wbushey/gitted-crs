# coding=utf-8

# Fetches CRS PDFs from sources and commits them to the repo

def openCrsFetcher():
    """
        Fetches CRS PDFs from Open CRS.
    """
    # 1.) Hit https://opencrs.com/api/reports/list.json?key=<KEY>&page=1
    # 2.) Add each record to a dict keyed by date
    # 3.) Goto 1; page++ until fetch is empty
    # 4.) Starting with oldest, in ascending order:
    #   1.) Download the PDF from the provided URL
    #   2.) saveInGit()
    
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

