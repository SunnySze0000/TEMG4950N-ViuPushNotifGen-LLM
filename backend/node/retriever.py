from typing import List
from langchain_together import ChatTogether
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.output_parsers import PydanticToolsParser
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0)

class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""
    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))

def retrieving(state):

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from a vector
        database. By generating multiple perspectives on the user question, your goal is to help
        the user overcome some of the limitations of the distance-based similarity search.
        Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    retrieving_chain = QUERY_PROMPT | llm | LineListOutputParser()

    print("---RETRIEVE---")
    question = state["question"]
    vectorstore = state["vectorstore"]

    retriever = MultiQueryRetriever(
        retriever = vectorstore.as_retriever(search_type="mmr"),
        llm_chain = retrieving_chain,
        parser_key = "lines"
    )

    documents = retriever.invoke(question)

    return {"documents": documents, "question": question}

def wiki_retrieving(vectorstore, cast, series_name):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    question = "Tell me more about the character acted by " + cast + " in the series: " + series_name
    retrieved_doc = retriever.invoke(question)
    
    print("The following are retrieved:")
    #for doc in retrieved_doc:
    #    print(doc)
    
    return 
    
def wiki_content_retrieving(vectorstore, series_name):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    question = "Tell me more about the series: " + series_name
    retrieved_doc = retriever.invoke(question)
    
    print("The following are retrieved:")
    #for doc in retrieved_doc:
    #    print(doc)
    
    return

def reranker_retrieving(question, vectorstore):

    print("---RETRIEVE---")

    retriever = vectorstore.as_retriever(search_type="mmr")
    
    compressor = FlashrankRerank()
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    retrieved_doc = compression_retriever.invoke(question)

    #for doc in retrieved_doc:
    #    print(doc)

    return retrieved_doc

def retrieve_and_rerank(state):

    class SubQuery(BaseModel):
        sub_query: str = Field(
            ...,
            description="A very specific query against the database.",
        )

    print("---GENERATE SUBQUESTIONS---")

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from a vector
        database. By generating multiple perspectives on the user question, your goal is to help
        the user overcome some of the limitations of the distance-based similarity search.
        Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    llm_with_tools = llm.bind_tools([SubQuery])
    parser = PydanticToolsParser(tools=[SubQuery])
    multiquery_chain = QUERY_PROMPT | llm_with_tools | parser

    question = state["question"]
    vectorstore = state["vectorstore"]

    sub_questions = multiquery_chain.invoke({"question": question})

    #-----------------Retrieve-----------------

    print("---RETRIEVE---")

    retriever = vectorstore.as_retriever(search_type="mmr")
    
    compressor = FlashrankRerank(model="ms-marco-TinyBERT-L-2-v2")

    print("---Testing 1---")
    
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    print("---Testing 2---")

    documents = []
    for q in sub_questions:
        print("--- Testing q loop---")
        documents.extend(compression_retriever.invoke(q.sub_query))

    print("---End Testing---")
    
    return {"documents": documents, "question": question}
    
    
        
