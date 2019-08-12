from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
#from forms import CustomerForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

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

@app.route('/')
def home():
    return render_template('home.html')
	
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

	
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
			#customer = customers(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
		 
			if customer.id == 0 :
				db.session.edit(customer)
			else :
				db.session.add(customer)

			db.session.commit()
			flash('Record was successfully added')
			return redirect(url_for('show_all'))
			
	
	

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)