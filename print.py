from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

#import requests # kommer behöva för api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eped_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    url_link = db.Column(db.String, nullable=False)
    
    # Define the one-to-many relationship with Print_text
    print_texts = relationship('Print_text', backref='medicine', lazy=True)

    def __repr__(self):
        return f"Medicine('{self.id}, {self.eped_id}', '{self.name}', '{self.url_link}, '{self.print_texts})"

class Print_text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eped_id = db.Column(db.String, db.ForeignKey('medicine.eped_id'), nullable=False)
    print_name = db.Column(db.String, nullable=False)
    print_text = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"Print_text('{self.eped_id}', {self.print_name}', '{self.print_text}')"

'''
@app.route("/", methods=['GET'])
def home():
    query = request.args.get('query', '')  # Extracting 'query' parameter from request arguments
    print_texts = []
    if query:
        results = Medicine.query.filter(Medicine.name.startswith(query)).all()
        # Iterate through the results and fetch associated print texts
        for medicine in results:
            # Assuming eped_id uniquely identifies a medicine
            eped_id = medicine.eped_id
            # Filter Print_text objects based on the eped_id of the current medicine
            print_texts.extend(Print_text.query.filter_by(eped_id=eped_id).all())
    else:
        results = []
    return render_template('home.html', results=results, query=query, print_texts=print_texts)

'''

@app.route("/", methods=['GET'])
def home():
    query = request.args.get('query', '')  # Extracting 'query' parameter
    page = request.args.get('page', 1, type=int)  # Extracting 'page' parameter
    per_page = 7  # Define how many items per page

    if query:
        paginated_results = Medicine.query.filter(Medicine.name.startswith(query)).paginate(page=page, per_page=per_page, error_out=False)
        results = paginated_results.items
        total_pages = paginated_results.pages

        # Preparing data for associated print texts
        medicines_print_texts = {}
        for medicine in results:
            eped_id = medicine.eped_id
            medicines_print_texts[eped_id] = Print_text.query.filter_by(eped_id=eped_id).all()
    else:
        # If there's no query, default to empty values
        results = []
        total_pages = 0
        medicines_print_texts = {}

    return render_template('home.html', query=query, results=results, total_pages=total_pages, current_page=page, medicines_print_texts=medicines_print_texts)


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