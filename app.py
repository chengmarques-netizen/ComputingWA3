import streamlit as st

st.set_page_config(
    page_title="Kailash Parbat",
    page_icon="🍛"
)

# -------------------------
# MENU
# -------------------------

menu = {
    "Chole Bhatura Combo": 15.00,
    "Pav Bhaji Combo": 15.00,
    "Biryani Combo": 15.00,
    "North Indian Combo": 16.00,
    "South Indian Combo": 16.00,
    "Chinese Combo": 17.00,
    "Paneer Butter Masala": 15.00,
    "Veg Jalfrezi": 15.00,
    "Dal Fry": 14.00,
    "Dal Makhani": 14.00,
    "KP Chole Masala": 14.00,
    "Veg Biryani": 15.00,
    "Jeera Rice": 12.00,
    "Tawa Chapati": 3.50,
    "Plain Dosa": 8.00,
    "Masala Dosa": 9.50,
    "Cheese Dosa": 9.50,
    "Masala Cheese Dosa": 11.00,
    "Idli Sambar": 9.50,
    "Medu Vada Sambar": 9.50,
    "Ghee Pongal": 9.50,
    "Mango Lassi": 7.00,
    "Sweet Lassi": 6.50,
    "Butter Milk": 6.50,
    "Lime Water": 5.00,
    "Fresh Lime Soda": 6.00,
    "Aerated Drinks": 2.50,
    "Mineral Water": 2.50,
    "Masala Tea": 4.00,
    "Chennai Filter Coffee": 4.00,
    "Gulab Jamun": 6.00,
    "Flavoured Kulfis": 8.00,
    "Pani Puri": 7.50,
    "Bhel Puri": 8.00,
    "Sev Puri": 8.00,
    "Dahi Puri": 9.00,
    "Ragda Dahi Puri": 9.00,
    "Papdi Chaat": 9.00,
    "Dahi Wada": 9.00,
    "Tikki Chaat": 9.00,
    "Samosa Chaat": 9.00,
    "Pav Bhaji": 10.00,
    "Cheese Pav Bhaji": 12.00,
    "Vada Pav": 8.00,
    "Veg Frankie": 8.50,
    "Aloo Paratha": 9.50,
    "Gobi Paratha": 9.50,
    "Mix Veg Paratha": 9.50,
    "Paneer Paratha": 9.50,
    "Cheese Paratha": 9.50
}


# -------------------------
# SESSION VARIABLES
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "account" not in st.session_state:
    st.session_state.account = None

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -------------------------
# 10 UDFS
# -------------------------

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
        quantity = st.session_state.cart[item]
        subtotal = subtotal + menu[item] * quantity

    return subtotal


# UDF 4
def calculate_gst(subtotal):
    gst = subtotal * 0.09
    return gst


# UDF 5
def calculate_total(subtotal, gst):
    total = subtotal + gst
    return total


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
def check_card(card_number):
    card_number = card_number.replace(" ", "")

    if len(card_number) != 16:
        return False

    if not card_number.isdigit():
        return False

    return True


# UDF 9
def create_account(email, password):
    st.session_state.account = {
        "email": email,
        "password": password
    }


# UDF 10
def login_user(email, password):
    if st.session_state.account is None:
        return False

    if email == st.session_state.account["email"]:
        if password == st.session_state.account["password"]:
            return True

    return False


# -------------------------
# HEADER
# -------------------------

st.title("🍛 Kailash Parbat")
st.caption("Chaats • Sweets • Dining")
st.divider()


# =====================================================
# LOGIN
# =====================================================

if st.session_state.page == "login":

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if st.session_state.account is None:
            st.error("No account found. Please create an account.")

        elif login_user(email, password):
            st.session_state.logged_in = True
            st.session_state.page = "menu"
            st.rerun()

        else:
            st.error("Incorrect email or password.")

    st.write("Don't have an account?")

    if st.button("Create Account"):
        st.session_state.page = "create"
        st.rerun()


# =====================================================
# CREATE ACCOUNT
# =====================================================

