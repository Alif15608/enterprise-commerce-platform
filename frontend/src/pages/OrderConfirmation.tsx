import { useParams, Link } from "react-router-dom";
import { useOrder } from "../hooks/useOrders";
import Spinner from "../components/ui/Spinner";

export default function OrderConfirmation() {
  const { orderNumber } = useParams<{ orderNumber: string }>();
  const { data: order, isLoading } = useOrder(orderNumber!);

  if (isLoading) return <Spinner />;
  if (!order) return <p className="p-8 text-center">Order not found.</p>;

  return (
    <div className="mx-auto max-w-xl p-8 text-center">
      <h1 className="mb-2 text-2xl font-bold">Order Confirmed 🎉</h1>
      <p className="text-gray-500">Order #{order.order_number}</p>

      <div className="mt-6 text-left">
        {order.items.map((item: any) => (
          <div key={item.id} className="flex justify-between border-b py-2 text-sm">
            <span>{item.product_name} × {item.quantity}</span>
            <span>${item.line_total}</span>
          </div>
        ))}

        <div className="mt-3 flex flex-col gap-1 text-sm">
          <div className="flex justify-between"><span>Subtotal</span><span>${order.subtotal}</span></div>
          {Number(order.discount_amount) > 0 && (
            <div className="flex justify-between text-green-600">
              <span>Discount {order.coupon_code ? `(${order.coupon_code})` : ""}</span>
              <span>-${order.discount_amount}</span>
            </div>
          )}
          <div className="flex justify-between text-gray-500"><span>Tax : </span><span>${order.tax_amount}</span></div>
          <div className="flex justify-between text-gray-500"><span>Shipping : </span><span>${order.shipping_cost}</span></div>
          <div className="mt-1 flex justify-between border-t pt-1 text-lg font-semibold">
            <span>Total : </span><span>${order.total}</span>
          </div>
        </div>
      </div>

      <Link to="/dashboard" className="mt-6 inline-block underline">View my orders</Link>
    </div>
  );
}