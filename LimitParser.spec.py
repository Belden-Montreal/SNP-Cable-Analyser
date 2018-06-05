import unittest
from limits.LimitParser import LimitParser
from limits.TreeItem import TreeItem
from limits.Limit import Limit

class TestLimitParser(unittest.TestCase):
    def setUp(self):
        self.parser = LimitParser("limits/test.xml")
        file = open("limits/test.xml", "r")
        self.initialFile = file.read()
        file.close()

    def test_parse(self):
        root = self.parser.parseFile()
        self.assertEqual("Standard", root.name)
        self.assertEqual("Tia", root.child(0).name)
        self.assertEqual("CAT6", root.child(0).child(0).name)
        self.assertEqual("Connecting Hardware", root.child(0).child(0).child(0).name)
        self.assertEqual(30, root.child(0).child(0).child(0).standard.limits["RL"].functions[0])

    def test_write(self):
        root = TreeItem("Standard")
        std = TreeItem("Tia", root)
        root.addChild(std)
        cat = TreeItem("CAT6", std)
        std.addChild(cat)
        hdw = TreeItem("Connecting Hardware", cat)
        cat.addChild(hdw)
        hdw.standard.limits["RL"] = Limit("RL", ["30"], [1.0, 50.0])
        self.parser.writeToFile(root)
        file = open("limits/test.xml", "r")
        self.assertEqual(self.initialFile, file.read())
        file.close()

    def tearDown(self):
        file = open("limits/test.xml", "w")
        file.write(self.initialFile)
        file.close()
        pass

if __name__ == "__main__":
    unittest.main()