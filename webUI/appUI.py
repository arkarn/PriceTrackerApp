from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@mysqldb:3306/proddb' #'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    prod_name = db.Column(db.String(64), primary_key=True)
    prod_url = db.Column(db.String(250), index=True)
    price_thresh = db.Column(db.Float, index=True)

db.create_all()

@app.route('/addproduct', methods=['POST'])
def addproduct():
    prod_name = request.form['prod_name']
    prod_url = request.form['prod_url']
    price_thresh = request.form['price_thresh']
    prod = Product(prod_name=prod_name, prod_url=prod_url, price_thresh=price_thresh)
    db.session.add(prod)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deleteproduct/<prodname>', methods=['GET'])
def deleteproduct(prodname):
    Product.query.filter_by(prod_name=prodname).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
def index():
    prods = Product.query
    return render_template('basic_table.html', title='Amazon Price Tracker',
                           prods=prods)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", debug=True)

