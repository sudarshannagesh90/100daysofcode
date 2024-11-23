import sys
sys.path.append('/Users/sudarshannagesh/miniconda3/lib/python3.12/site-packages')
import requests
import datetime
import time
import tkinter as tk
import tkinter.messagebox as msg

API_KEY = "6a7befbfb4ec446a4bce26d1a16fc214"
APP_ID = "61e42ecc"

headers = {"x-app-id": APP_ID,
           "x-app-key": API_KEY}

def submit():
    global query 
    query = entry.get()
    msg.showinfo(title='Ok', message='Please close the window.')

did_you_exercise_today = msg.askyesno('Exercise', 'Did you exercise today? (Press No if already entered response for today)')

# did_you_exercise_today = \
#     input('Did you exercise today? Y or N: (press N if already entered response for today)').strip().lower()
if did_you_exercise_today:
    #query = input('What did you exercise today?')
    window = tk.Tk()
    label = tk.Label(master=window, text='What did you exercise today?')
    entry = tk.Entry(master=window)
    submit_button = tk.Button(master=window, command=submit, text='Submit')
    label.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    submit_button.grid(row=1, column=0, padx=50)
    window.mainloop()
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
