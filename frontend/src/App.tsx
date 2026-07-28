import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./api/queryClient";
import ErrorBoundary from "./components/ui/ErrorBoundary";
import Toaster from "./components/ui/Toaster";
import Layout from "./components/layout/Layout";
import ProtectedRoute from "./routes/ProtectedRoute";
import AdminRoute from "./routes/AdminRoute";
import NotFound from "./pages/NotFound";

import Login from "./pages/Login";
import Register from "./pages/Register";
import VerifyEmail from "./pages/VerifyEmail";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Home from "./pages/Home";
import ProductList from "./pages/ProductList";
import ProductDetail from "./pages/ProductDetail";

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

              {/* Public Routes */}
              <Route index element={<Home />} />
              <Route path="products" element={<ProductList />} />
              <Route path="products/:slug" element={<ProductDetail />} />

              <Route path="login" element={<Login />} />
              <Route path="register" element={<Register />} />
              <Route path="verify-email" element={<VerifyEmail />} />
              <Route path="forgot-password" element={<ForgotPassword />} />
              <Route path="reset-password" element={<ResetPassword />} />

              {/* Protected Routes */}
              <Route element={<ProtectedRoute />}>
                <Route path="dashboard" element={<Placeholder label="Dashboard (14b)" />} />
                <Route path="cart" element={<Placeholder label="Cart (14c)" />} />
                <Route path="checkout" element={<Placeholder label="Checkout (14c)" />} />
              </Route>

              {/* Admin Routes */}
              <Route element={<AdminRoute />}>
                <Route path="admin/*" element={<Placeholder label="Admin (14d)" />} />
              </Route>

              {/* 404 */}
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}