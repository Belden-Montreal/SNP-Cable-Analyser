import xmltodict
from limits.TreeItem import TreeItem
from limits.Limit import Limit
class LimitParser():

    def __init__(self, url):
        self.url = url
        self.NAME_BY_LEVEL = ["Category", "Hardware", "Limit", "Part"]

    def parseFile(self):
        dataFile = open(self.url, "r")
        dictData = xmltodict.parse(dataFile.read())
        rootItem = TreeItem(dictData["Root"]["@name"])
        self.parseProperty("Standard", rootItem, dictData["Root"])
        dataFile.close()
        return rootItem

    def parseProperty(self, name, parent, data):
        if not isinstance(data[name], list):
            properties = [data[name]]
        else:
            properties = data[name]
        for prop in properties:
            if "@name" in prop:
                item = TreeItem(prop["@name"], parent)
                parent.addChild(item)
                for nextName in prop:
                    if not nextName == "@name":
                        self.parseProperty(nextName, item, prop)
            elif "#text" in prop:
                    if "@min" in prop:
                        parent.bounds.append(float(prop["@min"]))
                    if "@max" in prop:
                        parent.bounds.append(float(prop["@max"]))
                    parent.clauses.append(prop["#text"])
                    parent.parseClauses(parent.clauses)
            elif "Part" in prop:
                parent.standard.limits[prop["@param"]] = Limit(prop["@param"], [], [])
                self.parseProperty("Part", parent.standard.limits[prop["@param"]], prop)

    def writeToFile(self, root):
        dataFile = open(self.url, "w")
        dictData = self.updateDict(root)
        xmltodict.unparse(dictData, dataFile, pretty=True)
        dataFile.close()

    def updateDict(self, root):
        dictData = {}
        standardItems = self.constructDict(root, 0)
        if len(standardItems) > 0:
            dictData = {"Root": {"@name": "Standard", "Standard": standardItems}}
        else:
            dictData = {"Root": {"@name": "Standard"}}
        print(dictData)
        return dictData

    def constructDict(self, parent, k):
        items = []
        if k >= len(self.NAME_BY_LEVEL):
            for i, part in enumerate(parent.clauses):
                if i == 0:
                    partEntry = {"@min": parent.bounds[i], "@max": parent.bounds[i+1], "#text": part}
                else:
                    partEntry = {"@max": parent.bounds[i+1], "#text": part}                                        
                items.append(partEntry)
        elif parent.childCount() == 0:
            for limit in parent.standard.limits.values():
                if not (limit.clauses[0] == ""):
                    items.append({"@param": limit.parameter, self.NAME_BY_LEVEL[k]: self.constructDict(limit, k+1)})
        else:
            for child in parent.children:
                items.append({"@name": child.name, self.NAME_BY_LEVEL[k]: self.constructDict(child, k+1)})
        return items