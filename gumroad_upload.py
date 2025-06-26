import os
import requests
from bs4 import BeautifulSoup

EMAIL = os.getenv("GUMROAD_EMAIL")
PASSWORD = os.getenv("GUMROAD_PASSWORD")

def upload_to_gumroad(file_path, title="Modern Resume Template", price=500):
    session = requests.Session()

    # Step 1: Login to Gumroad
    login_page = session.get("https://gumroad.com/login")
    soup = BeautifulSoup(login_page.text, "html.parser")
    auth_token = soup.find("input", {"name": "authenticity_token"}).get("value")

    login_data = {
        "authenticity_token": auth_token,
        "email": EMAIL,
        "password": PASSWORD,
    }

    res = session.post("https://gumroad.com/login", data=login_data)
    if "Log out" not in res.text:
        raise Exception("❌ Gumroad login failed. Check credentials.")

    print("✅ Logged in to Gumroad")

    # Step 2: Upload file (PDF or PNG)
    with open(file_path, "rb") as f:
        upload = session.post("https://gumroad.com/api/v2/files", files={"file": f})
        if not upload.ok:
            raise Exception("❌ File upload failed.")
        upload_data = upload.json()
        file_id = upload_data["id"]

    print("✅ File uploaded")

    # Step 3: Create product
    product_data = {
        "name": title,
        "price": price,
        "custom_permalink": "",
        "description": "Clean, modern, ATS-optimized resume template. Instant download. Editable Canva link inside.",
        "file_upload_ids[]": file_id,
        "is_variants_enabled": False,
        "is_recurring_billing": False,
    }

    product_res = session.post("https://gumroad.com/products", data=product_data)
    if product_res.status_code != 200:
        raise Exception("❌ Product creation failed.")

    print("✅ Upload successful: Product created on Gumroad")
