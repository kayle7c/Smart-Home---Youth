import requests

if __name__ == '__main__':
    parms = {
        'username': '<YOUR USERNAME>',
        'password': '<YOURE PASSWOER>',
    }
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.post('http://127.0.0.1:5000/work',params=parms,headers=headers,verify=False)
    print(resp.json())