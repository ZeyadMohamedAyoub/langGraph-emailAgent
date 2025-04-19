from states import EmailState
from nodes import (
    N_1_read_email,
    N_2_classify_email,
    N_3_spam_handler,
    N_4_response_suggester,
    N_5_the_notifier
)
from langgraph.graph import StateGraph, START, END

def create_email_processing_graph():
    workflow = StateGraph(EmailState)
    workflow.add_node("read_email", N_1_read_email)
    workflow.add_node("classify_email", N_2_classify_email)
    workflow.add_node("spam_handler", N_3_spam_handler)
    workflow.add_node("response_suggester", N_4_response_suggester)
    workflow.add_node("the_notifier", N_5_the_notifier)
    
    #edges
    workflow.add_edge(START, "read_email")
    workflow.add_edge("read_email", "classify_email")
    # workflow.add_edge("classify_email", "spam_handler", condition=route_email)
    # workflow.add_edge("classify_email", "response_suggester", condition=lambda state: not state["is_spam"])
    
    #conditional edge
    workflow.add_conditional_edges(
        "classify_email",lambda state: "spam_handler" if state["is_spam"] else "response_suggester"
    )
    workflow.add_edge("spam_handler", END)
    workflow.add_edge("response_suggester", "the_notifier")
    workflow.add_edge("the_notifier", END)

    return workflow.compile()

email_processor = create_email_processing_graph()

# email_processor.get_graph().draw_mermaid_png()