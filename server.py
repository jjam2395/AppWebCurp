from flask import Flask, render_template
app=Flask(__name__,stati_url_path="/static")

@app.route('/')
def index():
	return render_template("hola a todos",name=name)