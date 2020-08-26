from InventoryAllocator import Shipment, Warehouse, InventoryAllocator
import unittest

class Test(unittest.TestCase):
    # First Few from Examples
    def test_Happy_Case(self):
        # Happy Case, Exact inventory Match
        inputShipment = Shipment({ "apple" : 1 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 1})
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertEqual(check ,[{ "owd": { "apple": 1 } }])

    def test_Not_Enough_Inven(self):
        # Not enough Inventory
        inputShipment = Shipment({ "apple" : 1 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 0})
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Not_Enough_Inven_Two(self):
        # Not enough Inventory
        inputShipment = Shipment({ "apple" : 2 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 1})
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Split_Items_Evenly(self):
        # Split Items across warehouses
        inputShipment = Shipment({ "apple" : 10 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 5 })
        inputWareHouse.append(temp)
        temp = Warehouse("dm", { "apple": 5 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        # What Example output was: [{ "dm": { "apple": 5 }}, { "owd": { "apple": 5 } }]
        # Question: Why is it that Warehouse name "dm" comes first?
        # What my belief is that since question mentioned that "the list of warehouses is PRE-SORTED based on COST" 
        # Because of this, I believe return output should also be in same format.
        self.assertListEqual(check ,[{ "owd": { "apple": 5 }}, { "dm": { "apple": 5 } }])
    
    def test_Two_Or_More_Items_Split(self):
        # Complex Example from given prompt
        inputShipment = Shipment({ "apple": 5, "banana": 5, "orange": 5 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 5, "orange": 10 })
        inputWareHouse.append(temp)
        temp = Warehouse("dm", { "banana": 5, "orange": 10 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[{ "owd": { "apple": 5, "orange": 5 }}, { "dm": { "banana": 5 } }])

    #My Tests

    def test_Different_Items(self):
        # Different Items
        inputShipment = Shipment({ "apple" : 1 })
        inputWareHouse = []
        temp = Warehouse("owd", { "orange": 0})
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Uneven_Split(self):
        # Unevenly Split items
        inputShipment = Shipment({ "apple" : 10 })
        inputWareHouse = []
        temp = Warehouse("owd", { "apple": 3 })
        inputWareHouse.append(temp)
        temp = Warehouse("dm", { "apple": 7 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[{ "owd": { "apple": 3 }}, { "dm": { "apple": 7 } }])

    def test_More_Complex_Items(self):
        # Complex Items
        inputShipment = Shipment({ "apple" : 7, "banana" : 6, "cherry" : 10, "watermelon" : 4, "mango" : 2 })
        inputWareHouse = []
        temp = Warehouse("owd", { "banana": 4, "cherry": 12 })
        inputWareHouse.append(temp)
        temp = Warehouse("dm", { "apple": 4, "mango": 3, "banana": 6 })
        inputWareHouse.append(temp)
        temp = Warehouse("ama", { "apple": 3, "cherry": 2, "watermelon": 3 })
        inputWareHouse.append(temp)
        temp = Warehouse("tw", { "watermelon": 4, "lime": 12 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[{ "owd": { "banana": 4, "cherry": 10 }}, { "dm": { "apple": 4, "mango": 2, "banana": 2 }}, { "ama": { "apple": 3, "watermelon": 3 }}, { "tw": { "watermelon": 1 }}])

    def test_Empty_In_WareHouse(self):
        inputShipment = Shipment({ "apple" : 2 })
        inputWareHouse = []
        # Empty in WareHouse
        temp = Warehouse("owd", {})
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Error_In_WareHouse(self):
        inputShipment = Shipment({ "apple" : 2 })
        inputWareHouse = []
        # Error in WareHouse System (Having Apple -1)
        temp = Warehouse("owd", { "apple": -1 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Error_In_Shipment(self):
        inputShipment = Shipment({ "apple" : -1 })
        inputWareHouse = []
        # Error in WareHouse System (Having Apple -1)
        temp = Warehouse("owd", { "apple": 5 })
        inputWareHouse.append(temp)
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

    def test_Error_In_WareHouse_Two(self):
        inputShipment = Shipment({ "apple" : 10 })
        inputWareHouse = []
        # Error in WareHouse System (Consider Two WareHouses are Same)
        temp = Warehouse("owd", { "apple": 5 })
        inputWareHouse.append(temp)
        temp = Warehouse("owd", { "apple": 5 })
        inputWareHouse.append(temp)
        # Although having Two SAME Warehouse in result wouldn't cause much difference afterwards (Still same price be affected)
        # But if there are any fees are applied FOR EACH WAREHOUSE in InventoryAllocator System, then we should dynamically combine those two same Warehouse
        # (Combine = delete one of those two) (Since I believe that error will produce Duplicate Element, NOT TWO WAREHOUSE SPLIT ITEM QUANTITY )
        check = InventoryAllocator().get_output(inputShipment, inputWareHouse)
        self.assertListEqual(check ,[])

if __name__ == '__main__':
   unittest.main()