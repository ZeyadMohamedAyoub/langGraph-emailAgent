from langchain_ollama import OllamaLLM
from states import EmailState
from langchain_core.messages import HumanMessage
import re
import json

try:
    # model = OllamaLLM(model="mistral:latest")#Worked perfect https://cloud.langfuse.com/project/cm9owmw1x00kuad07gyk0xs5r/traces
    model = OllamaLLM(model="llama3.2:latest")#Done the work as perfect approx 1 sec less each
except Exception as e:
    print(f"Warning: Could not initialize Ollama model: {e}")
    exit()
    # print("Using fallback responses")
    # model = None

def N_1_read_email(state: EmailState):
    email = state["email"]
    print(f"Agent is processing an email from {email['sender']} with subject: {email['subject']}")

    return {} #as no changes to state it just reads the email


#agent uses LLM to classify email
def N_2_classify_email(state: EmailState):
    email = state["email"]

    prompt = f"""
    You are an email classification agent.
    Classify the email as either 'spam' or 'not spam'. 

    Email: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    Classify:
    If this email is spam, explain why,
    If it is legitimate, categorize it (inquiry, complaint, thank you, etc.)
    response in JSON with keys without any further context:
    - email_category: str
    - spam_reason: str | null
    - is_spam: bool
    """
    

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        try:
            json_string = json_match.group(0)
            parsed_json = json.loads(json_string)

            is_spam = parsed_json.get("is_spam", False)
            spam_reason = parsed_json.get("spam_reason", None)
            email_category = parsed_json.get("email_category", "unknown")
        except json.JSONDecodeError:
            print("Failed to parse JSON response from LLM")
            is_spam = False
            spam_reason = None
            email_category = "parsing_error"
    else:
        print("Failed to extract JSON response from LLM")
        is_spam = False
        spam_reason = None
        email_category = "parsing_error"
    
    existing_messages = state.get("messages", [])

    new_messages = existing_messages + [{"role": "user", "content": prompt}, {"role": "assistant", "content": str(response)}]
    #parse response 
    #update messages for tracking
    #return state updates
    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": new_messages
    }
    
def N_3_spam_handler(state: EmailState):
    print(f"Agent has marked the email as spam. Reason: {state['spam_reason']}")
    print("Accordingly agent has thrown it away.")
    
    #as done processing this email
    return {}


def N_4_response_suggester(state: EmailState):
    email = state["email"]
    category = state["email_category"] or "general"

    prompt = f"""
    You are an email response agent.
    Suggest a response to the email based on its category as it is categorized as: {category}

    Email: 
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    Suggest a response:
    response in JSON with keys without any further context:
    - email_draft: str
    """

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    
    print(f"--------------------->Agent has suggested a response draft: {response}")

    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        try:
            json_string = json_match.group(0)
            parsed_json = json.loads(json_string)
            response = parsed_json.get("email_draft", "Default")
        except json.JSONDecodeError:
            print("Failed to parse JSON response from LLM")
            response = "Error parsing response"
    else:
        print("Failed to extract JSON response from LLM")
        response = "Error parsing response"

    
    existing_messages = state.get("messages", [])
    new_messages = existing_messages + [{"role": "user", "content": prompt}, {"role": "assistant", "content": str(response)}]

    return {
        "email_draft": response,
        "messages": new_messages
    }
    
def N_5_the_notifier(state: EmailState):
    email = state["email"]

    print("\n" + "-"*50)
    print(f"You've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print(f"category: {state['email_category']}")
    print("\nI've prepared a response draft for your review:")
    print("-"*50 + "\n")
    print(state["email_draft"])
    print("-"*50 + "\n")

    #cleared states for next email
    #as done processing this email
    return {}
