from flask import Flask, render_template, request
import Randomforest
app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def interface():
	if request.method == 'POST':
		# result = "Hellow World"
		value = request.form.items()
		for key, url in value:
			result = Randomforest.Accuracy_Randomforest(url)
		return render_template('interface.html', result = result)
	return render_template('interface.html', result = "")

if __name__ == '__main__':
   app.run(debug = True)