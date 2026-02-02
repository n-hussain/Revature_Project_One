from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class CheckoutAction(Enum):
    CHECK_OUT = "check_out"
    CHECK_IN = "check_in"

@dataclass(frozen=True)
class CheckoutEvent:
    book_id: str
    action: CheckoutAction
    timestamp: datetime
