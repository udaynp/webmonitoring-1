import json
import requests

username = 'udayradhika'
token = 'c3b7b60e52411292c7c931c66d968a79851750cc'
#token = 'coppergate51'

headers = {'Authorization': 'token ' + token}
repo_name = 'webmonitoring'

login = requests.get('https://api.github.com/user', headers=headers)

#print(login.json())
"""
Could not create Issue url
('Response:', '{"message":"Not Found","documentation_url":"https://developer.github.com/v3"}')

"""
def make_github_issue(title, body=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    headers = {'Authorization': 'token ' + token}

    #login = requests.get('https://api.github.com/user', headers=headers)
    url = requests.get('https://api.github.com/repos/'+username+'/'+repo_name+'/issues',headers=headers)
    # Create an authenticated session to create the issue
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = requests.post(url, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)

#make_github_issue(title="url", body="test", labels="response")




payload = { "title": "response time is more ","body": "response time is more for url1","labels": ["bug"]}

login = requests.post('https://api.github.com/'+'repos/'+username+'/'+repo_name+'/issues', auth=(username,token), data=json.dumps(payload))
print(login.json())



