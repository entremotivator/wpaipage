import streamlit as st
import requests

def register_user(api_url, api_key, customer_id, customer_info, membership_status, payment_status, site_url, site_title):
    endpoint = f"{api_url}/wp-json/wu/v2/register"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "customer_id": customer_id,
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
    st.title("WP Ultimo Registration App")

    # Move API URL and API Key to the sidebar
    with st.sidebar:
        st.subheader("API Configuration")
        api_url = st.text_input("API URL:")
        api_key = st.text_input("API Key:", type="password")

    customer_id = st.number_input("Customer ID:")

    user_id = st.number_input("User ID:")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    email = st.text_input("Email:")

    customer_info = {"user_id": user_id, "username": username, "password": password, "email": email}

    membership_status = st.selectbox("Membership Status", ["pending", "active", "trialing", "expired", "on-hold", "canceled"])
    payment_status = st.selectbox("Payment Status", ["pending", "completed", "refunded", "partially-refunded", "partially-paid", "failed", "canceled"])

    site_url = st.text_input("Site URL:")
    site_title = st.text_input("Site Title:")

    return api_url, api_key, customer_id, customer_info, membership_status, payment_status, site_url, site_title

def main():
    form_values = display_registration_form()

    if st.button("Register User"):
        with st.spinner("Registering user..."):
            response = register_user(*form_values)
        
        if "error" in response:
            st.error(f"Error: {response['error']}")
        else:
            st.success("User registered successfully!")
            # Display more specific information from the API response, if needed

if __name__ == "__main__":
    main()
