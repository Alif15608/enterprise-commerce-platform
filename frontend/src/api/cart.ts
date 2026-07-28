import apiClient from "./client";

export const cartApi = {
  getCart: () => apiClient.get("/cart/").then((r) => r.data),

  addItem: (product_id: number, quantity: number) =>
    apiClient.post("/cart/items/", { product_id, quantity }).then((r) => r.data),

  updateItem: (itemId: number, quantity: number) =>
    apiClient.patch(`/cart/items/${itemId}/`, { quantity }).then((r) => r.data),

  removeItem: (itemId: number) =>
    apiClient.delete(`/cart/items/${itemId}/remove/`),
};