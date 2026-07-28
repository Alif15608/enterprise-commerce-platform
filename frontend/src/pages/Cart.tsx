import { Link } from "react-router-dom";
import { useCart } from "../hooks/useCart";
import CartItemRow from "../components/cart/CartItemRow";
import Spinner from "../components/ui/Spinner";

export default function Cart() {
  const { data: cart, isLoading } = useCart();

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
      <div className="mt-6 flex items-center justify-between">
        <span className="text-lg font-semibold">Subtotal: ${cart.subtotal}</span>
        <Link to="/checkout" className="rounded bg-black px-6 py-3 text-white">
          Proceed to Checkout
        </Link>
      </div>
    </div>
  );
}