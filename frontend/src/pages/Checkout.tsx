import { useState } from "react";
import { useCart } from "../hooks/useCart";
import { useCheckout } from "../hooks/useOrders";
import AddressSelector from "../components/checkout/AddressSelector";

export default function Checkout() {
  const { data: cart } = useCart();
  const [addressId, setAddressId] = useState<number | null>(null);
  const checkout = useCheckout();

  return (
    <div className="mx-auto max-w-lg p-8">
      <h1 className="mb-6 text-2xl font-bold">Checkout</h1>

      <h2 className="mb-2 font-semibold">Shipping Address</h2>
      <AddressSelector onSelect={setAddressId} />

      {cart && (
        <div className="mt-6 border-t pt-4">
          <p className="flex justify-between text-sm"><span>Subtotal</span><span>${cart.subtotal}</span></p>
          <p className="mt-1 text-xs text-gray-400">Tax and shipping calculated at checkout</p>
        </div>
      )}

      <button
        disabled={!addressId || checkout.isPending}
        onClick={() => addressId && checkout.mutate(addressId)}
        className="mt-6 w-full rounded bg-black py-3 text-white disabled:opacity-50"
      >
        {checkout.isPending ? "Placing order..." : "Place Order"}
      </button>
    </div>
  );
}