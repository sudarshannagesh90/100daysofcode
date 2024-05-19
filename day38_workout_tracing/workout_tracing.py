import sys
import requests
import datetime
import time

API_KEY = "TO_BE_FILLED"
APP_ID = "TO_BE_FILLED"
DATE_OF_BIRTH = 'TO_BE_FILLED'
SHEETY_API_ENDPOINT = 'https://api.sheety.co/'\
'a0a97702616bbfa6796b8c132cef5a8d/myWorkouts/workouts'
SHEETY_HEADERS = {'Authorization': 
'Basic c3VkYXJzaGFubmFnZXNoOmtkbmRsa2V3NzgzNGtmb2Vq'}

date_now = datetime.datetime.now().strftime('%Y-%m-%d')
age = int(date_now[:4]) - int(DATE_OF_BIRTH[:4])
if date_now[4:] < DATE_OF_BIRTH[4:]:
    age -= 1

headers = {"x-app-id": APP_ID, "x-app-key": API_KEY}
did_you_exercise_today = \
    input('Did you exercise today? Y or N: '
          '(press N if already entered response for today)').strip().lower()
if did_you_exercise_today == 'y':
    query = input('What did you exercise today?')
else:
    sys.exit('Ok, exiting.')

api_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
exercise_paramsq = {
    'query': query,
    'weight_kg': 75,
    'height_cm': 174,
    'age': age,
    'gender': 'TO_BE_FILLED'
}

idx = 0
json_data = None
while idx < 5:
    try:
        response = requests.post(api_endpoint, json=exercise_paramsq,
                                 headers=headers)
        response.raise_for_status()
        json_data = response.json()
        time_now = datetime.datetime.now()
        exercise_params = {
        'workout': {
        'date': time_now.strftime('%d/%m/%Y'),
        'time': time_now.strftime('%H:%M:%S'),
        'exercise': json_data['exercises'][0]['name'],
        'duration': json_data['exercises'][0]['duration_min'],
        'calories': json_data['exercises'][0]['nf_calories']
    	}}
        break
    except Exception as e:
        print('Exception: ', e)
        idx += 1
        time.sleep(60)
if json_data is None:
    sys.exit('Didn\'t recieve a response')

idx = 0
json_data = None
while idx < 5:
    try:
        response = requests.post(SHEETY_API_ENDPOINT, json=exercise_params,
                                 headers=SHEETY_HEADERS)
        response.raise_for_status()
        json_data = response.json()
        break
    except Exception as e:
        print('Exception: ', e)
        idx += 1
        time.sleep(60)

if json_data is None:
    sys.exit('Didn\'t recieve a response')
else:
    print(json_data)
print('Exiting.')
