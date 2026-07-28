import { useUpdateCartItem, useRemoveCartItem } from "../../hooks/useCart";

export default function CartItemRow({ item }: { item: any }) {
  const updateItem = useUpdateCartItem();
  const removeItem = useRemoveCartItem();

  return (
    <div className="flex items-center justify-between border-b py-4">
      <div>
        <p className="font-medium">{item.product.name}</p>
        <p className="text-sm text-gray-500">${item.product.price} each</p>
      </div>
      <div className="flex items-center gap-3">
        <input
          type="number"
          min={1}
          value={item.quantity}
          onChange={(e) =>
            updateItem.mutate({ itemId: item.id, quantity: Math.max(1, Number(e.target.value)) })
          }
          className="w-16 rounded border px-2 py-1"
        />
        <span className="w-20 text-right font-medium">${item.line_total}</span>
        <button
          onClick={() => removeItem.mutate(item.id)}
          className="text-sm text-red-500 hover:underline"
        >
          Remove
        </button>
      </div>
    </div>
  );
}