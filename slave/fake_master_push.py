import requests
import hmac
import hashlib


url = "http://crunchy.llnl.gov:9982/slave"

secret = raw_input("Enter your webhook secret")
if secret == "":
  with open("github_secret.txt") as f:
    secret = f.read().strip()
    print "SECRET:",secret

with open("fake_data.json") as f:
	contents = f.read()

print type(secret)
print hashlib.sha1

h = hmac.new(secret, contents, hashlib.sha1)


response = requests.post(url, data=contents, headers={
      "BOT-Signature": "sha1=%s" % h.hexdigest(),
      })

print "CODE:",response.status_code
print "TEXT",dir(response),response.text
