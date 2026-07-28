import apiClient from "./client";

export interface ProductFilters {
  search?: string;
  category?: string;
  min_price?: string;
  max_price?: string;
  ordering?: string;
  page?: string;
}

export const catalogApi = {
  listProducts: (filters: ProductFilters) =>
    apiClient.get("/catalog/products/", { params: filters }).then((r) => r.data),

  getProduct: (slug: string) =>
    apiClient.get(`/catalog/products/${slug}/`).then((r) => r.data),

  getCategories: () =>
    apiClient.get("/catalog/categories/").then((r) => r.data),

  getPopularProducts: () =>
    apiClient.get("/catalog/products/popular/").then((r) => r.data),
};