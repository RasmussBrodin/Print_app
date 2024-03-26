from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    print_text = db.Column(db.String, nullable=False)
    link_url = db.Column(db.String)

    def __repr__(self):
        return f"Medicine('{self.name}', '{self.print_text}')"

@app.route("/", methods=['GET'])
def home():
    query = request.args.get('query', '')  # Extracting 'query' parameter from request arguments
    if query:
        results = Medicine.query.filter(Medicine.name.startswith(query)).all()
    else:
        results = []
    return render_template('home.html', results=results, query=query)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/print/<int:medicine_id>")
def print_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    return jsonify(print_text=medicine.print_text)

