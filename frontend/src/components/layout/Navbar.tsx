import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

export default function Navbar() {
  const { isAuthenticated, user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate("/login");
  };

  return (
    <nav className="flex items-center justify-between border-b px-6 py-4">
      <Link to="/" className="text-lg font-bold">
        Enterprise Commerce
      </Link>
      <div className="flex items-center gap-4 text-sm">
        <Link to="/products">Products</Link>
        <Link to="/cart">Cart</Link>
        {isAuthenticated ? (
          <>
            <Link to="/dashboard">{user?.first_name || "Account"}</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}