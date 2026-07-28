import apiClient from "./client";

export const addressApi = {
  list: () => apiClient.get("/accounts/addresses/").then((r) => r.data),
  create: (data: any) => apiClient.post("/accounts/addresses/", data).then((r) => r.data),
};