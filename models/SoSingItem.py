from dataclasses import dataclass


@dataclass
class SoSingItem:
    item_name: str
    item_price: str
    item_image_url: str
    item_link_url: str
    item_buy_num: str

    def __eq__(self, other):
        return (
            isinstance(other, SoSingItem) and
            self.item_name == other.item_name and
            self.item_price == other.item_price
        )

    def __hash__(self):
        return hash((self.item_name, self.item_price))
