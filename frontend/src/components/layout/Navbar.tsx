import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { useCart } from "../../hooks/useCart";
import { useLogout } from "../../hooks/useAuth";

export default function Navbar() {
  const { isAuthenticated, user } = useAuthStore();
  const { data: cart } = useCart();
  const logout = useLogout();

  return (
    <nav className="flex items-center justify-between border-b px-6 py-4">
      <Link to="/" className="text-lg font-bold">
        Enterprise Commerce
      </Link>

      <div className="flex items-center gap-4 text-sm">
        <Link to="/products">Products</Link>

        <Link to="/cart">
          Cart{cart?.item_count ? ` (${cart.item_count})` : ""}
        </Link>

        {isAuthenticated ? (
          <>
            <Link to="/dashboard">
              {user?.first_name || "Account"}
            </Link>

            {user?.roles?.some(
              (r) => r === "admin" || r === "manager"
            ) && <Link to="/admin">Admin</Link>}

            <button onClick={() => logout.mutate()}>
              Logout
            </button>
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