import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)


def send_email(subject, message):
    """Send an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = ADMIN_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully to the admin.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_stock():
    """Check product stock and notify admin if below threshold."""
    session = SessionLocal()
    try:
        low_stock_products = session.query(Product).filter(Product.stock < 10).all()
        if low_stock_products:
            product_list = "\n".join(
                [f"Product: {product.name}, Stock: {product.stock}" for product in low_stock_products]
            )
            subject = "Low Stock Alert"
            message = f"The following products have low stock:\n\n{product_list}"
            print(f"send_email {subject} {message}")
            send_email(subject, message)
        else:
            print("No low stock products detected.")
    finally:
        session.close()

if __name__ == "__main__":
    check_stock()
