import requests
import shutil
import time
from print import db, Medicine, Print_text, app
app.app_context().push()


texts = Print_text.query.all()  # Assuming Print_text is your model
count = 0

for info in texts:
    zpl = info.print_text    
    print_id = info.id

    # Adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/12dpmm/labels/3x1/0/'
    files = {'file' : zpl}
    headers = {'Accept' : 'image/png'}  # Request PNG format
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f'static/labels/{print_id}.png', 'wb') as out_file:  # Save as PNG file with print_id as filename
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)
    count += 1
    if count % 5 == 0:
        time.sleep(1)