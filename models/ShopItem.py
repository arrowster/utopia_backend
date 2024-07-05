from dataclasses import dataclass, field
from typing import List


@dataclass
class ShopItem:
    item_name: str
    image_url: str
    naver_category: str = field(default_factory="")
    taobao_item_url: str = field(default_factory="")
    main_keywords: List[str] = field(default_factory=list)
    sub_keywords: List[str] = field(default_factory=list)
