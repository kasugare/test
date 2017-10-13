#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pickle
import traceback
from socket import AF_INET, SOCK_STREAM, socket


class SimpleClient:
    def __init__(self):
        self.__hostIp = '127.0.0.1'
        self.__hostPort = 9999

    def __connServer(self):
        socketObj = socket(AF_INET, SOCK_STREAM)
        socketObj.connect((self.__hostIp, self.__hostPort))
        sender = DataSender(socketObj)
        receiver = DataReceiver(socketObj)
        return sender, receiver

    def doProcess(self):
        sender, receiver = self.__connServer()
        jsonString = '{"context": {"task": {"#01": {"input_data": {"data": "./test_data.csv", "type": {"age": "int", "code": "int", "id": "int", "name": "string"}}, "predict": {"name": "predict"}, "output_data": {"data_schema": ["string", ["int", "int"], "string"], "save_type": "file", "output_data_path": "./output_data_file", "data_type": "matrix"}, "model": {"hyper_params": {"a": 1, "c": 3, "b": 2}, "name": "descision tree"}, "evaluation": {"name": "evaluation"}, "ml_tools": "sclearn"}}, "context_version": "0.0.1"}}'
        jsonData = json.loads(jsonString)
        sender.sendMsg(jsonData)



class DataSender:
    def __init__(self, socketObj):
        self.__socketObj = socketObj

    def sendMsg(self, protoMessage):
        print(">> send message : %s" % str(protoMessage))
        try:
            protoMessage = json.dumps(protoMessage)
            print(protoMessage, type(protoMessage))
            # protoMessage = pickle.dumps(protoMessage)
            message = '#%d\r\n%s' % (len(protoMessage), protoMessage)
            print("# Step 1:", message)
            msgLength = len(message)
            totalsent = 0

            while totalsent < msgLength:
                message = bytes(message[totalsent:], 'utf-8')
                # temp = message[len(str("#%d\r\n" % len(protoMessage))):]
                # print("# Step 3:", str(message, 'utf-8'))
                # print("# Step 4:", pickle.loads(temp, encoding='string'))
                # print("# Step 5:", pickle.loads(message[len(str("#%d\r\n" %len(protoMessage))):]))
                sendLength = self.__socketObj.send(message)
                if sendLength == 0:
                    break
                totalsent = totalsent + sendLength

        except Exception as e:
            print("[warn] Network error")
            print(traceback.format_exc())
            return False
        return True

    def close(self):
        self.__socketObj.close()


class DataReceiver:
    def __init__(self, socketObj):
        self._socketObj = socketObj
        self.__BUFFER = 1024

    def recvMsg(self):
        dataBuffer = []
        try:
            receivedByte = 0
            dataLength = 0
            while True:
                if receivedByte == 0:
                    data = str(self._socketObj.recv(self.__BUFFER), 'utf-8')
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

                data = self._socketObj.recv(min(dataLength - receivedByte, BUFFER))
                dataBuffer.append(data)

                receivedByte = receivedByte + len(str(data))
                if dataLength - receivedByte <= 0:
                    break

        except Exception as e:
            print(traceback.format_exc(e))

        print("".join(dataBuffer))
        protoMessage = pickle.loads("".join(dataBuffer))
        print("<< received data : %s" % str(protoMessage))
        return protoMessage

    def close(self):
        self._socketObj.close()


if __name__ == "__main__":
    SimpleClient().doProcess()
