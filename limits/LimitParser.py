import xmltodict
from limits.TreeItem import TreeItem
from limits.Limit import Limit

class LimitParser():
    def __init__(self, url):
        self.url = url

    def parseFile(self):
        file = open(self.url, "r")
        dictData = xmltodict.parse(file.read())
        rootItem = TreeItem(dictData["Root"]["@name"])
        self.parseProperty("Standard", rootItem, dictData["Root"])
        file.close()
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
        file = open(self.url, "w")
        dictData = self.updateDict(root)
        xmltodict.unparse(dictData, file, pretty=True)
        file.close()

    def updateDict(self, root):
        dictData = {}
        standardItems = []
        for standard in root.children:
            categoryItems = []
            for category in standard.children:
                hardwareItems = []
                for hardware in category.children:
                    limitItems = []
                    for limit in hardware.standard.limits.values():
                        if not (limit.clauses[0] == ""):
                            partItems = []
                            i = 0
                            for part in limit.clauses:
                                if i == 0:
                                    partEntry = {"@min": limit.bounds[i], "@max": limit.bounds[i+1], "#text": part}
                                else:
                                    partEntry = {"@max": limit.bounds[i+1], "#text": part}                                        
                                partItems.append(partEntry)
                                i += 1
                            limitEntry = {"@param": limit.parameter, "Part": partItems}
                            limitItems.append(limitEntry)
                    if len(limitItems) > 0:
                        hardwareItems.append({"@name": hardware.name, "Limit": limitItems})
                    else:
                        hardwareItems.append({"@name": hardware.name})
                if len(hardwareItems) > 0:
                    categoryItems.append({"@name": category.name, "Hardware": hardwareItems})
                else:
                    categoryItems.append({"@name": category.name})
            if len(categoryItems) > 0: 
                standardItems.append({"@name": standard.name, "Category": categoryItems})
            else:
                standardItems.append({"@name": standard.name})
        if len(standardItems) > 0:
            dictData = {"Root": {"@name": "Standard", "Standard": standardItems}}
        else:
            dictData = {"Root": {"@name": "Standard"}}
        return dictData