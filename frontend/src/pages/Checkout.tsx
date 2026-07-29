import { useState } from "react";
import { useCart } from "../hooks/useCart";
import { useCheckout, useValidateCoupon } from "../hooks/useOrders";
import AddressSelector from "../components/checkout/AddressSelector";

export default function Checkout() {
  const { data: cart } = useCart();
  const [addressId, setAddressId] = useState<number | null>(null);
  const [couponCode, setCouponCode] = useState("");
  const [appliedDiscount, setAppliedDiscount] = useState<number | null>(null);
  const checkout = useCheckout();
  const validateCoupon = useValidateCoupon();

  const handleApplyCoupon = () => {
    if (!cart || !couponCode) return;
    validateCoupon.mutate(
      { code: couponCode, subtotal: cart.subtotal },
      { onSuccess: (data) => setAppliedDiscount(data.discount) }
    );
  };

  const handlePlaceOrder = () => {
    if (!addressId) return;
    checkout.mutate({
      shipping_address_id: addressId,
      coupon_code: appliedDiscount !== null ? couponCode : undefined,
    });
  };

  return (
    <div className="mx-auto max-w-lg p-8">
      <h1 className="mb-6 text-2xl font-bold">Checkout</h1>

      <h2 className="mb-2 font-semibold">Shipping Address</h2>
      <AddressSelector onSelect={setAddressId} />

      <h2 className="mb-2 mt-6 font-semibold">Coupon Code</h2>
      <div className="flex gap-2">
        <input
          value={couponCode}
          onChange={(e) => { setCouponCode(e.target.value); setAppliedDiscount(null); }}
          placeholder="Enter coupon code"
          className="flex-1 rounded border px-3 py-2 text-sm"
        />
        <button
          onClick={handleApplyCoupon}
          disabled={!couponCode || validateCoupon.isPending}
          className="rounded border px-4 py-2 text-sm disabled:opacity-50"
        >
          Apply
        </button>
      </div>
      {appliedDiscount !== null && (
        <p className="mt-1 text-sm text-green-600">Coupon applied: -${appliedDiscount}</p>
      )}

      {cart && (
        <div className="mt-6 flex flex-col gap-1 border-t pt-4 text-sm">
          <div className="flex justify-between"><span>Subtotal</span><span>${cart.subtotal}</span></div>
          {appliedDiscount !== null && (
            <div className="flex justify-between text-green-600"><span>Discount</span><span>-${appliedDiscount}</span></div>
          )}
          <p className="mt-1 text-xs text-gray-400">Tax and shipping calculated at checkout</p>
        </div>
      )}

      <button
        disabled={!addressId || checkout.isPending}
        onClick={handlePlaceOrder}
        className="mt-6 w-full rounded bg-black py-3 text-white disabled:opacity-50"
      >
        {checkout.isPending ? "Placing order..." : "Place Order"}
      </button>
    </div>
  );
}