// pages/dashboard/DashboardOverview.tsx (new)
import { useAuthStore } from "../../store/authStore";
import { useMyOrders } from "../../hooks/useOrders";

export default function DashboardOverview() {
  const user = useAuthStore((s) => s.user);
  const { data: orders } = useMyOrders();
  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Welcome, {user?.first_name || user?.email}</h1>
      <p className="text-sm text-gray-500">You have {orders?.length ?? 0} order(s).</p>
    </div>
  );
}