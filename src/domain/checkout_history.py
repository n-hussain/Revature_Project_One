from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class CheckoutEvent:
    book_id: str
    checkout_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    returned: bool = False
