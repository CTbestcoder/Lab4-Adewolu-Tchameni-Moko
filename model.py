from unittest.mock import DEFAULT

from constants import TABLES, MENU_ITEMS
from enum import Enum

class Orderstate(Enum):
    DEFAULT_STATE = 1
    PLACED = 2
    COOKING = 3
    READY = 4
    SERVED = 5


class Restaurant:

    def __init__(self):
        super().__init__()
        self.tables = [Table(seats, loc) for seats, loc in TABLES]
        self.menu_items = [MenuItem(name, price) for name, price in MENU_ITEMS]
        self.views = []

    def add_view(self, view):
        self.views.append(view)

    def notify_views(self):
        for view in self.views:
            view.update()


class Table:

    def __init__(self, seats, location):
        self.n_seats = seats
        self.location = location
        self.orders = [Order() for _ in range(seats)]

    def has_any_active_orders(self):
        for order in self.orders:
            for item in order.items:
                if item.has_been_ordered() and not item.has_been_served():
                    return True
        return False

    def has_order_for(self, seat):
        return bool(self.orders[seat].items)

    def order_for(self, seat):
        return self.orders[seat]


class Order:

    def __init__(self):
        self.items = []

    def add_item(self, menu_item):
        item = OrderItem(menu_item)
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def place_new_orders(self):
        for item in self.unordered_items():
            item.mark_as_ordered()

    def remove_unordered_items(self):
        for item in self.unordered_items():
            self.items.remove(item)

    def unordered_items(self):
        return [item for item in self.items if not item.has_been_ordered()]

    def total_cost(self):
        return sum((item.details.price for item in self.items))


    def change_state(self,item):
        print(f"Before change: {item.current_state()}")
        if item.has_been_ordered() and item.current_state() == Orderstate.PLACED:
            item.mark_as_cooking()
        elif item.is_cooking():
            item.mark_as_ready()
        elif item.is_ready():
            item.mark_as_served()
        print(f"After change: {item.current_state()}")





class OrderItem:

    # TODO: need to represent item state, not just ordered
    def __init__(self, menu_item):
        self.details = menu_item
        self.__ordered = Orderstate.DEFAULT_STATE
        

    def mark_as_ordered(self):
        self.__ordered = Orderstate.PLACED

    def mark_as_cooking(self):
        self.__ordered = Orderstate.COOKING

    def mark_as_ready(self):
        self.__ordered = Orderstate.READY

    def mark_as_served(self):
        self.__ordered = Orderstate.SERVED


    def has_been_ordered(self):
            return self.__ordered in (
                Orderstate.PLACED,
                Orderstate.COOKING,
                Orderstate.READY,
                Orderstate.SERVED,
            )

    def is_cooking(self):
        return self.__ordered == Orderstate.COOKING

    def is_ready(self):
        return self.__ordered == Orderstate.READY



    def has_been_served(self):
        return self.__ordered == Orderstate.SERVED


    def current_state(self):
        return self.__ordered




    def can_be_cancelled(self):
        return self.__ordered == Orderstate.PLACED or self.__ordered == Orderstate.DEFAULT_STATE

        # TODO: correct implementation based on item state


class MenuItem:

    def __init__(self, name, price):
        self.name = name
        self.price = price
