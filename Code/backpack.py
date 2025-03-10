
class Backpack:
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.slots = [None] * capacity

    def add_item(self, item, quantity=1):

        if item.stackable:
            quantity_left = quantity
            for i in range(self.capacity):
                slot = self.slots[i]
                if slot and slot["item"].name == item.name:
                    max_can_stack = item.stack_limit - slot["quantity"]
                    if max_can_stack > 0:
                        amount_to_add = min(max_can_stack, quantity_left)
                        slot["quantity"] += amount_to_add
                        quantity_left -= amount_to_add
                        if quantity_left <= 0:
                            return True
            
            while quantity_left > 0:
                free_index = self._find_free_slot()
                if free_index == -1:
                    return False
                amount_to_add = min(item.stack_limit, quantity_left)
                self.slots[free_index] = {"item": item, "quantity": amount_to_add}
                quantity_left -= amount_to_add
            return True
        else:
            added_any = False
            for _ in range(quantity):
                free_index = self._find_free_slot()
                if free_index == -1:
                    return added_any
                self.slots[free_index] = {"item": item, "quantity": 1}
                added_any = True
            return added_any

    def remove_item(self, slot_index, quantity=1):
        if slot_index < 0 or slot_index >= self.capacity:
            return False

        slot = self.slots[slot_index]
        if not slot:
            return False

        if slot["quantity"] <= quantity:
            self.slots[slot_index] = None
        else:
            slot["quantity"] -= quantity

        return True

    def _find_free_slot(self):
        for i in range(self.capacity):
            if self.slots[i] is None:
                return i
        return -1

    def is_full(self):
        return all(slot is not None for slot in self.slots)

    def show_backpack(self):
        print("\n======== Backpack ========")
        for idx, slot in enumerate(self.slots):
            if slot:
                item = slot["item"]
                qty = slot["quantity"]
                print(f"Slot {idx+1}: {item.icon} {item.name} x{qty} (Stackable={item.stackable})")
            else:
                print(f"Slot {idx+1}: [leer]")
        print("===========================\n")
