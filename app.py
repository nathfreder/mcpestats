from flask import Flask, render_template, request
import mcstats
import validators

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ping')
def ping():
    host = request.args.get('host')
    port = request.args.get('port')
    if not port.isdigit():
        return 'error: port is not digit'
    if not validators.domain(host):
        return 'error: invalid hostname'
    try:
        with mcstats.mcstats(host, int(port), timeout=10) as data:
            full_address = host + ':' + port
            return render_template('ping.html', fulladdress=full_address, data=data)
    except mcstats.main.StatsNetworkError as err:
        return 'network error: ' + err.__str__()


if __name__ == '__main__':
    app.run()
