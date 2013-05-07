from django.conf import settings
from twilio.rest import TwilioRestClient

from planit.accounts.models import generate_verification_token

import logging
logger = logging.getLogger(__name__)

def send_verification(user):
    verification_token = generate_verification_token(user)

    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    body = "Hey there from gogroup.us! Go to http://gogroup.us/v/?token=%s to verify your phone." % verification_token.token
    
    logger.debug(body)
    logger.debug(settings.TWILIO_PHONE_NUMBER)
    message = client.sms.messages.create(to=str(user.phone),
                                        from_=settings.TWILIO_PHONE_NUMBER,
                                        body=str(body))