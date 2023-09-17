from flask import Flask, request, render_template, jsonify
import os, requests

app = Flask(__name__)

# AbuseIPDB API Key (replace with your own)
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY')

# Endpoint to handle IP address submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        abuse_data = get_abuse_data(ip_address)
        whois_data = get_whois_data(ip_address)
        return render_template('result.html', ip=ip_address, abuse=abuse_data, whois=whois_data)
    return render_template('index.html')

# Function to get abuse data from AbuseIPDB API
def get_abuse_data(ip):
    url = f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}'
    headers = {'Key': ABUSEIPDB_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    if not 'data' in data:
        return {
            'score': 'Unknown',
            'users': 'Unknown',
            'reports': 'Unknown',
            'usage': 'Unknown'
        }

    return {
        'score': data['data']['abuseConfidenceScore'],
        'users': data['data']['numDistinctUsers'],
        'reports': data['data']['totalReports'],
        'usage': data['data']['usageType']
    }

# Function to get geolocation and ISP data from ipwho.is API
def get_whois_data(ip):
    url = f'http://ipwhois.app/json/{ip}'
    response = requests.get(url)
    data = response.json()

    if 'success' in data and not data['success']:
        return {
            'location': 'Unknown',
            'timezone': 'Unknown',
            'asn': 'Unknown',
            'isp': 'Unknown'
        }

    return {
        'location': f'{data["city"]}, {data["region"]}, {data["country_code"]}',
        'timezone': data['timezone'],
        'asn': data['asn'],
        'isp': data['isp']
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4600)