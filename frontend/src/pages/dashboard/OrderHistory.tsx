import { Link } from "react-router-dom";
import { useMyOrders } from "../../hooks/useOrders";
import Spinner from "../../components/ui/Spinner";

export default function OrderHistory() {
  const { data: orders, isLoading } = useMyOrders();

  if (isLoading) return <Spinner />;

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Order History</h1>
      {orders?.length === 0 && <p className="text-gray-500">No orders yet.</p>}
      {/* {orders?.map((order: any) => (
        <Link
          key={order.id}
          to={`/dashboard/orders/${order.order_number}`}
          className="flex justify-between border-b py-3 text-sm hover:bg-gray-50"
        >
          <span>#{order.order_number}</span>
          <span className="capitalize">{order.status}</span>
          <span>${order.total}</span>
        </Link>
      ))} */}
      {orders?.map((order: any) => {
        const summary = order.items.map((i: any) => i.product_name).join(", ");
        return (
          <Link 
            key={order.id} 
            to={`/dashboard/orders/${order.order_number}`} 
            className="block border-b py-3 text-sm hover:bg-gray-50"
          >
            {summary}
          </Link>
        );
      })}
    </div>
  );
}