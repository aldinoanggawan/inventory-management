import peeweedbevolve # new; must be imported before models
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store # new line

app = Flask(__name__)
app.secret_key = '2klqufb3lsbcd'

@app.before_request # new line
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command() # new
def migrate(): 
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/store")
def store():
    return render_template('store.html')

@app.route("/store_create")
def store_verify():
    store_name = request.args.get('store_name')
    s = Store(name=store_name)

    if s.save():
        flash(f"Successfully saved {store_name}")
        return redirect(url_for('store'))
    else :
        return render_template('store.html', name=store_name)
    # return render_template('store.html', store_name=store_name)


if __name__ == '__main__':
    app.run()