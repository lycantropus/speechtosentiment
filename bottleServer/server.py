from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/translate/<language>/<sample_rate>/<format>')
def index(language, sample_rate, format):
	return template('future statistics')

run(host='0.0.0.0', port=80)
