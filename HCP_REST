import requests
import datetime
import os

# Date for formatting endpoint URL
date = datetime.datetime.now()
retention_date = date + datetime.timedelta(days=366)
retention_date_epoch = int(retention_date.timestamp())

# HCP request information
hcp_user = "USERINBASE64=="
hcp_pass = "SHAOFPASSWORD"
token = f"HCP {hcp_user}:{hcp_pass}"
url = "HCP REST URI"
retention_url = f"?retention={retention_date_epoch}"
#endpoint2 = "HCP REST URI"
headers = {
        "Authorization": token,
        "Content-Type": "application/binary"
        }

# Files to be sent
root_dir = r"C:\Users\stevlam\Desktop\LR Inactive"
for parent_dir in (os.listdir(path=root_dir)):
    for child_dir in os.listdir(path=os.path.join(root_dir, parent_dir)):
        for file in os.listdir(path=os.path.join(root_dir,parent_dir,child_dir)):
            full_file_path = f"{root_dir}\\{parent_dir}\\{child_dir}\\{file}"
            with open(full_file_path, "r") as fr:
                request_url = f"{url}/{parent_dir}/{child_dir}/{file}{retention_url}"
                fr.close()
                # r = requests.put(url=request_url, headers=headers, data=fr.read(), verify=False)
