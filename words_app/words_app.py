# Write your code here
import sys
sys.path.append('/Users/sudarshannagesh/miniconda3/lib/python3.12/site-packages')
import datetime
import tkinter as tk
import requests
import os
current_folder = os.path.dirname(__file__)
sys.path.append(current_folder)

word_idx_fl = os.path.join(current_folder, "word_idx.txt")
words_l_fl = os.path.join(current_folder, "words.txt")

with open(words_l_fl, 'r') as f:
	words_str = f.read()
	words_l = words_str.split('\n')
with open(word_idx_fl, 'r') as f:
	word_idx = int(f.read()) + 1

meanings_l = []
if word_idx < len(words_l):
    word = words_l[word_idx]
    with open(word_idx_fl, 'w') as f:
        f.write(str(word_idx))
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/{0}".format(word)
    tr = 0
    while tr < 5:
        response = requests.get(url)
        tr += 1
        if response.ok:
            break
    if response.ok:
        resp_json = response.json()[0]
        for idx, meaning in enumerate(resp_json["meanings"]):
            meaning_str = ''
            meaning_str += 'meaning: {0} \n'.format(idx + 1)
            meaning_str += 'partOfSpeech: {0} \n'.format(meaning['partOfSpeech'])
            meaning_str += 'definition(s): \n'
            for defn in meaning['definitions']:
                meaning_str += '\t - {0} \n'.format(defn['definition'])
            if len(meaning['synonyms']):
                meaning_str += 'synonyms: {0} \n'.format(','.join(meaning['synonyms']))
            if len(meaning['antonyms']):
                meaning_str += 'antonyms: {0} \n'.format(','.join(meaning['antonyms']))
            meanings_l.append(meaning_str)
    else:
        meaning_str = 'not getting resp'
        meanings_l.append(meaning_str)
else:
    word = 'word_idx seems > words_l'
    meaning_str = ''
    meanings_l.append(meaning_str)

window = tk.Tk()
word_frame = tk.Frame(master=window, relief=tk.RAISED, border=3, pady=3)
word_label = tk.Label(master=word_frame, text='Word: {0} \n Date: {1}'.format(word, datetime.date.today()))
meaning_frame = tk.Frame(master=window, relief=tk.RAISED, border=3, pady=3)
meaning_sub_frames = []
meaning_labels = []
for idx, meaning_str in enumerate(meanings_l):
    meaning_sub_frame = tk.Frame(master=meaning_frame, relief=tk.RAISED,
                                 border=2, padx=2, pady=2)
    meaning_sub_frames.append(meaning_sub_frame)
    meaning_label = tk.Label(master=meaning_sub_frames[idx], text=meaning_str, wraplength='600px')
    meaning_labels.append(meaning_label)
word_frame.grid(row=0, column=0)
meaning_frame.grid(row=0, column=1)
word_label.pack()
for idx in range(len(meanings_l)):
    meaning_sub_frames[idx].grid(row=idx, column=0)
    meaning_labels[idx].pack()
tk.mainloop()
