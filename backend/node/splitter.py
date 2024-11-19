from langchain_text_splitters import RecursiveCharacterTextSplitter

def splitting(docs):
    
    all_splits = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    
    for doc in docs:
        if doc is not None:
            all_splits += text_splitter.split_documents(doc)
    
    print("The total number of splits are " + str(len(all_splits)))
    
    return all_splits