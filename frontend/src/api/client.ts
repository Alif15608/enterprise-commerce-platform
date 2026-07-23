import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "../store/authStore";
import { getGuestToken, setGuestToken } from "../hooks/useGuestToken";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// --- Request interceptor: attach access token OR guest token ---
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const { accessToken } = useAuthStore.getState();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  } else {
    const guestToken = getGuestToken();
    if (guestToken) {
      config.headers["X-Guest-Token"] = guestToken;
    }
  }
  return config;
});

// --- Response interceptor: capture a freshly-issued guest token, and
//     silently refresh an expired access token on 401 ---
let isRefreshing = false;
let refreshQueue: Array<(token: string) => void> = [];

apiClient.interceptors.response.use(
  (response) => {
    // Cart endpoints (Phase 8) return session_token in the body the
    // first time a guest cart is created — persist it automatically.
    const token = response.data?.session_token;
    if (token) setGuestToken(token);
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      // A refresh is already in flight (e.g. two parallel requests both
      // hit 401 at once) — queue this request rather than triggering a
      // second, redundant refresh call.
      return new Promise((resolve) => {
        refreshQueue.push((newToken: string) => {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          resolve(apiClient(originalRequest));
        });
      });
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) throw new Error("No refresh token available");

      const { data } = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/accounts/token/refresh/`,
        { refresh: refreshToken }
      );

      useAuthStore.getState().setAccessToken(data.access);
      if (data.refresh) localStorage.setItem("refresh_token", data.refresh); // ROTATE_REFRESH_TOKENS is on (Phase 5)

      refreshQueue.forEach((cb) => cb(data.access));
      refreshQueue = [];

      originalRequest.headers.Authorization = `Bearer ${data.access}`;
      return apiClient(originalRequest);
    } catch (refreshError) {
      useAuthStore.getState().clearAuth();
      window.location.href = "/login";
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default apiClient;