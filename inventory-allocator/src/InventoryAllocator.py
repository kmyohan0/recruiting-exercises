from typing import Dict, List


class Shipment:
    def __init__(self, orderedItems: dict):
        # orderedItems = Dictionary (Assume it is ordered)
        self.orderedItems = orderedItems
        for itemName, quantity in self.orderedItems.items():
            if quantity < 0:
                self.orderedItems[itemName] = 0
    # Methods need:
    # 1. Changing items in dictionary (Works like a pop() method)

    def retrieveItem(self, itemName: str, quantity: int):
        # Check if item Exists
        if itemName in self.orderedItems:
            # Then check if quantity exceed the storageAmount or not
            if quantity >= self.orderedItems[itemName]:
                # if quantity exceed our availability, we pop our item then return needed amount
                returnAmount = self.orderedItems[itemName]
                self.orderedItems.pop(itemName)
                return returnAmount
            else:
                # If not, check if quantity is 0 and update our shipments and return amount that they need
                self.orderedItems.update(
                    {itemName: (self.orderedItems[itemName]-quantity)})
                return quantity
        else:
            # if item doesn't exist in our shipment, return 0
            return -1


class Warehouse:
    def __init__(self, name="dummy", inventoryAmount={}):
        self.name = name
        self.inventoryAmount = inventoryAmount
        # In order to be safe, make every error-causing value 0 (that is, negative)
        for itemName, quantity in self.inventoryAmount.items():
            if quantity < 0:
                self.inventoryAmount[itemName] = 0

    def get_name(self):
        return self.name

    def get_inventoryAmount(self):
        return self.inventoryAmount

    def set_name(self, name):
        self.name = name

    def set_inventoryAmount(self, inventoryAmount):
        self.inventoryAmount = inventoryAmount

# Now, Class InventoryAllocator


class InventoryAllocator:
    def __init__(self):
        self.output = []

    def get_output(self, allocator: Shipment, destination: List[Warehouse]):
        for warehouseStorage in destination:
            # first, retrieve dictionary of items from each destinations
            # Then, for each keys / values inside destination, perform retrieveItem()
            providerName = warehouseStorage.get_name()
            # Since every Warehouse should be unique, check if there are any duplicate from previous output
            isDuplicate = False
            for warehouse in self.output:
                if providerName in warehouse.keys():
                    # If we find a duplicate, simply store this info
                    isDuplicate = True
            provider = {providerName: {}}
            if not isDuplicate:
                for inventory, quantity in warehouseStorage.inventoryAmount.items():
                    # Store return value from retrieveItem() and create warehouse object with it
                    amountProvided = allocator.retrieveItem(
                        inventory, quantity)
                    if amountProvided > 0:
                        provider[warehouseStorage.get_name()].update(
                            {inventory: amountProvided})
                    # Store created object and append it to output list
                    # Check if provider has any supply
                if len(provider[warehouseStorage.get_name()]) > 0:
                    self.output.append(provider)
                # if not, then forget provider
        # Now, check if we still have any leftover. If we do have it, that means our Warehouses are short on Inventory, so remove corresponding output
        for leftOverKey in allocator.orderedItems.keys():
            for wareHouseShipOutput in self.output:
                for items in wareHouseShipOutput.values():
                    if leftOverKey in items.keys():
                        self.output.pop(self.output.index(wareHouseShipOutput))
        return self.output
