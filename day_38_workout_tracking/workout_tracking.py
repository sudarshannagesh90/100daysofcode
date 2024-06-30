import sys
import requests
import datetime
import time

API_KEY = "6a7befbfb4ec446a4bce26d1a16fc214"
APP_ID = "61e42ecc"

headers = {"x-app-id": APP_ID,
           "x-app-key": API_KEY}

did_you_exercise_today = \
    input('Did you exercise today? Y or N: '
          '(press N if already entered response for today)').strip().lower()
if did_you_exercise_today == 'y':
    query = input('What did you exercise today?')
else:
    sys.exit('Ok, exiting.')

api_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
exercise_params = {
    'query': query,
    'weight_kg': 75,
    'height_cm': 174,
    'age': 33,
    'gender': 'Male'
}

idx = 0
json_data = None
while idx < 5:
    try:
        response = requests.post(api_endpoint, json=exercise_params,
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
    	}
	}
        break
    except Exception as e:
        print('Exception: ', e)
        idx += 1
        time.sleep(60)
if json_data is None:
    sys.exit('Didn\'t recieve a response')

api_endpoint = 'https://api.sheety.co/a0a97702616bbfa6796b8c132cef5a8d/myWorkouts/workouts'
headers = {'Authorization': 'Basic c3VkYXJzaGFubmFnZXNoOmtkbmRsa2V3NzgzNGtmb2Vq'}
idx = 0
json_data = None
while idx < 5:
    try:
        response = requests.post(api_endpoint, json=exercise_params,
                                 headers=headers)
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
# sudarshannagesh    # username
# kdndlkew7834kfoej  # password
# Authorization: Basic c3VkYXJzaGFubmFnZXNoOmtkbmRsa2V3NzgzNGtmb2Vq
# for id in range(100, 2, -1):
#     api_endpoint = 'https://api.sheety.co/a0a97702616bbfa6796b8c132cef5a8d/myWorkouts/workouts/{0}'.format(id)
#     idx = 0
#     while idx < 5:
#         try:
#             response = requests.delete(api_endpoint, headers=headers)
#             response.raise_for_status()
#             break
#         except Exception as e:
#             print('Exception: ', e)
#             idx += 1
#             time.sleep(60)
