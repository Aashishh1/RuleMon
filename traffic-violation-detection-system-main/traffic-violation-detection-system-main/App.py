import streamlit as st
import pandas as pd
import psycopg2
import cv2
import os
from ultralytics import YOLO
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname='bikewatch',
        user='postgres',
        password='root',
        host='localhost',
        port='5432'
    )
    return conn

# Function to fetch violation details from database
def get_violation_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT p.name, p.email, v.veh_reg_id, v.date, v.image_url, r.name AS violation_name, r.penalty_amount
    FROM violation v
    JOIN person p ON v.person_id = p.id
    JOIN rule r ON v.rules_violated = r.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Function to send email notification
def send_email(to_address, subject, body):
    try:
        # Validate email address
        valid = validate_email(to_address)
        to_address = valid.email

        from_address = 'support@aptpath.in'
        password = 'btpdcnfkgjyzdndh'

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
    except EmailNotValidError as e:
        st.error(f"Invalid email address: {to_address}. {str(e)}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Function to format email body
def format_email_body(details):
    body = f"""
    Dear {details[0]},

    We would like to inform you about a traffic violation that was recorded on {details[3]}.

    Violation Details:
    - Violation: {details[5]}
    - Penalty Amount: {details[6]}
    - Vehicle Registration ID: {details[2]}
    - Image URL: {details[4]}

    Please take the necessary action to resolve this issue.

    Regards,
    Traffic Department
    """
    return body

# Function to perform violation detection using YOLO
def perform_detection(image_path):
    try:
        # Load your custom YOLO model for helmet detection
        helmet_model_path = "C:/Users/Arshia Shaikh/Desktop/best (1).pt"
        helmet_model = YOLO(helmet_model_path)

        # Load the YOLOv8 model for general object detection
        general_model_path = "yolov8n.pt"  # or any other pre-trained YOLOv8 model
        general_model = YOLO(general_model_path)

        # Process the image
        image = cv2.imread(image_path)
        if image is None:
            st.error(f"Failed to load image: {image_path}")
            return None

        # Perform inference using the helmet model
        helmet_results = helmet_model(image_path)[0]

        # Perform inference using the general object detection model
        general_results = general_model(image_path)[0]

        # Draw bounding boxes and labels on the image
        detected_image = draw_detection(image, helmet_results, general_results)

        return detected_image

    except Exception as e:
        st.error(f"Error during detection: {e}")
        return None

# Function to draw detection results on the image
def draw_detection(image, helmet_results, general_results):
    # Extract bounding boxes and labels for helmet model
    helmet_boxes = helmet_results.boxes.xyxy.cpu().numpy()  # xyxy format
    helmet_classes = helmet_results.boxes.cls.cpu().numpy()  # class indices
    helmet_scores = helmet_results.boxes.conf.cpu().numpy()  # confidences
    helmet_labels = helmet_results.names

    # Extract bounding boxes and labels for general model
    general_boxes = general_results.boxes.xyxy.cpu().numpy()  # xyxy format
    general_classes = general_results.boxes.cls.cpu().numpy()  # class indices
    general_scores = general_results.boxes.conf.cpu().numpy()  # confidences
    general_labels = general_results.names

    # Process each detected object from helmet model
    for box, cls, conf in zip(helmet_boxes, helmet_classes, helmet_scores):
        x1, y1, x2, y2 = map(int, box)
        label = helmet_labels[int(cls)]
        color = (0, 255, 0) if label == 'with helmet' else (0, 0, 255) if label == 'without helmet' else (255, 0, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Process each detected object from general model
    for box, cls, conf in zip(general_boxes, general_classes, general_scores):
        x1, y1, x2, y2 = map(int, box)
        label = general_labels[int(cls)]
        color = (255, 0, 0) if label == 'person' else (255, 255, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return image

# Streamlit app for violation dashboard
def violation_dashboard():
    st.title("Violation Dashboard")
    violations = get_violation_details()

    if violations:
        st.write("Recent Violations:")
        data = []
        merged_data = {}

        for violation in violations:
            person_key = violation[2]  # Use vehicle registration ID as the key for merging
            if person_key not in merged_data:
                merged_data[person_key] = {
                    "Date": violation[3],
                    "Vehicle Reg No.": violation[2],
                    "Name": violation[0],
                    "Comments": [violation[5]],  # Start with a list for potential multiple violations
                    "Penalty": f"₹{violation[6]}",
                    "Image URL": violation[4]  # Include image URL
                }
            else:
                merged_data[person_key]["Comments"].append(violation[5])  # Append new violation comment

        # Convert merged_data to the format needed for DataFrame
        for key, value in merged_data.items():
            value["Comments"] = ", ".join(value["Comments"])  # Join multiple comments into one string
            data.append(value)

        df = pd.DataFrame(data)
        st.table(df)

        # Display images in expanders
        for i, violation in enumerate(violations):
            with st.expander(f"Show Image for {violation[2]}"):
                st.image(violation[4], caption=f'Violation Image {i+1}', use_column_width=True)

        # Plotting graph
        st.write("Penalty Distribution")
        penalty_df = pd.DataFrame(violations, columns=["Name", "Email", "Vehicle Reg No.", "Date", "Image URL", "Violation", "Penalty"])
        sns.barplot(data=penalty_df, x="Violation", y="Penalty")
        plt.xticks(rotation=90)
        st.pyplot(plt)
    else:
        st.write("No violations found.")

# Streamlit app for violation detection
def detection_page():
    st.title("Violation Detection")

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    veh_reg_id = st.text_input("Enter Vehicle Registration ID")

    if uploaded_file is not None and veh_reg_id:
        try:
            image_path = os.path.join('uploads', uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                st.success("Saved File")

            # Perform detection
            detected_image = perform_detection(image_path)

            if detected_image is not None:
                # Convert OpenCV BGR image to RGB format for display in Streamlit
                detected_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
                st.image(detected_image_rgb, caption='Detected Objects', use_column_width=True)

                # Send email notification
                violation_details = get_violation_details()
                for violation in violation_details:
                    if violation[2] == veh_reg_id:
                        email_body = format_email_body(violation)
                        send_email(violation[1], "Traffic Violation Notification", email_body)
                        st.success("Email sent successfully!")
                        break
            else:
                st.warning("No objects detected in the uploaded image.")
        except Exception as e:
            st.error(f"Error processing the uploaded image: {e}")

# Main Streamlit app
def main():
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Go to", ["Violation Dashboard", "Violation Detection"])

    if options == "Violation Dashboard":
        violation_dashboard()
    elif options == "Violation Detection":
        detection_page()

if __name__ == "__main__":
    main()   
