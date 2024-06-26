# Author(s): 
# Rasmuss Brodin (rpbrodin@kth.se)
# Klara Lindemalm (klindema@kth.se)

# Description: Main functionality and routing of application used for printing medicine 
#              labels using ePed instructions

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Association table for many-to-many relationship between Medicine and Region
medicine_region_association = db.Table('medicine_region_association',
    db.Column('eped_id', db.Integer, db.ForeignKey('medicine.eped_id')),
    db.Column('region_id', db.Integer, db.ForeignKey('region.id'))
)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eped_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    url_link = db.Column(db.String, nullable=False)

    # Define the one-to-many relationship with Print_text
    print_texts = db.relationship('Print_text', backref='medicine', lazy=True)

    def __repr__(self):
        return f"Medicine('{self.id}, '{self.eped_id}', '{self.name}', '{self.url_link}, '{self.print_texts}')"

class Print_text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eped_id = db.Column(db.String, db.ForeignKey('medicine.eped_id'), nullable=False)
    print_name = db.Column(db.String, nullable=False)
    print_text = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Print_text('{self.eped_id}', '{self.print_name}', '{self.print_text}')"

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String, nullable=False)

    # Define many-to-many relationship with Medicine
    medicines = db.relationship('Medicine', secondary='medicine_region_association', backref='regions', lazy='dynamic')

    def __repr__(self):
        return f"Region('{self.id}', '{self.region}')"


@app.route("/")
def region():
    regions = Region.query.order_by(Region.region).all()  # Query all items from the Regions table
    return render_template('region.html', regions=regions)

@app.route("/search/<int:regionId>", methods=['GET'])
def search(regionId):
    query = request.args.get('query', '')  # Extracting 'query' parameter from request arguments
    print_texts = []
    if query:
        results = Medicine.query.join(Medicine.regions).filter(Region.id == regionId, Medicine.name.startswith(query.strip())).all()
        # Iterate through the results and fetch associated print texts
        for medicine in results:
            # Assuming eped_id uniquely identifies a medicine
            eped_id = medicine.eped_id
            # Filter Print_text objects based on the eped_id of the current medicine
            print_texts.extend(Print_text.query.filter_by(eped_id=eped_id).all())
    else:
        results = []
    return render_template('search.html', results=results, query=query, print_texts=print_texts, regionId=regionId)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/print/<int:id>")
def print_medicine(id):
    print_text_db = Print_text.query.get_or_404(id)
    return jsonify(print_text=print_text_db.print_text)