import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { adminApi } from "../api/admin";

export function useAllOrders() {
  return useQuery({ queryKey: ["admin", "orders"], queryFn: adminApi.allOrders });
}

export function useUpdateOrderStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ orderNumber, status }: { orderNumber: string; status: string }) =>
      adminApi.updateOrderStatus(orderNumber, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "orders"] });
      toast.success("Order status updated.");
    },
  });
}