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


def deserialize_data(data, cnt):
    if cnt == 0:
        cnt = 1
    return {
        "cpu": {
            "kernel": data.get('cpu_kernel', 0)/cnt,
            "user": data.get('cpu_user', 0)/cnt,
            "irq": data.get('cpu_irq', 0)/cnt,
            "nrCore": data.get('cpu_nrCore', 0)/cnt,
            "total": data.get('cpu_total', 0)/cnt
        },
        "storage": {
            "free": data.get('storage_free', 0)/cnt,
            "usage": data.get('storage_usage', 0)/cnt,
            "total": data.get('storage_total', 0)/cnt
        },
        "memory": {
            "kernel": data.get('memory_kernel', 0)/cnt,
            "cache": data.get('memory_cache', 0)/cnt,
            "free": data.get('memory_free', 0)/cnt,
            "anon": data.get('memory_anon', 0)/cnt,
            "total": data.get('memory_total', 0)/cnt
        },
        "network": {
            "inbound": data.get('network_inbound', 0)/cnt,
            "outbound": data.get('network_inbound', 0)/cnt
        }
    }