elif st.session_state.page == "create":

    st.header("Create Account")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        # VALIDATION 1
        if not check_email(email):
            st.error("Email cannot be empty.")

        # VALIDATION 2
        elif not check_password(password):
            st.error("Password must be at least 6 characters.")

        elif password != confirm:
            st.error("Passwords do not match.")

        else:
            create_account(email, password)

            st.success("Account created!")

            st.session_state.page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# MENU
# =====================================================

elif st.session_state.page == "menu":

    if not st.session_state.logged_in:
        st.session_state.page = "login"
        st.rerun()

    st.header("🍽️ Menu")

    number_of_items = sum(
        st.session_state.cart.values()
    )

    if st.button(
        "🛒 View Cart (" +
        str(number_of_items) +
        " items)"
    ):
        st.session_state.page = "cart"
        st.rerun()

    st.divider()

    for item in menu:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write("**" + item + "**")
            st.write(
                "$" +
                format(menu[item], ".2f")
            )

        with col2:
            if st.button(
                "Add",
                key=item
            ):
                add_item(item)
                st.rerun()

        st.divider()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.cart = {}
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# CART
# =====================================================

elif st.session_state.page == "cart":

    st.header("🛒 Your Cart")

    if len(st.session_state.cart) == 0:

        st.info("Your cart is empty.")

    else:

        for item in list(st.session_state.cart):

            quantity = st.session_state.cart[item]
            price = menu[item]

            col1, col2, col3 = st.columns(
                [4, 1, 1]
            )

            with col1:
                st.write("**" + item + "**")

            with col2:
                st.write(
                    "$" +
                    format(price, ".2f")
                )

            with col3:
                st.write(
                    "Qty: " +
                    str(quantity)
                )

            if st.button(
                "Remove",
                key="remove_" + item
            ):
                remove_item(item)
                st.rerun()

            st.divider()

        subtotal = calculate_subtotal()

        st.subheader(
            "Subtotal: $" +
            format(subtotal, ".2f")
        )

        if st.button("Proceed to Checkout"):
            st.session_state.page = "checkout"
            st.rerun()

    if st.button("← Back to Menu"):
        st.session_state.page = "menu"
        st.rerun()


# =====================================================
# CHECKOUT
# =====================================================

elif st.session_state.page == "checkout":

    st.header("💳 Checkout")

    subtotal = calculate_subtotal()
    gst = calculate_gst(subtotal)
    total = calculate_total(
        subtotal,
        gst
    )

    st.subheader("Order Summary")

    for item in st.session_state.cart:

        quantity = st.session_state.cart[item]
        price = menu[item]

        item_total = price * quantity

        st.write(
            item +
            " × " +
            str(quantity) +
            " = $" +
            format(item_total, ".2f")
        )

    st.divider()

    st.write(
        "Subtotal: $" +
        format(subtotal, ".2f")
    )

    st.write(
        "GST (9%): $" +
        format(gst, ".2f")
    )

    st.subheader(
        "Total: $" +
        format(total, ".2f")
    )

    st.divider()

    st.subheader("Credit Card Details")

    card_name = st.text_input(
        "Cardholder Name"
    )

    card_number = st.text_input(
        "Card Number",
        placeholder="1234 5678 9012 3456"
    )

    expiry = st.text_input(
        "Expiry Date",
        placeholder="MM/YY"
    )

    cvv = st.text_input(
        "CVV",
        type="password"
    )

    st.warning(
        "This is a school project. Do not enter a real card."
    )

    if st.button(
        "Pay $" +
        format(total, ".2f") +
        " & Place Order"
    ):

        # VALIDATION 3
        if not check_card(card_number):
            st.error(
                "Card number must contain 16 digits."
            )

        else:
            st.session_state.cart = {}
            st.session_state.page = "success"
            st.rerun()

    if st.button("← Back to Cart"):
        st.session_state.page = "cart"
        st.rerun()


# =====================================================
# SUCCESS PAGE
# =====================================================

elif st.session_state.page == "success":

    st.header("🎉 Order Successful!")

    st.success(
        "Your Kailash Parbat order has been placed successfully!"
    )

    st.write(
        "Thank you for ordering with Kailash Parbat."
    )

    if st.button("Order Again"):
        st.session_state.page = "menu"
        st.rerun()
