import streamlit as st
import requests

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
    st.title("WP AI Registration App")

    # Sidebar for API configuration
    with st.sidebar:
        st.subheader("API Configuration")
        api_url = st.text_input("API URL:")
        api_key = st.text_input("API Key:", type="password")

    st.write("## User Information")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    
    # Password strength checker
    if len(password) < 8:
        st.warning("Password should be at least 8 characters long.")
    
    email = st.text_input("Email:")
    
    # Email validation
    if not st.button("Validate Email"):
        st.warning("Click the button to validate email.")

    st.write("## Site Information")
    site_url = st.text_input("Site URL:")
    site_title = st.text_input("Site Title:")

    st.write("## Membership and Payment Options")
    membership_status = st.selectbox("Membership Status", ["pending", "active", "trialing", "expired", "on-hold", "canceled"])
    payment_status = st.selectbox("Payment Status", ["pending", "completed", "refunded", "partially-refunded", "partially-paid", "failed", "canceled"])

    return api_url, api_key, {"username": username, "password": password, "email": email}, site_url, site_title, membership_status, payment_status

def main():
    form_values = display_registration_form()

    if st.button("Register User"):
        # Input validation
        if any(value == '' for value in form_values[:-2]):
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
            # Customize success message based on status
            if response['membership']['status'] == 'active' and response['payment']['status'] == 'completed':
                st.success("Congratulations! Your membership is now active, and the payment is completed.")
            elif response['membership']['status'] == 'pending':
                st.info("Your membership is pending approval.")
            else:
                st.info("Please check your registration details.")

if __name__ == "__main__":
    main()
