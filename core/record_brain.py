import os

DATA_PATH = "/ai_system/data/RecordRoom"


def search_documents(query):
    results = []

    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if query.lower() in file.lower():
                results.append(os.path.join(root, file))

    return results[:5]
