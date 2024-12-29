from flask import Flask, render_template,redirect,request, session,url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import pytz



app = Flask(__name__)
Scss(app)
app.secret_key = 'your_secret_key'  # Required for session management

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# initialize the app with the extension
db = SQLAlchemy(app)


class Box(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(50), nullable=False)
	comment=db.Column(db.String(150), nullable=True)
	
	items=db.relationship('Item',back_populates='box', cascade='all, delete-orphan')
	

	def __repr__(self) -> str:
		return f"Box {self.title}"

class Item(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(50), nullable=False)
	quantity=db.Column(db.Integer, nullable=False, default=1)
	added_on=db.Column(db.DateTime, default=datetime.utcnow)

	box_id = db.Column(db.Integer, db.ForeignKey('box.id'), nullable=False)
	box = db.relationship('Box', back_populates='items')


	def __repr__(self) -> str:
		return f"Item {self.name}"
	
# Function to format time based on selected timezone
def format_time(utc_time):
    timezone = session.get('timezone', 'UTC')
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    local_time = utc_time.astimezone(pytz.timezone(timezone))
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

# Register the format_time function as a template filter
@app.template_filter('format_time')
def format_time_filter(utc_time):
    return format_time(utc_time)

app.jinja_env.filters['format_time'] = format_time_filter

@app.route("/set_timezone", methods=['POST'])
def set_timezone():
    session['timezone'] = request.form['timezone']
    return redirect(url_for('index'))
	

# Home page
@app.route("/",methods=['GET'])
def index():
	
		all_items = Item.query.order_by(Item.id).all()
		all_boxes = Box.query.order_by(Box.id).all()
		return render_template('index.html',all_boxes=all_boxes,all_items=all_items)

# Add item to the box
@app.route("/add_item",methods=['POST'])
def add_item():
	add_item = request.form['item']
	add_box = request.form['box']
	item_quantity = request.form['quantity']

	new_item = Item(box_id=add_box, name=add_item, quantity=item_quantity)	
	try:
			db.session.add(new_item)
			db.session.commit()
			return redirect('/')
	except Exception as e:
			print(f"This error {e} occurred")
			return f"This error {e} occurred"
	
		
# Add box
@app.route("/add_box",methods=['POST'])
def add_box():
	
	if request.method == 'POST':
		new_box = request.form['title']
		new_comment = request.form['comment']
		
		adding_box = Box(title=new_box,comment=new_comment)
		try:
			
			db.session.add(adding_box)
			db.session.commit()
			return redirect('/')
		except Exception as e:
			print(f"This error {e} occured")
			return f"This error {e} occured"



# Delete item from the box
@app.route("/delete/<int:id>")
def delete(id:int):
	delete_item = Item.query.get_or_404(id)
	try:
		db.session.delete(delete_item)
		db.session.commit()
		return redirect('/')
	except Exception as e:
			print(f"This error {e} occured")
			return f"This error {e} occured"
	



# Delete item from the box
@app.route("/delete_box/<int:id>")
def delete_box(id:int):
	delete_box = Box.query.get_or_404(id)
	try:
		db.session.delete(delete_box)
		db.session.commit()
		return redirect('/')
	except Exception as e:
			print(f"This error {e} occured")
			return f"This error {e} occured"
	



# Update item from the box
@app.route("/edit/<int:id>", methods=['POST','GET'])
def edit(id:int):
	edit_item = Item.query.get_or_404(id)
	if request.method == "POST":
		edit_item.name = request.form['edit_item']
		try:
			db.session.commit()
			return redirect('/')
		except Exception as e:
			print(f"This error {e} occured")
			return f"This error {e} occured"
	else:
		return render_template('edit.html',edit_item=edit_item)
	



if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True,port=5004)