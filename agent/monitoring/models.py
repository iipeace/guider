from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class CPU(db.EmbeddedDocument):
    kernel = db.IntField(default=0)
    user = db.IntField(default=0)
    irq = db.IntField(default=0)
    nrCore = db.IntField(default=0)
    total = db.IntField(default=0)


class Memory(db.EmbeddedDocument):
    kernel = db.IntField(default=0)
    cache = db.IntField(default=0)
    free = db.IntField(default=0)
    anon = db.IntField(default=0)
    total = db.IntField(default=0)


class Storage(db.EmbeddedDocument):
    free = db.IntField(default=0)
    usage = db.IntField(default=0)
    total = db.IntField(default=0)


class Network(db.EmbeddedDocument):
    inbound = db.IntField(default=0)
    outbound = db.IntField(default=0)


class Data(db.Document):
    timestamp = db.DateTimeField(default=datetime.utcnow)
    mac_addr = db.StringField()
    cpu = db.EmbeddedDocumentField(CPU)
    memory = db.EmbeddedDocumentField(Memory)
    storage = db.EmbeddedDocumentField(Storage)
    network = db.EmbeddedDocumentField(Network)


def spread_data(data):
    result = dict()
    result.update(spread_cpu(data.cpu))
    result.update(spread_storage(data.storage))
    result.update(spread_memory(data.memory))
    result.update(spread_network(data.network))
    return result


def spread_cpu(cpu):
    return dict(cpu_kernel=cpu.kernel, cpu_user=cpu.user,
                cpu_irq=cpu.irq, cpu_nrCore=cpu.nrCore,
                cpu_total=cpu.total)


def spread_storage(storage):
    if storage:
        return dict(
            storage_free=storage.free,
            storage_usage=storage.usage,
            storage_total=storage.total
        )
    else:
        return dict(
            storage_free=0,
            storage_usage=0,
            storage_total=0
        )


def spread_memory(memory):
    return dict(
        memory_kernel=memory.kernel,
        memory_cache=memory.cache,
        memory_free=memory.free,
        memory_anon=memory.anon,
        memory_total=memory.total
    )


def spread_network(network):
    return dict(
        network_inbound=network.inbound,
        network_outbound=network.outbound
    )


def deserialize_data(data):
    return {
        "cpu": {
            "kernel": data.cpu_kernel,
            "user": data.cpu_user,
            "irq": data.cpu_irq,
            "nrCore": data.cpu_nrCore,
            "total": data.cpu_total
        },
        "storage": {
            "free": data.storage_free,
            "usage": data.storage_usage,
            "total": data.storage_total
        },
        "memory": {
            "kernel": data.memory_kernel,
            "cache": data.memory_cache,
            "free": data.memory_free,
            "anon": data.memory_anon,
            "total": data.memory_total
        },
        "network": {
            "inbound": data.network_inbound,
            "outbound": data.network_inbound
        }
    }