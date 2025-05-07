import streamlit as st
from datetime import datetime
from uuid import uuid4

st.set_page_config(page_title="GiveBack", layout="wide")

# Initialize session state
if "items" not in st.session_state:
    st.session_state["items"] = []
if "claimed" not in st.session_state:
    st.session_state["claimed"] = []
if "email" not in st.session_state:
    st.session_state["email"] = ""

# --- Navigation Tabs ---
tab1, tab2, tab3 = st.tabs(["➕ Post Item", "📋 Available Items", "✅ Claimed by Me"])

# --- Tab 1: Post Item ---
with tab1:
    st.title("🎁 GiveBack: Pass it on. Waste less, care more!")
    st.subheader("Post something you no longer need:")

    with st.form("post_form"):
        st.session_state["email"] = st.text_input("Your Email")
        name = st.text_input("Item Name")
        location = st.text_input("Pickup Location")
        description = st.text_area("Description")
        image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Post")

        if submit:
            if name and location and description and st.session_state["email"]:
                item = {
                    "id": str(uuid4()),
                    "name": name,
                    "location": location,
                    "description": description,
                    "posted_by": st.session_state["email"],
                    "claimed_by": None,
                    "timestamp": str(datetime.now()),
                    "image": image.read() if image else None,
                    "image_type": image.type if image else None
                }
                st.session_state["items"].append(item)
                st.success("✅ Your item has been posted!")
            else:
                st.error("❌ Please fill out all fields and upload an image (optional).")

# --- Tab 2: Available Items ---
with tab2:
    st.header("📋 Available Items")
    available_items = [item for item in st.session_state["items"] if item["claimed_by"] is None]

    if available_items:
        for i, item in enumerate(available_items):
            with st.expander(f"{item['name']} - {item['location']}"):
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Posted by:** {item['posted_by']}")
                if item["image"]:
                    st.image(item["image"], caption="Item Image", use_column_width=True)
                if st.button("Claim this item", key=f"claim_{i}"):
                    item["claimed_by"] = st.session_state["email"]
                    st.session_state["claimed"].append(item)
                    st.success("🎉 You've claimed this item! It will now appear in your profile.")
    else:
        st.info("No items currently available. Check back later!")

# --- Tab 3: Claimed Items ---
with tab3:
    st.header("✅ Items You've Claimed")
    claimed_by_user = [item for item in st.session_state["items"] if item["claimed_by"] == st.session_state["email"]]

    if claimed_by_user:
        for item in claimed_by_user:
            with st.expander(f"{item['name']} - {item['location']}"):
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Posted by:** {item['posted_by']}")
                if item["image"]:
                    st.image(item["image"], caption="Item Image", use_column_width=True)
    else:
        st.info("You haven’t claimed anything yet.")

# --- Optional CSS for styling ---
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            border-radius: 6px;
            background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)

