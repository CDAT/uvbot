import requests


url = "http://localhost:9982/slave"


with open("fake_master_push.json") as f:
	contents = f.read()



response = requests.post(url, data=contents, headers={})

print "CODE:",response.status_code
print "TEXT",dir(response),response.text
