import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

// Placeholder until Phase 14b's /accounts/me/ response includes roles —
// tracked explicitly so this isn't silently forgotten.
// TODO(14b): replace with real role check once roles are exposed on User.
export default function AdminRoute() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}