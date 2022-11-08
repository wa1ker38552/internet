from datetime import datetime
from threading import Thread
import requests
import time
import json

internet_on = True

def history():
    while True:
        with open('tracker.json', 'r') as file:
            try:
                requests.post('https://xxxx.xxxx.repl.co/history', json={'history': json.loads(file.read())})
            except requests.exceptions.ReadTimeout: pass
            except requests.exceptions.ConnectionError: pass
        time.sleep(60)

        
Thread(target=history).start()
while True:
    try:
        requests.post('https://xxxx.xxxx.repl.co/update', data={"last_synced": time.time()}, timeout=5)
        if internet_on is False:
            data = json.loads(open('tracker.json', 'r').read())
            with open('tracker.json', 'w') as file:
                data.append({
                    'internet': True,
                    'time': datetime.strftime(datetime.now(), "%H:%M:%S")
                })
                file.write(json.dumps(data, indent=2))
        internet_on = True
    except requests.exceptions.ReadTimeout: pass
    except requests.exceptions.ConnectionError:
        # internet shutoff
        if internet_on is True:
            data = json.loads(open('tracker.json', 'r').read())
            with open('tracker.json', 'w') as file:
                data.append(({
                    'internet': False,
                    'time': datetime.strftime(datetime.now(), "%H:%M:%S")
                }))
                file.write(json.dumps(data, indent=2))
        internet_on = False
            
    print(f'{time.time()} Refreshing...')
    time.sleep(5)
