
import os

class HiveSiteParser:
    def __init__(self):
        pass

    def doProcess(self):
        dirPath = '/Users/hyundai/Work/kasugare/test/hive_site_parser/data'
        filePaths = [os.path.join(dirPath,filename) for filename in os.listdir(dirPath)]
        self.eleMap = {}

        for filePath in filePaths:
            print filePath
            fd = open(filePath, 'r')
            namekey = None

            for readline in fd.readlines():
                for line in readline.split("\n"):
                    if line.find("<name>") >= 0:
                        namekey = line.replace("<name>","").replace("</name>","").replace("\n","").replace(" ","")
                        # print " - NAME : %s" %namekey
                    if line.find("<value>") >= 0:
                        value = line.replace("<value>","").replace("</value>","").replace("\n","").replace(" ","")
                        self.addMap(namekey, value)
                        # print " - VALUE : %s" %value
            fd.close()

        keys = self.eleMap.keys()
        keys.sort()
        for k in keys:
            print "# %s    -    %s" %(k, self.eleMap[k])

        print self.makeXml()

    def addMap(self, key, value, index=0):
        if self.eleMap.has_key(key):
            index += 1
            if self.eleMap[key] != value:
                key = key.split('-')[0]
                key = "%s-%d" %(key, index)
                # self.addMap(key, value, index)
                pass
        else:
            self.eleMap[key] = value

    def makeXml(self):
        keys = self.eleMap.keys()
        keys.sort()
        elements = []
        for name in keys:
            value = self.eleMap[name]
            elements.append("    <property>\n        <name>%s</name>\n        <value>%s</value>\n    </property>" %(name, value))

        nameValues = ("\n").join(elements)
        header = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n'''
        hiveSite = "%s\n<configuration>\n%s\n</configuration>" %(header, nameValues)

        dirPath = '/Users/hyundai/Work/kasugare/test/hive_site_parser/data'
        filePath = os.path.join(dirPath, 'hive-site.xml')
        fd = open(filePath, 'w')
        fd.write(hiveSite)
        fd.close()





if __name__=='__main__':
    parser = HiveSiteParser()
    parser.doProcess()