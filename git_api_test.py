import json
import requests

username = 'udayradhika'
token = 'd9a5eee4961340145d256c011e2a311185980c9d'
headers = {'Authorization': 'token ' + token}
repo = 'webmonitoring'

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
    login = 'https://api.github.com/' + 'repos/' + username + '/' + repo+'/issues/'
    # Create an authenticated session to create the issue
    gh_session = requests.Session()
    gh_session.auth = (username, token)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(login, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)

make_github_issue(title="url", body="test", labels="response")
