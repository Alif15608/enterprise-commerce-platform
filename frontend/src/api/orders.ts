import apiClient from "./client";

export const ordersApi = {
  checkout: (data: { shipping_address_id: number; coupon_code?: string }) =>
    apiClient.post("/orders/checkout/", data).then((r) => r.data),

  validateCoupon: (code: string, subtotal: number) =>
    apiClient.post("/orders/coupons/validate/", { code, subtotal }).then((r) => r.data),

  getOrder: (orderNumber: string) =>
    apiClient.get(`/orders/${orderNumber}/`).then((r) => r.data),

  myOrders: () => apiClient.get("/orders/my-orders/").then((r) => r.data),
};