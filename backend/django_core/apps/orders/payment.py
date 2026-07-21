from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    message: str = ""


class PaymentGateway(ABC):
    """
    Strategy interface for payment processing. Checkout logic depends only
    on this interface, never on a concrete gateway — new providers (Stripe,
    PayPal) plug in as new subclasses with zero changes to services.py.
    """
    @abstractmethod
    def charge(self, *, order, amount) -> PaymentResult:
        ...


class MockPaymentGateway(PaymentGateway):
    """
    Always succeeds. Placeholder until a real gateway (e.g. Stripe) is
    wired in — deliberately isolated here so that integration is a
    drop-in replacement, not a rewrite of checkout logic.
    """
    def charge(self, *, order, amount) -> PaymentResult:
        return PaymentResult(
            success=True,
            transaction_id=f"mock_txn_{order.order_number}",
            message="Mock payment always succeeds — replace with a real gateway in production.",
        )


def get_payment_gateway() -> PaymentGateway:
    # Single point of control for which gateway implementation is active.
    # Swapping to Stripe later means changing only this function.
    return MockPaymentGateway()