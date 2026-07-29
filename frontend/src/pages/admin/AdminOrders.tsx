import { useAllOrders, useUpdateOrderStatus } from "../../hooks/useAdminOrders";

const STATUSES = ["pending", "paid", "shipped", "delivered", "cancelled"];

export default function AdminOrders() {
  const { data: orders } = useAllOrders();
  const updateStatus = useUpdateOrderStatus();

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">All Orders</h1>
      <table className="w-full text-left text-sm">
        <thead><tr className="border-b"><th>Order #</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
        <tbody>
          {orders?.map((order: any) => (
            <tr key={order.id} className="border-b">
              <td className="py-2">{order.order_number}</td>
              <td>{order.customer_email}</td>
              {/* <td>{order.user?.email}</td> */}
              <td>${order.total}</td>
              <td>
                <select
                  value={order.status}
                  onChange={(e) =>
                    updateStatus.mutate({ orderNumber: order.order_number, status: e.target.value })
                  }
                  className="rounded border px-2 py-1"
                >
                  {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}