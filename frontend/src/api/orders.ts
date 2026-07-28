import apiClient from "./client";

export const ordersApi = {
  checkout: (shipping_address_id: number) =>
    apiClient.post("/orders/checkout/", { shipping_address_id }).then((r) => r.data),

  getOrder: (orderNumber: string) =>
    apiClient.get(`/orders/${orderNumber}/`).then((r) => r.data),

  myOrders: () => apiClient.get("/orders/my-orders/").then((r) => r.data),
};