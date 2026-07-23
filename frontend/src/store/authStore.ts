import { create } from "zustand";
import type { User } from "../types/auth";

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, accessToken: string) => void;
  setAccessToken: (accessToken: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  isAuthenticated: false,

  setAuth: (user, accessToken) =>
    set({ user, accessToken, isAuthenticated: true }),

  setAccessToken: (accessToken) => set({ accessToken }),

  clearAuth: () => {
    localStorage.removeItem("refresh_token");
    set({ user: null, accessToken: null, isAuthenticated: false });
  },
}));