import apiClient from "./client";

export const adminApi = {
  // Products
  createProduct: (data: any) => apiClient.post("/catalog/products/create/", data).then((r) => r.data),
  updateProduct: (slug: string, data: any) => apiClient.patch(`/catalog/products/${slug}/update/`, data).then((r) => r.data),
  deleteProduct: (slug: string) => apiClient.delete(`/catalog/products/${slug}/delete/`),
  uploadProductImage: (slug: string, file: File) => {
    const formData = new FormData();
    formData.append("image", file);
    return apiClient.post(`/catalog/products/${slug}/images/`, formData).then((r) => r.data);
  },

  // Categories / Brands
  createCategory: (data: any) => apiClient.post("/catalog/categories/create/", data).then((r) => r.data),
  createBrand: (data: any) => apiClient.post("/catalog/brands/create/", data).then((r) => r.data),

  // Orders
  allOrders: () => apiClient.get("/orders/all/").then((r) => r.data),
  updateOrderStatus: (orderNumber: string, status: string) =>
    apiClient.patch(`/orders/${orderNumber}/status/`, { status }).then((r) => r.data),
};