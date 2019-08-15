from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
#from forms import CustomerForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class products(db.Model):
	id = db.Column('product_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	code = db.Column(db.String(15))	

	def __init__(self, code, name):
		self.name = name
		self.code  = code
		self.id = 0
			
class customers(db.Model):
	id = db.Column('customer_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	city = db.Column(db.String(50))
	addr = db.Column(db.String(200)) 
	pin = db.Column(db.String(10))

	def __init__(self, name, city, addr,pin):
		self.name = name
		self.city = city
		self.addr = addr
		self.pin = pin
		self.id = 0

@app.route('/')
def home():
    return render_template('home.html')
	
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/product/")
def show_all_product():
	#return 'Ini Product'
	return render_template("show_all_product.html")

@app.route("/new_product/")
def new_product():
	#return 'Ini Product'
	return render_template("product.html")
		
@app.route('/customer/')
def show_all():
	return render_template('show_all.html', customers = customers.query.all() )
	#return render_template('show_all.html')

@app.route('/editcustomer', methods = ['GET', 'POST'])
def editcustomer():
	if request.method == 'GET':
		if request.args.get('id'):			
			obj=customers.query.filter_by(id=request.args.get('id')).one()
			return render_template('new.html', customer = obj)

	return 'No Data Edited'


@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'GET':
		if request.args.get('id'):
			obj=customers.query.filter_by(id=request.args.get('id')).one()
			#return request.args.get('isdelete')

			if request.args.get('isdelete') == '1':					
				db.session.delete(obj)
				db.session.commit()
				flash('Record was successfully deleted')
				return redirect(url_for('show_all'))
			else :
				return render_template('new.html', customer = obj)			
		else :			
			return render_template('new.html', customer = customers('','','',''))
	
	
	if request.method == 'POST':
		customer = customers(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
		if not request.form['name'] or not request.form['city'] or not request.form['addr']:
			if not request.form['name']:
				flash('Please enter Name', 'error')

			if not request.form['city']:
				flash('Please enter City', 'error')
			
			if not request.form['addr']:
				flash('Please enter Address', 'error')
					
			return render_template('new.html', customer=customer)
		else:
			customer = customers(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
			customer.id = request.form['id']
						
			if customer.id == '0' :
				obj = db.session.query(customers).order_by(customers.id.desc()).first()
				
				if obj :
					customer.id = obj.id + 1
				else :
					customer.id = 1

				db.session.add(customer)
				db.session.commit()
				flash('Record was successfully added')
				return redirect(url_for('show_all'))
			else :
				obj=customers.query.filter_by(id=customer.id).first()
				obj.addr 	= customer.addr
				obj.name 	= customer.name
				obj.city 	= customer.city
				obj.pin 	= customer.pin

				db.session.commit()

				flash('Record was successfully Edited')
				return redirect(url_for('show_all'))

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)
	app.run(host="0.0.0.0",port=5000)