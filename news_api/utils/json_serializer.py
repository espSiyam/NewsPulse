from bson import ObjectId

def convert_object_id(doc):
    if isinstance(doc, list):
        return [convert_object_id(d) for d in doc]
    if isinstance(doc, dict):
        return {k: convert_object_id(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc
