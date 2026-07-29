import { useParams } from "react-router-dom";
import { useState } from "react";
import toast from "react-hot-toast";
import { useOrder } from "../../hooks/useOrders";
import { useOrderStatusSocket } from "../../hooks/useOrderStatusSocket";
import Spinner from "../../components/ui/Spinner";

export default function OrderDetail() {
  const { orderNumber } = useParams<{ orderNumber: string }>();
  const { data: order, isLoading } = useOrder(orderNumber!);
  const [liveStatus, setLiveStatus] = useState<string | null>(null);

  useOrderStatusSocket((data) => {
    if (data.order_number === orderNumber) {
      setLiveStatus(data.status);
      toast.success(`Order status updated: ${data.status}`);
    }
  });

  if (isLoading) return <Spinner />;
  if (!order) return <p className="p-8">No Order Yet.</p>;

  const displayStatus = liveStatus || order.status;

  return (
    <div className="mx-auto max-w-2xl p-8">
      <h1 className="mb-2 text-xl font-bold">Order #{order.order_number}</h1>
      <p className="mb-6 inline-block rounded bg-gray-100 px-3 py-1 text-sm capitalize">
        {displayStatus}
      </p>
      {order.items.map((item: any) => (
        <div key={item.id} className="flex justify-between border-b py-2 text-sm">
          <span>{item.product_name} × {item.quantity}</span>
          <span>${item.line_total}</span>
        </div>
      ))}
      <div className="mt-3 flex flex-col gap-1 text-sm">
        <div className="flex justify-between"><span>Subtotal : </span><span>${order.subtotal}</span></div>
        <div className="flex justify-between text-gray-500"><span>Tax : </span><span>${order.tax_amount}</span></div>
        <div className="flex justify-between text-gray-500"><span>Shipping Charge : </span><span>${order.shipping_cost}</span></div>
        {Number(order.discount_amount) > 0 && (
          <div className="flex justify-between text-green-600"><span>Discount : </span><span>-${order.discount_amount}</span></div>
        )}
        <div className="mt-1 flex justify-between border-t pt-1 font-semibold">
          <span>Total : </span><span>${order.total}</span>
        </div>
      </div>
    </div>
  );
}