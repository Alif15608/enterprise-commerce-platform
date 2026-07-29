import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { ordersApi } from "../api/orders";

export function useCheckout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { shipping_address_id: number; coupon_code?: string }) => ordersApi.checkout(data),
    onSuccess: (order) => {
      queryClient.invalidateQueries({ queryKey: ["cart"] });
      navigate(`/order-confirmation/${order.order_number}`);
    },
    onError: (err: any) => toast.error(err.response?.data?.detail || "Checkout failed."),
  });
}

export function useValidateCoupon() {
  return useMutation({
    mutationFn: ({ code, subtotal }: { code: string; subtotal: number }) =>
      ordersApi.validateCoupon(code, subtotal),
    onError: (err: any) => toast.error(err.response?.data?.detail || "Invalid coupon."),
  });
}

export function useOrder(orderNumber: string) {
  return useQuery({ queryKey: ["order", orderNumber], queryFn: () => ordersApi.getOrder(orderNumber), enabled: !!orderNumber });
}

export function useMyOrders() {
  return useQuery({ queryKey: ["orders", "mine"], queryFn: ordersApi.myOrders });
}