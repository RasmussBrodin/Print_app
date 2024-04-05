import re
from bs4 import BeautifulSoup
from print import db, Medicine, Print_text, app
app.app_context().push()

## Remove all old data from the Medicine table
Medicine.query.delete()
Print_text.query.delete()

# Load the HTML content
file_path = 'Etiketter_ny.htm'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

data = []
# Regular expression pattern to match text within brackets
bracket_pattern = re.compile(r'\[(.*?)\]')

# Iterate over <hr> tags, as each marks the beginning of a new entry
for h1 in soup.find_all('h1'):
    medicine_name = h1.get_text(strip=True)

    # Extract the text within brackets using regex
    match = bracket_pattern.search(medicine_name)
    if match:
        bracket_content = match.group(1)
    else:
        bracket_content = None
    medicine_link_url = "https://eped.se/backup/eped/" + bracket_content + ".pdf"

    # Create a new Medicine instance
    medicine = Medicine(eped_id=bracket_content, name=medicine_name, url_link=medicine_link_url)
    db.session.add(medicine)  # Add the Medicine instance to the session
    
    # Find all elements between current h1 and next h1
    elements_between_h1 = h1.find_all_next()
    for tag in elements_between_h1:
        if tag.name == 'h1':
            break
        if tag.name == 'h2':
            print_name1 = tag.text.strip()
            start_point = tag.find_next('p')
            zpl_code = ""
            # Start capturing from the next element of <p> to avoid capturing empty ZPL codes
            for element in start_point.next_elements:
                if element.name == "hr":  # Stop if we reach the next entry marker (<hr>)
                    break
                if element.name == "p":  # Ignore <p> tags as they are used as separators
                    continue 
                if getattr(element, "string", None):
                    zpl_code += element.string.strip()
            # Create a new Print_text instance associated with the Medicine instance
            print_text = Print_text(eped_id=bracket_content, print_name=print_name1, print_text=zpl_code)
            db.session.add(print_text)  # Add the Print_text instance to the session

# Commit the changes to the database
db.session.commit()

# Print a message to confirm successful addition to the database
print("Data added to the database successfully!")

'''
for data_entry in data[:5]:
    medicine_name, new_instructions, medicine_link_url = data_entry
    print(f"Medicine Name: {medicine_name}")
    print("Instructions:")
    for i, (instruction, extracted_numbers) in enumerate(new_instructions, start=1):
        print(f"  {i}. {instruction} - Extracted Numbers: {extracted_numbers}")
    print(f"Link URL: {medicine_link_url}\n")

# Confirm that we have captured all entries
print(f"Total entries captured: {len(data)}")


## Remove all old data from the Medicine table
Medicine.query.delete()
Print_text.query.delete()

for bracket_content, medicine_name, instructions, medicine_link_url in data:
    # Create a new Medicine instance
    medicine = Medicine(eped_id=bracket_content, name=medicine_name, url_link=medicine_link_url)
    db.session.add(medicine)  # Add the Medicine instance to the session

    # Iterate over the instructions list and add each instruction as a Print_text instance
    for instruction in instructions:
        # Create a new Print_text instance associated with the Medicine instance
        print_text = Print_text(eped_id=bracket_content, print_text=instruction)
        db.session.add(print_text)  # Add the Print_text instance to the session

# Commit the changes to the database
db.session.commit()

# Print a message to confirm successful addition to the database
print("Data added to the database successfully!")
'''