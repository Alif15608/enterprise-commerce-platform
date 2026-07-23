import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./api/queryClient";
import ErrorBoundary from "./components/ui/ErrorBoundary";
import Toaster from "./components/ui/Toaster";
import Layout from "./components/layout/Layout";
import ProtectedRoute from "./routes/ProtectedRoute";
import AdminRoute from "./routes/AdminRoute";
import NotFound from "./pages/NotFound";

// Placeholder pages — real implementations arrive in 14b/14c/14d.
const Placeholder = ({ label }: { label: string }) => <div className="p-8">{label}</div>;

export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Toaster />
          <Routes>
            <Route element={<Layout />}>
              <Route index element={<Placeholder label="Home (14b)" />} />
              <Route path="products" element={<Placeholder label="Product list (14b)" />} />
              <Route path="login" element={<Placeholder label="Login (14a-auth)" />} />
              <Route path="register" element={<Placeholder label="Register (14a-auth)" />} />

              <Route element={<ProtectedRoute />}>
                <Route path="dashboard" element={<Placeholder label="Dashboard (14b)" />} />
                <Route path="cart" element={<Placeholder label="Cart (14c)" />} />
                <Route path="checkout" element={<Placeholder label="Checkout (14c)" />} />
              </Route>

              <Route element={<AdminRoute />}>
                <Route path="admin/*" element={<Placeholder label="Admin (14d)" />} />
              </Route>

              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}