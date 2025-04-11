import requests

#testing Tidy API, we will use this string to test
req = {"BotID": "5", "BotIP": "212.102.59.80", "BotName": "Chris", "BotPub": "aEzkaYh2L3HspVAnigmlCO1qxlFUCgLPjcLdG4VLEotCus6ldIHAroXbMkS5aim3bamSdgslF9ATadEnJKmOm5DGaQbpJ0QIwpfXdXpNpY8J99zJiWsVXsXHFpG4wahv6yBkD1b9PEaY1rvhXMG5U4MjgyqzIl1idv3ykjk66alD9i7G5VYzZU0luAIjo7YcNguw2Ts1uyUe5EmPTWTAC6gUxujUkdQLsb8pDAYqfRwuMhVWhIGrp53wJtdtsxnCLPzUhydjASSjlgEr1sUyZZsGOlBpLN4BmnQmTuwnmmEACM6FvZEBDM1WrUGsf6JrZua84t1inCG36XDoeBJvxb7Ybmayr0p4je9o9C6ajw48novNHELBQnVl638Qo2ntGUcvqzaKaou3t5usIhYWFY7MJmUmtfdL0bMAnjZ8FGzMuC2Fo5FXD9Ca1CgVeK8nio4F63cv5PQT04jNgcqOWmu6J8FlvWU2i3oYEvLJh8v0EDkhm8JkLomVGQEEElWXhyAi8E8pqhuSRupRD3iUem52sTpyNq", "DataType": "URL", "SiteAddress": "https://gamespot.com", "LocalID": "215", "SiteIcon": "test", "Site_Notes": "test", "Title": "Gamespot", "Keywords": "Video Games", "Description": "Video game news", "PagePath": "https://gamespot.com"}
server = "https://212.102.59.80:251"

resp = requests.post(server, json=req, verify=False)

print(resp.status_code)
print(resp.text)