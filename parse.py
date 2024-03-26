from bs4 import BeautifulSoup
from print import db, Medicine  # Replace 'your_application' with the name of your Flask application package

from print import app  # Replace 'your_application' with the name of your Flask application package
app.app_context().push()



# Load the HTML content
file_path = 'Etiketter.htm'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

data = []

# Iterate over <hr> tags, as each marks the beginning of a new entry
for hr in soup.find_all('hr'):
    next_b = hr.find_next('b')
    if next_b:
        medicine_name = next_b.get_text(strip=True)
        zpl_code = ""

        # Use the <p> tag following the <b> tag as the starting point for capturing ZPL code
        start_point = next_b.find_next('p')

        # Start capturing from the next element of <p> to avoid capturing empty ZPL codes
        for element in start_point.next_elements:
            if element.name == "hr":  # Stop if we reach the next entry marker (<hr>)
                break
            if element.name == "p":  # Ignore <p> tags as they are used as separators
                continue
            if getattr(element, "string", None):
                zpl_code += element.string.strip()

        data.append((medicine_name, zpl_code))

# Confirm that we have captured all entries
print(f"Total entries captured: {len(data)}")

# Add data to the database
for medicine_name, zpl_code in data:
    # Create a new Medicine object and add it to the database session
    medicine = Medicine(name=medicine_name, print_text=zpl_code)
    db.session.add(medicine)

# Commit the changes to the database
db.session.commit()

# Print a message to confirm successful addition to the database
print("Data added to the database successfully!")
