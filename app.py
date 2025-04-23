from graph import email_processor
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
import os
from dotenv import load_dotenv
load_dotenv()
# https://langfuse.com/docs/sdk/python/low-level-sdk#initialize-client
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LF_SEC_KEY")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LF_PUB_KEY")
os.environ["LANGFUSE_HOST"] = os.getenv("LF_HOST")
langfuse_handler = CallbackHandler()
# legit_res = email_processor.invoke({"email": legit_email}, config={"callbacks": [langfuse_handler]})
# spam_res = email_processor.invoke({"email": spam_email}, config={"callbacks": [langfuse_handler]})
    

def process_email(email, callbacks=None):
    result = email_processor.invoke({"email": email}, config={"callbacks": callbacks})
    return result

if __name__ == "__main__":
    legit_email = {
        "sender": "ayoubzeyad@yahoo.com",
        "subject": "Meeting Reminder",
        "body": "Don't forget our meeting tomorrow at 3 PM.",
    }
    # result = process_email(legit_email, callbacks=[langfuse_handler])
    result = process_email(legit_email)
    print("\n\nFinal legit Done\n")
    # print(result)
    
    spam_email = {
        "sender": "win-money-now@hotmail.com",
        "subject": "YOU WON $10,000,000!!!",
        "body": "CONGRATULATIONS! you've been selected to receive $10,0000,000! Send your bank details to claim your prize NOW!!!"
    }

    result = process_email(spam_email)
    # result = process_email(spam_email, callbacks=[langfuse_handler])
    print("\n\nFinal spam Done\n")
    # print(result)
    
    # pip install langfuse
    