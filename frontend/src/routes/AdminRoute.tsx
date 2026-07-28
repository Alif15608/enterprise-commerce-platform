import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

// Placeholder until Phase 14b's /accounts/me/ response includes roles —
// tracked explicitly so this isn't silently forgotten.
// TODO(14b): replace with real role check once roles are exposed on User.
export default function AdminRoute() {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const isAdminOrManager = user?.roles.some((r) => r === "admin" || r === "manager");
  if (!isAdminOrManager) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}