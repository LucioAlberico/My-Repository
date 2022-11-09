import requests
import re


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

params = {
    'name': 'censored',
}


response1 = requests.get('URL OBJETIVO', params=params, headers=headers)
print("StatusCode:", response1.status_code)
#print(response1.text)
if int(response1.status_code) != 200: #502 BAD GATEWAY --> ERROR
    print("ERROR, STATUS CODE RESPONSE 1:", response1.status_code)
    quit()

a = re.search('csrf:".*"}]', response1.text).group(0)
a = a[:a.index('}')]
csrf = a.replace('csrf:"', "").replace('"', "")
print(csrf)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'censored',
    'Referer': 'censored',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'x-csrf-token': csrf,
    'x-troov-web': 'com.troov.web',
}

json_data = {
    'standaloneServiceName': 'censored',
    'sessionId': None,
}

response2 = requests.post('API OBJETIVO', headers=headers, json=json_data)
if int(response2.status_code) != 200: #429 TOO MANY REQUESTS --> ERROR
    print("ERROR, STATUS CODE RESPONSE 2:", response2.status_code)
    time.sleep(randint(7,15))
    quit()
j = response2.json()
#print(j)

response0 = requests.get(f"API OBJETIVO", headers=headers, json=j) #f string used to format the url of the api
#Session ID was needed to continue. Session ID was in the variable j.
print("StatusCode:", response0.status_code)
print(response0.text)

if response0.text == "STRING OBJETIVO":
    print("")
else:
    continue

#GUARDA CON ESTE ENDPOINT
#response3 = requests.post('https://api.consulat.gouv.fr/api/team/6230a68c9614bcf9d95f1aa5/reservations-session/632633289789fc41d0150e61/update-step-value', headers=headers, json=json_data)
#print("StatusCode:", response3.status_code)
#print(response3.text)
