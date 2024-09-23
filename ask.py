token = input('Enter the API token for OPENAI: ')
work = input('Enter please your hobby: ')

with open('token.txt', 'w') as file:
    file.write(token)

with open('personality.txt', 'w') as file:
    file.write(work)
