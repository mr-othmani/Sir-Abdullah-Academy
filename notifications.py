import os
import logging
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

def send_whatsapp_confirmation(to_number: str, student_name: str, course_name: str) -> bool:
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logging.warning("Twilio credentials missing. Skipping WhatsApp notification.")
        return False

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format destination phone number for Twilio WhatsApp format
        formatted_phone = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"

        body_text = (
            f"🎓 *Sir Abdullah Academy*\n\n"
            f"Dear {student_name},\n"
            f"We have received your admission application for *{course_name}*!\n\n"
            f"Our onboarding representative will contact you on this number within 24 hours to finalize your schedule and Zoom portal login credentials.\n\n"
            f"Thank you for choosing Sir Abdullah Academy!"
        )

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body_text,
            to=formatted_phone
        )
        return bool(message.sid)
    except Exception as e:
        logging.error(f"Failed to send WhatsApp message: {e}")
        return False
