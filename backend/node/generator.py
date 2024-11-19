from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_together import ChatTogether

llm = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", temperature=0.4)

def generating(state):
    
    prompt = PromptTemplate(
        input_variables=["question", "document"],
        template="""You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question.
        If the context have nothing to be related with the question, just answer dont't know.
        If name or short answer are required in the question, answer only the required item without elaboration.
        If content or fun fact is asked then answer as much as possible.
        Keep the answer concise."
        Here is the user question: {question}
        \n\n
        Here are the context:
        {document}
        """,
    )

    generating_chain = prompt | llm | StrOutputParser()
    
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    retry_count = state["retry_count"]
    
    if retry_count >= 2:
        print("---DECISION: EXCEED MAX RETRY---")
        retry_count -= 1   
        return {"next": False}

    response = generating_chain.invoke({"question": question,  "document": documents})

    print("THIS IS THE RESPONSE \n", response + "\n")

    return {"documents": documents, "question": question, "generation": response, "next": True}


def content_generating(state):

    prompt = PromptTemplate(
        input_variables=["question", "document"],
        template="""You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question.
        If the context have nothing to be related with the question, just answer dont't know.
        If name or short answer are required in the question, answer only the required item without elaboration.
        If content or fun fact is asked then answer as much as possible.
        Keep the answer concise."
        Here is the user question: {question}
        \n\n
        Here are the context:
        {document}
        """,
    )

    generating_chain = prompt | llm | StrOutputParser()

    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    retry_count = state["retry_count"]

    if retry_count >= 3:
        print("---DECISION: EXCEED MAX RETRY---")
        retry_count -= 1   
        return {"next": False}

    response = generating_chain.invoke({"question": question,  "document": documents})

    print("THIS IS THE RESPONSE \n", response + "\n")

    return {"documents": documents, "question": question, "generation": response, "next": True}