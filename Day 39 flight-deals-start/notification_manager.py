from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONENUM, TWILIO_USER_PHONENUM
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_whatsapp(self, message):
        """
        Twilio API를 사용하여 WhatsApp 메시지 전송
        :param message: 전송할 메시지 내용
        """
        try:
            message = self.client.messages.create(
                body=message,  # 메시지 내용
                from_=TWILIO_PHONENUM,  # Twilio WhatsApp 발신 번호
                to=TWILIO_USER_PHONENUM  # 수신자 WhatsApp 번호
            )
            print(f"Message sent successfully: {message.sid}")
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")