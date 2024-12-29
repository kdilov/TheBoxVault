from flask import Flask, render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime




app = Flask(__name__)
Scss(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config 
# initialize the app with the extension
db = SQLAlchemy(app)


class Box(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(50), nullable=False)
	comment=db.Column(db.String(150), nullable=True)
	
	items=db.relationship('Item',back_populates='box', cascade='all, delete-orphan')
	

	def __repr__(self) -> str:
		return f"Box {self.id}"

class Item(db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(50), nullable=False)
	quantity=db.Column(db.Integer, nullable=False, default=1)
	added_on=db.Column(db.DateTime, default=datetime.utcnow)

	box_id = db.Column(db.Integer, db.ForeignKey('box.id'), nullable=False)
	box = db.relationship('Box', back_populates='items')


	def __repr__(self) -> str:
		return f"Item {self.name}"
	

	

# Home page
@app.route("/",methods=['POST','GET'])
def index():
	# add item to box
	if request.method == 'POST':
		add_item = request.form['item']
		add_box = request.form['box']
		item_quantity = request.form['quantity']
		new_box = request.form['title']
		new_comment = request.form['comment']
		print(f"Received title: {new_box}, comment: {new_comment}")
		new_item = Item(box_id=add_box,name=add_item,quantity=item_quantity)
		add_box = Box(title=new_box,comment=new_comment)

		try:
			db.session.add(new_item)
			db.session.add(add_box)
			db.session.commit()
			return redirect('/')
		except Exception as e:
			print(f"This error {e} occured")
			return f"This error {e} occured"

	# See all items from the box
	else:
		all_items = Item.query.order_by(Item.id).all()
		all_boxes = Box.query.order_by(Box.id).all()
		return render_template('index.html',all_boxes=all_boxes, all_items=all_items)


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