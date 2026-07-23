import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function ProtectedRoute() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const location = useLocation();

  if (!isAuthenticated) {
    // Preserve the attempted destination so login can redirect back
    // afterward, instead of always dumping the user on the homepage.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}