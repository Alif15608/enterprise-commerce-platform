import { useMutation, useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { authApi } from "../api/auth";
import { useAuthStore } from "../store/authStore";
import { getGuestToken, clearGuestToken } from "./useGuestToken";
import apiClient from "../api/client";

export function useRegister() {
  return useMutation({
    mutationFn: authApi.register,
    onSuccess: () => toast.success("Check your email to verify your account."),
    onError: (err: any) =>
      toast.error(err.response?.data?.email?.[0] || "Registration failed."),
  });
}

export function useVerifyEmail() {
  return useMutation({
    mutationFn: authApi.verifyEmail,
    onError: (err: any) => toast.error(err.response?.data?.detail || "Invalid link."),
  });
}

export function useLogin() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);

  return useMutation({
    mutationFn: authApi.login,
    onSuccess: async (tokens) => {
      localStorage.setItem("refresh_token", tokens.refresh);
      // Set the access token first so the /me/ call below is authenticated.
      useAuthStore.getState().setAccessToken(tokens.access);

      const user = await authApi.me();
      setAuth(user, tokens.access);

      // Merge any guest cart into the now-authenticated user's cart —
      // this is the Phase 8 merge flow, triggered explicitly here per
      // the Phase 8 architecture decision (accounts stays unaware of cart).
      const guestToken = getGuestToken();
      if (guestToken) {
        try {
          await apiClient.post("/cart/merge/", null, {
            headers: { "X-Guest-Token": guestToken },
          });
          clearGuestToken();
        } catch {
          // Non-fatal — user still logs in successfully even if merge fails.
        }
      }

      toast.success("Welcome back!");
      navigate("/dashboard");
    },
    onError: () => toast.error("Invalid email or password."),
  });
}

export function useLogout() {
  const navigate = useNavigate();
  const clearAuth = useAuthStore((s) => s.clearAuth);

  return useMutation({
    mutationFn: async () => {
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) await authApi.logout(refresh);
    },
    onSettled: () => {
      // Clear local state regardless of whether the server call succeeded —
      // a failed logout call shouldn't leave the user stuck "logged in" locally.
      clearAuth();
      navigate("/login");
    },
  });
}

export function useMe() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  return useQuery({
    queryKey: ["me"],
    queryFn: authApi.me,
    enabled: isAuthenticated,
  });
}

export function useRequestPasswordReset() {
  return useMutation({
    mutationFn: authApi.requestPasswordReset,
    onSuccess: () => toast.success("If that email is registered, a reset link has been sent."),
  });
}

export function useConfirmPasswordReset() {
  return useMutation({
    mutationFn: authApi.confirmPasswordReset,
    onError: (err: any) => toast.error(err.response?.data?.detail || "Reset failed."),
  });
}