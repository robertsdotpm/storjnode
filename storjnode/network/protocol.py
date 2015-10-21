try:
    from Queue import Queue  # py2
except ImportError:
    from queue import Queue  # py3
from kademlia.protocol import KademliaProtocol


class StorjProtocol(KademliaProtocol):

    def __init__(self, *args, **kwargs):
        self.messages_received = Queue()
        KademliaProtocol.__init__(self, *args, **kwargs)

    def rpc_message(self, sender, message):
        self.messages_received.put({ "sender": sender, "message": message})
        return (sender[0], sender[1])  # return (ip, port)

    def callMessage(self, nodeToAsk, message):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.message(address, self.sourceNode.id, message)
        return d.addCallback(self.handleCallResponse, nodeToAsk)
