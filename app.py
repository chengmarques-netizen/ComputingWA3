import streamlit as st

st.set_page_config(page_title="Kailash Parbat", page_icon="🍛")

# MENU
menu = {
    "Chole Bhatura": 15.00,
    "Pav Bhaji": 10.00,
    "Biryani": 15.00,
    "Paneer Butter Masala": 15.00,
    "Veg Biryani": 15.00,
    "Plain Dosa": 8.00,
    "Masala Dosa": 9.50,
    "Idli Sambar": 9.50,
    "Mango Lassi": 7.00,
    "Gulab Jamun": 6.00
}

# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "login"

if "account" not in st.session_state:
    st.session_state.account = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "cart" not in st.session_state:
    st.session_state.cart = {}


# UDF 1
def add_item(item):
    if item in st.session_state.cart:
        st.session_state.cart[item] += 1
    else:
        st.session_state.cart[item] = 1


# UDF 2
def remove_item(item):
    if item in st.session_state.cart:
        st.session_state.cart[item] -= 1

        if st.session_state.cart[item] <= 0:
            del st.session_state.cart[item]


# UDF 3
def calculate_subtotal():
    subtotal = 0

    for item in st.session_state.cart:
        subtotal += menu[item] * st.session_state.cart[item]

    return subtotal


# UDF 4
def calculate_gst(subtotal):
    return subtotal * 0.09


# UDF 5
def calculate_total(subtotal, gst):
    return subtotal + gst


# UDF 6
def check_email(email):
    if email == "":
        return False
    return True


# UDF 7
def check_password(password):
    if len(password) < 6:
        return False
    return True


# UDF 8
def check_card(card):
    card = card.replace(" ", "")

    if len(card) != 16:
        return False

    if card.isdigit() == False:
        return False

    return True


# UDF 9
def create_account(email, password):
    st.session_state.account = {
        "email": email,
        "password": password
    }


# UDF 10
def login(email, password):

    if st.session_state.account is None:
        return False

    if email == st.session_state.account["email"]:
        if password == st.session_state.account["password"]:
            return True

    return False


# TITLE
st.title("🍛 Kailash Parbat")
st.write("Chaats • Sweets • Dining")

st.divider()


# LOGIN PAGE
if st.session_state.page == "login":

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if st.session_state.account is None:
            st.error("Please create an account first.")

        elif login(email, password):
            st.session_state.logged_in = True
            st.session_state.page = "menu"
            st.rerun()

        else:
            st.error("Incorrect email or password.")

    if st.button("Create Account"):
        st.session_state.page = "create"
        st.rerun()


# CREATE ACCOUNT
elif st.session_state.page == "create":

    st.header("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        # VALIDATION 1
        if check_email(email) == False:
            st.error("Email cannot be empty.")

        # VALIDATION 2
        elif check_password(password) == False:
            st.error("Password must be at least 6 characters.")

        else:
            create_account(email, password)

            st.success("Account created!")

            st.session_state.page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# MENU
elif st.session_state.page == "menu":

    st.header("🍽️ Menu")

    item_count = sum(st.session_state.cart.values())

    if st.button("Cart (" + str(item_count) + " items)"):
        st.session_state.page = "cart"
        st.rerun()

    st.divider()

    for item in menu:

        st.write("**" + item + "**")
        st.write("$" + format(menu[item], ".2f"))

        if st.button("Add", key=item):
            add_item(item)
            st.rerun()

        st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.cart = {}
        st.session_state.page = "login"
        st.rerun()


# CART
elif st.session_state.page == "cart":

    st.header("🛒 Cart")

    if len(st.session_state.cart) == 0:

        st.write("Your cart is empty.")

    else:

        for item in list(st.session_state.cart):

            quantity = st.session_state.cart[item]

            st.write(
                item + " x " +
                str(quantity) +
                " = $" +
                format(menu[item] * quantity, ".2f")
            )

            if st.button("Remove", key="remove_" + item):
                remove_item(item)
                st.rerun()

        st.divider()

        subtotal = calculate_subtotal()

        st.subheader(
            "Subtotal: $" +
            format(subtotal, ".2f")
        )

        if st.button("Checkout"):
            st.session_state.page = "checkout"
            st.rerun()

    if st.button("Back to Menu"):
        st.session_state.page = "menu"
        st.rerun()


# CHECKOUT
elif st.session_state.page == "checkout":

    st.header("💳 Checkout")

    subtotal = calculate_subtotal()
    gst = calculate_gst(subtotal)
    total = calculate_total(subtotal, gst)

    st.write("Subtotal: $" + format(subtotal, ".2f"))
    st.write("GST: $" + format(gst, ".2f"))

    st.subheader("Total: $" + format(total, ".2f"))

    name = st.text_input("Name")
    card = st.text_input("Card Number")

    if st.button("Pay"):

        # VALIDATION 3
        if check_card(card) == False:
            st.error("Card number must contain 16 digits.")

        else:
            st.session_state.cart = {}
            st.session_state.page = "success"
            st.rerun()

    if st.button("Back to Cart"):
        st.session_state.page = "cart"
        st.rerun()


# SUCCESS
elif st.session_state.page == "success":

    st.header("🎉 Order Successful!")

    st.success("Your order has been placed!")

    if st.button("Order Again"):
        st.session_state.page = "menu"
        st.rerun()
    st.success("Your order has been placed!")

    if st.button("Order Again"):
        st.session_state.page = "menu"
        st.rerun()
