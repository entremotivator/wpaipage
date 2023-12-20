import streamlit as st
import requests

def register_user(api_url, api_key, customer_info, site_url, site_title):
    endpoint = f"{api_url}/wp-json/wu/v2/register"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "customer": customer_info,
        "site": {"site_url": site_url, "site_title": site_title}
    }

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_registration_form():
    st.title("WP AI Registration App")

    # Sidebar for API configuration
    with st.sidebar:
        st.subheader("API Configuration")
        api_url = st.text_input("API URL:")
        api_key = st.text_input("API Key:", type="password")

    st.write("## User Information")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    email = st.text_input("Email:")

    st.write("## Site Information")
    site_url = st.text_input("Site URL:")
    site_title = st.text_input("Site Title:")

    return api_url, api_key, {"username": username, "password": password, "email": email}, site_url, site_title

def main():
    form_values = display_registration_form()

    if st.button("Register User"):
        # Input validation
        if any(value == '' for value in form_values[:-1]):
            st.warning("Please fill out all fields.")
            return

        with st.spinner("Registering user..."):
            response = register_user(*form_values)

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

if __name__ == "__main__":
    main()
