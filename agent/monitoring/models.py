from flask_mongoengine import MongoEngine
from datetime import datetime
db = MongoEngine()


class CPU(db.EmbeddedDocument):
    kernel = db.IntField()
    user = db.IntField()
    irq = db.IntField()
    nrCore = db.IntField()
    total = db.IntField()


class Memory(db.EmbeddedDocument):
    kernel = db.IntField()
    cache = db.IntField()
    free = db.IntField()
    anon = db.IntField()
    total = db.IntField()


class Storage(db.EmbeddedDocument):
    free = db.IntField()
    usage = db.IntField()
    total = db.IntField()


class Network(db.EmbeddedDocument):
    inbound = db.IntField()
    outbound = db.IntField()


class Data(db.Document):
    timestamp = db.DateTimeField(default=datetime.utcnow)
    cpu = db.EmbeddedDocumentField(CPU)
    memory = db.EmbeddedDocumentField(Memory)
    storage = db.EmbeddedDocumentField(Storage)
    network = db.EmbeddedDocumentField(Network)
