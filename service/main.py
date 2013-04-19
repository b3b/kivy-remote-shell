
import os

# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.base import EventLoop

from twisted.internet import reactor
from twisted.cred import portal, checkers
from twisted.conch import manhole, manhole_ssh


def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    def getManhole(_):
        return manhole.ColoredManhole(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_SERVICE_ARGUMENT', '8000'))
    connection = reactor.listenTCP(port,
                                   getManholeFactory(globals(), admin='kivy'))
    EventLoop.event_listeners = [None]  # need some to listen, or loop quit
    EventLoop.start()
    EventLoop.run()
