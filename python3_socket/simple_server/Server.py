#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pickle
import traceback
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread


class SimpleServer:
    def __init__(self):
        self.__hostIp = '127.0.0.1'
        self.__hostPort = 9999

    def __socketClose(self, socketObj):
        try:
            if socketObj:
                socketObj.close()
                print("# client connection closed")
        except Exception as e:
            self._logger.exception(e)

    def __bindClientListener(self, socketObj, addr):
        clientListener = ClientListener(socketObj, addr)
        clientListener.doProcess()

    def runServer(self):
        try:
            svrsock = socket(AF_INET, SOCK_STREAM)
            svrsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            svrsock.bind((self.__hostIp, self.__hostPort))
            svrsock.listen(5)

            while True:
                socketObj, addr = svrsock.accept()
                clientListener = Thread(target=self.__bindClientListener, args=(socketObj, addr))
                clientListener.setDaemon(1)
                clientListener.start()

                print("# Connected Client")
                print(" - client addr : %s, port : %d" % (addr[0], addr[1]))

        except Exception as e:
            print(traceback.format_exc(e))


class ClientListener:
    def __init__(self, socketObj, addr):
        self.__socketObj = socketObj
        self.__addr = addr
        self.__buffer = 2048
        self.__peerName = None

        if socketObj:
            self.__peerName = str(socketObj.getpeername())

    def __close(self):
        try:
            if self.__socketObj:
                self.__socketObj.close()
                print("# client connection closed")
        except Exception as e:
            print(traceback.format_exc(e))

    def sendMsg(self, protoMessage):
        if not self.__socketObj:
            return False

        if protoMessage['protocol'] == 'MW_NET_STAT_HB' or protoMessage['protocol'] == 'WM_NET_STAT_HB':
            pass
        else:
            print(">> send message : %s" % str(protoMessage))

        try:
            protoMessage = pickle.dumps(protoMessage)
            sendMsg = "#%d\r\n%s" % (len(protoMessage), protoMessage)
            msgLength = len(sendMsg)
            totalsent = 0

            while totalsent < msgLength:
                sendLength = self.__socketObj.send(sendMsg[totalsent:])
                if sendLength == 0:
                    break
                totalsent = totalsent + sendLength

        except Exception as e:
            if self.__peerName:
                print("# socket is closed, addr : %s" % (self.__peerName))
            else:
                print("# socket is closed")
            self.__close()
            return False
        return True

    def recvMsg(self):
        dataBuffer = []

        try:
            receivedByte = 0
            dataLength = 0

            while True:
                if not self.__socketObj:
                    return False

                if receivedByte == 0:
                    data = str(self.__socketObj.recv(self.__buffer), 'utf-8')
                    lengthIndex = data.find('\r\n')

                    if lengthIndex == -1:
                        return

                    if not data:
                        break

                    dataLength = int(data[:lengthIndex].split('#')[1])
                    rawData = data[lengthIndex + 2:]
                    dataBuffer.append(rawData)
                    receivedByte = len(rawData)

                if receivedByte >= dataLength:
                    break

                data = self.__socketObj.recv(min(dataLength - receivedByte, self.__buffer))
                dataBuffer.append(data)
                receivedByte = receivedByte + len(str(data))

                if dataLength - receivedByte <= 0:
                    break

        except EOFError as e:
            if self.__peerName:
                print("# socket is closed, addr : %s" % (self.__peerName))
            else:
                print("# socket is closed")
            return None

        except Exception as e:
            if self.__peerName:
                print("# socket is closed, addr : %s" % (self.__peerName))
            else:
                print("# socket is closed")
                print(traceback.format_exc(e))

        bufferedData = ''.join(dataBuffer)
        receivedMsg = json.loads(bufferedData)
        self.__printJson(receivedMsg)

    def __printJson(self, message):
        print(json.dumps(message, sort_keys=True, indent=4));

    def doProcess(self):
        self.recvMsg()


if __name__ == '__main__':
    server = SimpleServer()
    server.runServer()
