from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def info():
    return render_template('info.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/timeout')
def timeout():
    return render_template('timeout.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.errorhandler(404)
def page_not_find(error):
    return 'Opps, page you requested is not exsit yet', 404


"""
@app.route('/a')
def a():
	return redirect(url_for('hello_world'))

@app.route('/b')
def b():
	start = '<img src = "'
	end = '">'
	url = url_for('static', filename = 'vmask.jpg')
	return start+url+end, 200

@app.route('/c', methods = ['GET', 'POST'])
def c():
	if request.method == 'GET': 
		page = '''
		<html><body>
			<form action = '' method = 'POST' name = 'form'>
			<label for='name'>Name:<label>
			<input type = 'text' name = 'name' id = 'name'/>
			<input type = 'submit' name = 'submit' id = 'submit'/>
			</form>
		</body></html>
		'''
		return page
	else: 
		print(request.form)
		name = request.form['name']
		return 'Hello ' +  name

@app.route('/')
@app.route('/d/<name>') #construct page with variables
def d(name=None): 
	return render_template('hello.html', name = name)

@app.route('/e/') #construct html with parameters
def e():
	name = request.args.get('name','an alter one when name is not provide')
	return 'Hello %s' %name

@app.route('/f/', methods = ['GET', 'POST']) # get files than para/vari
def f():
	if request.method == 'POST':
		f = request.files['datafile']
		print(f)
		f.save('static/uploads/upload.png')
		return 'File Uploaded'
	else: 
		page='''
			<html><body>
				<form action = '' method = 'post' name = 'form' enctype = 'multipart/form-data'>
				<input type = 'file' name = 'datafile'/>
				<input type = 'submit' name = 'submit' id = 'submit'/>
				</form>
			</body></html>
			'''
		return page, 200

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)
"""
