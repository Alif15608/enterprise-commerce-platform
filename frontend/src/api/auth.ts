import apiClient from "./client";
import type { User, AuthTokens } from "../types/auth";

export const authApi = {
  register: (data: { email: string; password: string; first_name?: string; last_name?: string }) =>
    apiClient.post("/accounts/register/", data),

  verifyEmail: (data: { uid: string; token: string }) =>
    apiClient.post("/accounts/verify-email/", data),

  login: (data: { email: string; password: string }) =>
    apiClient.post<AuthTokens>("/accounts/login/", data).then((r) => r.data),

  logout: (refresh: string) => apiClient.post("/accounts/logout/", { refresh }),

  me: () => apiClient.get<User>("/accounts/me/").then((r) => r.data),

  requestPasswordReset: (email: string) =>
    apiClient.post("/accounts/password-reset/", { email }),

  confirmPasswordReset: (data: { uid: string; token: string; new_password: string }) =>
    apiClient.post("/accounts/password-reset/confirm/", data),

  changePassword: (data: { old_password: string; new_password: string }) =>
    apiClient.post("/accounts/change-password/", data),
};