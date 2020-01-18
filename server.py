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

@app.route("/store_create", methods=["POST"])
def s_create():
    store_name = request.form.get('store_name')
    s = Store(name=store_name)

    if s.save():
        flash(f"Successfully saved {store_name}")
        return redirect(url_for('store'))
    else :
        return render_template('store.html', name=store_name)

@app.route("/warehouse")
def warehouse():
    return render_template('warehouse.html')

@app.route("/warehouse_create")
def w_create():
    warehouse_name = request.form.get('warehouse_name')
    # w = Warehouse(location=warehouse_name, store=#add here)


if __name__ == '__main__':
    app.run()