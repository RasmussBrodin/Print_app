import openpyxl
from print import db, Medicine, Print_text, Regions, app
app.app_context().push()

# Load the Excel workbook
workbook = openpyxl.load_workbook('regions.xlsx')

# Select the active worksheet (you can also specify a particular sheet by name)
sheet = workbook.active

# Iterate through rows and columns
for row in sheet.iter_rows(values_only=True):
    eped_id = row[0]
    region = row[2]

    if region != "Alla instruktioner":
        # Create a new Regions instance
        region = Regions(eped_id=eped_id, region=region)
        db.session.add(region)  # Add the Medicine instance to the session


# Close the workbook
workbook.close()
