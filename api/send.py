
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/send', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        
        to = data.get('to')
        sender = data.get('sender')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([to, sender, subject, message]):
            return jsonify({'success': False, 'error': 'Missing fields'}), 400
        
        payload = {
            'to': to,
            'from': sender,
            'subject': subject,
            'message': message
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r = requests.post(
            'https://api.proxynova.com/v1/send_email',
            data=payload,
            headers=headers,
            timeout=20
        )
        
        if r.status_code == 200:
            return jsonify({'success': True, 'message': 'Email sent'})
        else:
            return jsonify({'success': False, 'error': f'Status {r.status_code}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
