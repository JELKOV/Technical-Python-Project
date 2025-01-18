# class NotificationManager:
#     #This class is responsible for sending notifications with the deal flight details.
#     def __init__(self):
#         self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#
#     def send_sms(self, message):
#         message = self.client.messages.create(
#             body=message,
#             from_=TWILIO_PHONE_NUMBER,
#             to=USER_PHONE_NUMBER
#         )
#         print(f"Message sent: {message.sid}")