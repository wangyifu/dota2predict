import requests
content = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/?key=C13E4166CAAA9955FF78739B58CCF5D8").json()
print(content)
#print("status: " + str(content.status))
#newdata = str(content.data).replace('\\t', '').replace('\\n', '')
#print(newdata)
#json.loads(newdata)
