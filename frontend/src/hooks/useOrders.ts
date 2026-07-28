import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { ordersApi } from "../api/orders";

export function useCheckout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ordersApi.checkout,
    onSuccess: (order) => {
      queryClient.invalidateQueries({ queryKey: ["cart"] }); // cart is now converted, Phase 9
      navigate(`/order-confirmation/${order.order_number}`);
    },
    onError: (err: any) =>
      toast.error(err.response?.data?.detail || "Checkout failed."),
  });
}

export function useOrder(orderNumber: string) {
  return useQuery({
    queryKey: ["order", orderNumber],
    queryFn: () => ordersApi.getOrder(orderNumber),
    enabled: !!orderNumber,
  });
}

export function useMyOrders() {
  return useQuery({
    queryKey: ["orders", "mine"],
    queryFn: ordersApi.myOrders,
  });
}