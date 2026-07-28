import { useState } from "react";
import { useAddToCart } from "../../hooks/useCart";

export default function AddToCartButton({ productId, disabled }: { productId: number; disabled?: boolean }) {
  const [quantity, setQuantity] = useState(1);
  const addToCart = useAddToCart();

  return (
    <div className="mt-4 flex items-center gap-3">
      <input
        type="number"
        min={1}
        value={quantity}
        onChange={(e) => setQuantity(Math.max(1, Number(e.target.value)))}
        className="w-16 rounded border px-2 py-1"
      />
      <button
        disabled={disabled || addToCart.isPending}
        onClick={() => addToCart.mutate({ productId, quantity })}
        className="rounded bg-black px-6 py-2 text-white disabled:opacity-50"
      >
        {addToCart.isPending ? "Adding..." : "Add to Cart"}
      </button>
    </div>
  );
}