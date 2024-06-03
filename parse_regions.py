# Author(s): 
# Rasmuss Brodin (rpbrodin@kth.se)
# Klara Lindemalm (klindema@kth.se)

# Description: Code used to parse xlxs file containing information about what rehions have 
# choosen what ePed instructions.

import openpyxl
from print import db, Region, Medicine, app
app.app_context().push()

# Load the Excel workbook
workbook = openpyxl.load_workbook('regions.xlsx')

# Select the active worksheet (you can also specify a particular sheet by name)
sheet = workbook.active

# Iterate through rows and columns
for row in sheet.iter_rows(values_only=True):
    eped_id = row[0]
    region_name = row[2]

    # Check if the region is already added to the database
    region = Region.query.filter_by(region=region_name).first()

    if not region and region_name != "Alla instruktioner":
        # Create a new Region instance
        region = Region(region=region_name)
        db.session.add(region)  # Add the Region instance to the session

    # Retrieve the medicine based on eped_id
    medicine = Medicine.query.filter_by(eped_id=eped_id).first()

    if medicine and region:
        # Add the medicine to the region's list of medicines
        region.medicines.append(medicine)

# Commit the session to persist changes to the database
db.session.commit()

# Close the workbook
workbook.close()

print("done")
