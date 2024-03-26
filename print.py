from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    print_text = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Medicine('{self.name}', '{self.print_text}')"

@app.route("/", methods=['GET'])
def home():
    query = request.args.get('query', '')  # Extracting 'query' parameter from request arguments
    if query:
        results = Medicine.query.filter(Medicine.name.startswith(query)).all()

    else:
        results = []

    print(query)
    return render_template('home.html', results=results, query=query)

@app.route("/about")
def about():
    return render_template('about.html')
