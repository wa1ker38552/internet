from flask import render_template
from flask import request
from flask import Flask

from replit import db
import datetime
import time


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
  if request.method == 'GET':
    return render_template('history.html', data=db['history'])
  else:
    db['history'] = request.json['history']
    return {'success': True}

@app.route('/sync')
def sync():
  if time.time()-db['last_synced'] > 10:
    return {
      'internet': False,
      'last_synced': [round(float(i)) for i in str(datetime.timedelta(seconds=time.time()-db['last_synced'])).split(':')]
    }
  else:
    return {
      'internet': True,
      'last_synced': round(time.time()-db['last_synced'])
    }

@app.route('/update', methods=['POST'])
def update():
  if request.headers.get('x-forwarded-for') == 'YOUR IP':
    db['last_synced'] = float(request.form['last_synced'])

  return {'success': True}
    

# db['last_synced'] = time.time()
# db['history'] = []
app.run(host='0.0.0.0', port=8080)
