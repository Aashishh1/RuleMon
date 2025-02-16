import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Function to send email
def send_email(to_address, subject, body):
    from_address = 'email'
    password = 'pass'

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)  # Replace with your SMTP server and port
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

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

# Main function to orchestrate sending emails
def main():
    violation_details = get_violation_details()

    for details in violation_details:
        name, email, registration_id, date, image_url, violation_name, penalty_amount = details
        subject = f"Traffic Violation Notification for {registration_id}"
        body = format_email_body(details)
        send_email(email, subject, body)

if __name__ == "__main__":
    main()
