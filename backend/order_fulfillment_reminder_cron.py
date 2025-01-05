import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship


# Database Configuration
DATABASE_URL = "postgresql://postgres:root@localhost/thepointy"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "niteshsahujhansi@gmail.com"
SMTP_PASSWORD = "cucp uams vuhe hvgk"
ADMIN_EMAIL = "niteshsahu920@gmail.com"

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    # product = relationship("Product", back_populates="orders")



def send_email(subject, message, recipient):
    """Send an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {recipient}.")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def send_reminders():
    """Send reminders for orders pending for more than 24 hours."""
    session = SessionLocal()
    try:
        # Calculate the cutoff time (24 hours ago)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)

        pending_orders = (
            session.query(Order)
            .join(User, Order.user_id == User.id)
            .filter(Order.status == "Pending", Order.created_at <= cutoff_time)
            .all()
        )

        if pending_orders:
            for order in pending_orders:
                subject = "Order Fulfillment Reminder"
                message = (
                    f"Dear Customer,\n\n"
                    f"Your order with ID {order.id} is still pending. Please take action to fulfill it.\n\n"
                    f"Thank you,\nYour Company"
                )
                send_email(subject, message, order.user.email)
            print(f"Sent reminders for {len(pending_orders)} pending orders.")
        else:
            print("No pending orders older than 24 hours.")
    finally:
        session.close()

if __name__ == "__main__":
    send_reminders()
