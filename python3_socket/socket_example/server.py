#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import pickle
import time
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread

import Logger

BUFFER = 1024


class ClientListener:
    def __init__(self):
        clientQ = { 'reqQ': multiprocessing.Queue(), 'routerQ': multiprocessing.Queue() }
        self._logger = Logger().getLogger()
        self._logger.info('# process start : %s' % PROCESS_NAME)
        self._clientQ = clientQ
        self._reqQ = clientQ['reqQ']
        self._routerQ = clientQ['routerQ']

    def __del__(self):
        self._logger.warn('@ terminate process : %s' % PROCESS_NAME)

    def runServer(self):
        try:
            hostIp, hostPort = ("127.0.0.1", 5050)
            svrsock = socket(AF_INET, SOCK_STREAM)
            svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            svrsock.bind((hostIp, hostPort))
            svrsock.listen(5)

            while True:
                socketObj, addr = svrsock.accept()
                clientListener = Thread(target=self._bindClientListener, args=(socketObj, addr))
                clientListener.setDaemon(1)
                clientListener.start()

                self._logger.info("# connected client")
                self._logger.info("- client addr : %s, port : %d" % (addr[0], addr[1]))

        except KeyboardInterrupt as ki:
            self._logger.exception(ki)
        except Exception as e:
            self._logger.exception(e)
        finally:
            if socketObj:
                self._socketClose(socketObj)

    def _bindClientListener(self, socketObj, addr):
        time.sleep(1)
        network = NetworkHandler(self._logger, socketObj)
        print(network.recvMsg())

        self._socketClose(socketObj)

    def _socketClose(self, socketObj):
        try:
            if socketObj:
                socketObj.close()
                self._logger.info("# client connection closed")
        except Exception as e:
            self._logger.exception(e)


class NetworkHandler:
    def __init__(self, logger, socketObj=None):
        self._logger = logger
        self._socketObj = socketObj
        if socketObj:
            self._isAlive = True
        else:
            self._isAlive = False
        self._autoRecvQ = False
        self._workerId = None
        self._peerName = None
        if socketObj:
            self._peerName = str(socketObj.getpeername())

    def __del__(self):
        self.close()

    def connection(self, hostInfo):
        try:
            socketObj = socket(AF_INET, SOCK_STREAM)
            socketObj.connect(hostInfo)
            self._socketObj = socketObj
            self._isAlive = True
        except Exception as e:
            self._isAlive = False

    def sendMsg(self, protoMessage):
        if protoMessage['protocol'] == 'MW_NET_STAT_HB' or protoMessage['protocol'] == 'WM_NET_STAT_HB':
            pass
        else:
            self._logger.debug(">> send message : %s" % str(protoMessage))
        if not self._socketObj:
            return False
        try:
            protoMessage = pickle.dumps(protoMessage)
            sendMsg = "#%d\r\n%s" % (len(protoMessage), protoMessage)
            msgLength = len(sendMsg)
            totalsent = 0

            while totalsent < msgLength:
                sendLength = self._socketObj.send(sendMsg[totalsent:])
                if sendLength == 0:
                    break
                totalsent = totalsent + sendLength
        except Exception as e:
            if self._peerName:
                self._logger.error("# socket is closed, addr : %s" % (self._peerName))
            else:
                self._logger.error("# socket is closed")
            self._isAlive = False
            self.close()
            return False
        return True

    def recvMsg(self):
        dataBuffer = []
        try:
            receivedByte = 0
            dataLength = 0
            while True:
                if not self._socketObj:
                    print("# Step 1")
                    return False

                if receivedByte == 0:
                    print("# Step 2")
                    # data = str(self._socketObj.recv(BUFFER), 'utf-8')
                    data = str(self._socketObj.recv(BUFFER), 'utf-8')

                    print("-" * 100)
                    print(data)
                    print("-" * 100)
                    lengthIndex = data.find('\r\n')

                    if lengthIndex == -1:
                        print("# Step 3")
                        return
                    if not data:
                        print("# Step 4")
                        break

                    dataLength = int(data[:lengthIndex].split('#')[1])
                    rawData = data[lengthIndex + 2:]
                    dataBuffer.append(rawData)
                    receivedByte = len(rawData)
                    print("# Step 2-1 : %d" % dataLength)
                    print("# Step 2-2 : %s" % rawData)
                    print("# Step 2-3 : %s" % str(dataBuffer))
                    print("# Step 2-4 : %s" % receivedByte)

                if receivedByte >= dataLength:
                    print("# Step 5")
                    break

                print("# Step 6")
                data = self._socketObj.recv(min(dataLength - receivedByte, BUFFER))
                dataBuffer.append(data)

                receivedByte = receivedByte + len(str(data))
                if dataLength - receivedByte <= 0:
                    print("# Step 7")
                    break
                print("# Step 8")
            print("# Step 9")
            bufferedData = "".join(dataBuffer)
            print(bufferedData)
            print(type(bytes(bufferedData), 'utf-8'))
            print(pickle.loads(bufferedData))
            protoMessage = pickle.loads("".join(dataBuffer))
            print(protoMessage)


        except EOFError as e:
            if self._peerName:
                self._logger.error("# socket is closed, addr : %s" % (self._peerName))
            else:
                self._logger.error("# socket is closed")
            self._isAlive = False
            return None
        except Exception as e:
            self._logger.exception(e)
            if self._peerName:
                self._logger.error("# socket is closed, addr : %s" % (self._peerName))
            else:
                self._logger.error("# socket is closed")
                self._logger.exception(e)
                self._isAlive = False
            return None

        if protoMessage['protocol'] == 'MW_NET_STAT_HB' or protoMessage['protocol'] == 'WM_NET_STAT_HB':
            pass
        else:
            self._logger.debug("<< received data : %s" % str(protoMessage))
        return protoMessage

    def runMsgToQueue(self, queue):
        def _runRecvMsgQ(queue):
            while self.isAlive():
                message = self.recvMsg()
                if message:
                    queue.put_nowait(message)
                else:
                    self._isAlive = False
                    # queue.put_nowait(genConnectionLost(self.getWorkerId()))
            if self._socketObj:
                self.close()

        recvQ = Thread(target=_runRecvMsgQ, args=(queue,))
        recvQ.setDaemon(1)
        recvQ.start()

    def isAlive(self):
        return self._isAlive

    def hasWorkerId(self):
        if self._workerId:
            return True
        return False

    def setWorkerId(self, workerId):
        self._workerId = workerId

    def getWorkerId(self):
        return self._workerId

    def close(self):
        try:
            if self._socketObj:
                self._socketObj.close()
                self._logger.info("# client connection closed")
        except Exception as e:
            self._logger.exception(e)
        finally:
            self._isAlive = False


if __name__ == '__main__':
    server = ClientListener()
    server.runServer
