import peeweedbevolve # new; must be imported before models
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store, Warehouse # new line

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
        return render_template('store.html', name=store_name, errors=s.errors)


@app.route("/warehouse")
def warehouse():
    store_list = Store.select()
    return render_template('warehouse.html', store_list=store_list)

@app.route("/warehouse_create", methods=["POST"])
def w_create():
    store_id = Store.get_by_id(request.form.get('s_id'))
    warehouse_name = request.form.get('warehouse_name')
    w = Warehouse(location=warehouse_name, store=store_id)

    if w.save():
        flash(f"Successfully saved {warehouse_name}")
        return redirect(url_for('warehouse'))
    else:
        return render_template('warehouse', location=warehouse_name)


@app.route("/stores")
def stores():
    stores_list = Store.select()
    return render_template('stores.html', stores_list=stores_list)

@app.route("/stores/<id>/delete", methods=["POST"])
def store_delete(id):
    s_del = Store.get_by_id(id)
    query = Warehouse.delete().where(Warehouse.store_id == id)
    query.execute()

    if s_del.delete_instance():
        flash(f"Successfully deleted {s_del.name}")
        return redirect(url_for('stores'))
    else:
        return render_template('stores')


@app.route("/store/<int:sid>")
def id_store(sid):
    s = Store.get_by_id(sid)
    return render_template('sid.html', s=s)

@app.route("/store/<storeid>/update", methods=["POST"])
def store_update(storeid):
    s_new = Store.get_by_id(storeid)
    s_new.name = request.form.get('edit_store_name')

    if s_new.save():
        flash(f"Successfully saved {s_new.name}")
        return redirect(url_for('id_store', sid=storeid))
    else:
        return render_template('id_store')

if __name__ == '__main__':
    app.run()