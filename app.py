import streamlit as st
import requests
from ftplib import FTP
import json

def create_woocommerce_product(api_url, api_key, product_info):
    endpoint = f"{api_url}/wp-json/wc/v3/products"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, data=json.dumps(product_info), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_product_creation_form():
    api_url = st.text_input("WooCommerce API URL:")
    api_key = st.text_input("WooCommerce API Key:", type="password")

    product_name = st.text_input("Product Name:")
    product_description = st.text_area("Product Description:", height=200)
    product_price = st.number_input("Product Price:", min_value=0.01, value=0.01)

    product_info = {
        "name": product_name,
        "description": product_description,
        "regular_price": str(product_price),
    }

    return api_url, api_key, product_info

# Placeholder functions for Divi page creation and WordPress interaction
def create_divi_page(api_key, page_title, page_content, uploaded_file):
    try:
        # Implement logic to create a new Divi page
        # You can use the uploaded_file parameter to handle file uploads
        return "123"  # Placeholder ID, replace with actual logic
    except Exception as e:
        st.error(f"Error creating Divi page: {e}")
        return None

def set_home_page(api_key, page_id):
    try:
        # Implement logic to set the newly created page as the homepage
        pass
    except Exception as e:
        st.error(f"Error setting the homepage: {e}")

def upload_to_ftp(ftp_host, ftp_user, ftp_password, uploaded_file):
    try:
        # Connect to FTP server
        with FTP(ftp_host) as ftp:
            ftp.login(user=ftp_user, passwd=ftp_password)

            # Change to the appropriate directory on the FTP server
            ftp.cwd("/path/to/destination/directory")

            # Upload the file
            with open(uploaded_file.name, "rb") as file:
                ftp.storbinary(f"STOR {uploaded_file.name}", file)
    except Exception as e:
        st.error(f"Error uploading files to FTP: {e}")

def register_user(api_url, api_key, customer_info, site_url, site_title, membership_status, payment_status):
    endpoint = f"{api_url}/wp-json/wu/v2/register"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "customer": customer_info,
        "membership": {"status": membership_status},
        "payment": {"status": payment_status},
        "site": {"site_url": site_url, "site_title": site_title}
    }

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_registration_form():
    api_url = st.text_input("API URL:")
    api_key = st.text_input("API Key:", type="password")

    user_id = st.number_input("User ID:")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    email = st.text_input("Email:")

    customer_info = {"user_id": user_id, "username": username, "password": password, "email": email}

    membership_status = st.selectbox("Membership Status", ["pending", "active", "trialing", "expired", "on-hold", "canceled"])
    payment_status = st.selectbox("Payment Status", ["pending", "completed", "refunded", "partially-refunded", "partially-paid", "failed", "canceled"])

    site_url = st.text_input("Site URL:")
    site_title = st.text_input("Site Title:")

    return api_url, api_key, customer_info, site_url, site_title, membership_status, payment_status

# Apply some basic styling using HTML and CSS
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 10px;
        }
        .main {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("AI Funnel Machine")

    # Sidebar for FTP credentials and OpenAI key
    with st.sidebar:
        st.subheader("FTP Configuration")
        ftp_host = st.text_input("FTP Host")
        ftp_user = st.text_input("FTP User")
        ftp_password = st.text_input("FTP Password", type="password")

        st.subheader("OpenAI Key")
        openai_key = st.text_input("Enter your OpenAI key")

    # Tabs for Site Creation, Divi Page Maker, and WooCommerce Product Creator
    tabs = st.radio("Select a tab:", ["Site Creation", "Divi Page Maker", "WooCommerce Product Creator"])

    if tabs == "Site Creation":
        # Site Creation Tab
        st.header("Site Creation")

        # Get user registration form values
        api_url, api_key, customer_info, site_url, site_title, membership_status, payment_status = display_registration_form()

        if st.button("Register User"):
            # Input validation
            if any(value == '' for value in [api_url, api_key] + list(customer_info.values()) + [site_url, site_title]):
                st.warning("Please fill out all fields for user registration.")
            else:
                with st.spinner("Registering user..."):
                    response = register_user(api_url, api_key, customer_info, site_url, site_title, membership_status, payment_status)

                if "error" in response:
                    st.error(f"Error: {response['error']}")
                else:
                    st.success("User registered successfully!")
                    st.write("## Registration Details")
                    st.write(f"**Username:** {response['customer']['username']}")
                    st.write(f"**Email:** {response['customer']['email']}")
                    st.write(f"**Site Title:** {response['site']['site_title']}")
                    st.write(f"**Membership Status:** {response['membership']['status']}")
                    st.write(f"**Payment Status:** {response['payment']['status']}")
                    # Customize success message based on status
                    if response['membership']['status'] == 'active' and response['payment']['status'] == 'completed':
                        st.success("Congratulations! Your membership is now active, and the payment is completed.")
                    elif response['membership']['status'] == 'pending':
                        st.info("Your membership is pending approval.")
                    else:
                        st.info("Please check your registration details.")

    elif tabs == "Divi Page Maker":
        # Divi Page Maker Tab
        st.header("Divi Page Maker")

        # Get the number of page sections
        num_sections = st.number_input("Number of Page Sections", min_value=1, value=1)

        # Loop through each section
        for i in range(num_sections):
            st.subheader(f"Section {i + 1}")

            # Get page details for each section
            page_title = st.text_input(f"Enter the title for Section {i + 1}")
            page_content = st.text_area(f"Enter the content for Section {i + 1}", height=200)

            # File upload for each section
            uploaded_file = st.file_uploader(f"Upload file for Section {i + 1}", type=["jpg", "jpeg", "png", "pdf"])

            # Create Divi page for each section
            if st.button(f"Create Divi Page for Section {i + 1}"):
                with st.spinner(f"Creating Divi Page for Section {i + 1}..."):
                    page_id = create_divi_page(openai_key, page_title, page_content, uploaded_file)

                if page_id:
                    st.success(f"Divi page created successfully for Section {i + 1} with ID: {page_id}")
                    # Set the new page as the homepage
                    set_home_page(openai_key, page_id)
                    # Upload files to WordPress through FTP
                    if uploaded_file:
                        st.info("Uploading file to FTP...")
                        upload_to_ftp(ftp_host, ftp_user, ftp_password, uploaded_file)
                        st.success("File uploaded to FTP successfully.")

    elif tabs == "WooCommerce Product Creator":
        # WooCommerce Product Creator Tab
        st.header("WooCommerce Product Creator")

        # Get product creation form values
        api_url_wc, api_key_wc, product_info = display_product_creation_form()

        if st.button("Create WooCommerce Product"):
            # Input validation
            if any(value == '' for value in [api_url_wc, api_key_wc] + list(product_info.values())):
                st.warning("Please fill out all fields for product creation.")
            else:
                with st.spinner("Creating WooCommerce product..."):
                    response_wc = create_woocommerce_product(api_url_wc, api_key_wc, product_info)

                if "error" in response_wc:
                    st.error(f"Error: {response_wc['error']}")
                else:
                    st.success("WooCommerce product created successfully!")
                    st.write("## Product Details")
                    st.write(f"**Product Name:** {response_wc['name']}")
                    st.write(f"**Product ID:** {response_wc['id']}")
                    st.write(f"**Regular Price:** {response_wc['regular_price']}")
                    # Add additional product details as needed

if __name__ == "__main__":
    main()
