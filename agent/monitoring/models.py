from flask_mongoengine import MongoEngine
from datetime import datetime
db = MongoEngine()

class CPU(db.EmbeddedDocuments):
    kernel=db.IntField()
    user=db.IntField()
    irq=db.IntField()
    nrCore=db.IntField
    total=db.IntField()
class Memory(db.EmbeddedDocuments):
    kernel = db.IntField()
    cache = db.IntField()
    free = db.IntField()
    anon = db.IntField()
    total = db.IntField()
class Storage(db.EmbeddedDocuments):
    free = db.IntField()
    usage = db.IntField()
    total = db.IntField()
class Network(db.EmbeddedDocuments):
    inbound = db.IntField()
    outbound = db.IntField()
class Data(db.Document):
    timestamp = db.DateTimeField(default=datetime.utcnow)
    cpu = db.EmbeddedDocumentField(CPU)
    memory = db.EmbeddedDocumentField(Memory)
    storage = db.EmbeddedDocumentField(Storage)
    network = db.EmbeddedDocumentField(Network)
