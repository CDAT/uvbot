import requests


url = "http://localhost:9982/slave"

secret = raw_input("Enter your webhook secret")
if secret == "":
  with open("github_secret.txt") as f:
    secret = f.read().strip()
    print secret

with open("fake_master_push.json") as f:
	contents = f.read()



response = requests.post(url, data=contents, headers={
      "BOT-Signature": "sha1=%s" % h.hexdigest(),
      })

print "CODE:",response.status_code
print "TEXT",dir(response),response.text
