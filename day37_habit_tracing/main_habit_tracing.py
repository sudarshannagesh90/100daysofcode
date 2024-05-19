import requests
import datetime
import tkinter.messagebox as msg
import tkinter as tk
import sys

USERNAME = 'TO_BE_FILLED'
TOKEN = 'TO_BE_FILLED'
GRAPHID = 'TO_BE_FILLED'
pixela_endpoint = 'https://pixe.la/v1/users'
headers = {
    'X-USER-TOKEN': TOKEN
}


def submit():
    global number_of_pages
    entry_text = entry.get()
    try:
        number_of_pages = int(entry_text)
        number_of_pages = str(number_of_pages)
        msg.showinfo(title="{0} pages read".format(number_of_pages),
                     message="Please close the reading window.")
    except:
        msg.showinfo(title="Couldnt convert to int",
                     msg="Couldn't convert to int")


number_of_pages = None
window = tk.Tk()
window.config()
window.title("Reading")
label = tk.Label(master=window, text='Pages read yesterday:',
                 width=15)
entry = tk.Entry(master=window, width=5)
button = tk.Button(master=window, command=submit, text='Submit',
                   width=5)
label.grid(row=0, column=0, padx=2)
entry.grid(row=0, column=1, padx=2)
button.grid(row=0, column=2, padx=2)
window.mainloop()
if number_of_pages is None:
    sys.exit('Didn\'t recieve number_of_pages')

post_endpoint = f'{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}'
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
post_config = {
    'date': yesterday.strftime('%Y%m%d'),
    'quantity': number_of_pages
}
idx = 0
while idx < 5:
    try:
        response = requests.post(url=post_endpoint, json=post_config,
                                 headers=headers)
        json_data = response.json()
        if 'message' in json_data.keys() and \
                json_data['message'] == 'Success.' and \
                'isSuccess' in json_data.keys() and \
                json_data['isSuccess'] == True:
            msg.showinfo(title="Success",
                         message="{0}.html".format(post_endpoint))
            break
        else:
            response_text = response.text
            raise Exception("response_text: {0}".format(response_text))
    except Exception as e:
        msg.showinfo(title='Request didnt go through',
                     message="{0}".format(e))
        idx += 1
