from dataclasses import dataclass, field
from typing import List


@dataclass
class ShopItem:
    item_name: str
    item_image_url: str
    item_naver_category: str = field(default_factory=str)
    item_taobao_item_url: str = field(default_factory=str)
    item_taobao_image_url: str = field(default_factory=str)
    item_recommended_keywords: List[str] = field(default_factory=list)
    item_main_keywords: str = field(default_factory=str)
    item_sub_keywords: List[str] = field(default_factory=list)
