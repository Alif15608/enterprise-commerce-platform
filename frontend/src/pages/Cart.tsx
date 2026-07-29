import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useCart } from "../hooks/useCart";
import apiClient from "../api/client";
import CartItemRow from "../components/cart/CartItemRow";
import Spinner from "../components/ui/Spinner";

export default function Cart() {
  const { data: cart, isLoading } = useCart();

  const { data: estimate } = useQuery({
    queryKey: ["order-estimate", cart?.subtotal],
    queryFn: () =>
      apiClient
        .get("/orders/estimate/", { params: { subtotal: cart?.subtotal } })
        .then((r) => r.data),
    enabled: !!cart?.subtotal,
  });

  if (isLoading) return <Spinner />;

  if (!cart || cart.items.length === 0) {
    return (
      <div className="mx-auto max-w-lg py-24 text-center">
        <p className="text-gray-500">Your cart is empty.</p>
        <Link to="/products" className="mt-4 inline-block underline">Browse products</Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl p-8">
      <h1 className="mb-6 text-2xl font-bold">Your Cart</h1>
      {cart.items.map((item: any) => (
        <CartItemRow key={item.id} item={item} />
      ))}
      <div className="mt-6 flex flex-col gap-1 text-sm">
        <div className="flex justify-between"><span>Subtotal</span><span>${cart.subtotal}</span></div>
        {estimate && (
          <>
            <div className="flex justify-between text-gray-500"><span>Tax (estimated)</span><span>${estimate.tax}</span></div>
            <div className="flex justify-between text-gray-500"><span>Shipping (estimated)</span><span>${estimate.shipping}</span></div>
            <div className="flex justify-between text-lg font-semibold"><span>Estimated Total</span><span>${estimate.total}</span></div>
          </>
        )}
      </div>
      <div className="mt-6 flex justify-end">
        <Link to="/checkout" className="rounded bg-black px-6 py-3 text-white">
          Proceed to Checkout
        </Link>
      </div>
    </div>
  );
}