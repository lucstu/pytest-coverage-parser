from xml.dom import minidom
import github
import os

def get_data(filename):
    doc = minidom.parse('./test.xml')

    classes = doc.getElementsByTagName('class')

    coverage = doc.getElementsByTagName('coverage')[0]
    total_lines = coverage.attributes['lines-valid'].value
    covered_lines = coverage.attributes['lines-covered'].value
    total_line_rate = coverage.attributes['line-rate'].value

    total = "Out of {} lines, {} were covered with a rate of {}\n".format(total_lines, covered_lines, total_line_rate)
    
    total += "Filename | Line Rate\n"
    total += "-------- | ---------\n"

    for case in classes:
        name = case.attributes['name'].value
        line_rate = case.attributes['line-rate'].value

        #total += "\nFilename: {}, Line Rate: {}".format(name, line_rate)
        total += name + " | " + line_rate + "\n"
    
    return total

def create_comment():
    data = get_data(os.environ['INPUT_FILE'])
    git = github.Github(os.environ['INPUT_TOKEN'])
    repo = git.get_repo(os.environ['GITHUB_REPOSITORY'])
    sha = os.environ['GITHUB_SHA']

    commit = repo.get_commit(sha)

    commit.create_comment(data)

create_comment()