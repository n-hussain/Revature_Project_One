from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CheckoutEvent:
    book_id: str
    checked_out_at: datetime
    returned_at: datetime | None = None
    returned: bool = False
