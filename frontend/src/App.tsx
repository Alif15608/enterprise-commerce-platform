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

import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import OrderConfirmation from "./pages/OrderConfirmation";

import DashboardHome from "./pages/dashboard/DashboardHome";
import OrderHistory from "./pages/dashboard/OrderHistory";
import OrderDetail from "./pages/dashboard/OrderDetail";
import Profile from "./pages/dashboard/Profile";
import Addresses from "./pages/dashboard/Addresses";
import AdminLayout from "./pages/admin/AdminLayout";
import AdminProducts from "./pages/admin/AdminProducts";
import AdminProductForm from "./pages/admin/AdminProductForm";
import AdminCategories from "./pages/admin/AdminCategories";
import AdminBrands from "./pages/admin/AdminBrands";
import AdminOrders from "./pages/admin/AdminOrders";
import AdminInventory from "./pages/admin/AdminInventory";

import ChangePassword from "./pages/dashboard/ChangePassword";
import DashboardOverview from "./pages/dashboard/DashboardOverview";

// Placeholder pages — real implementations arrive in 14b/14c/14d.
//const Placeholder = ({ label }: { label: string }) => <div className="p-8">{label}</div>;

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

              <Route path="cart" element={<Cart />} />

              {/* Protected Routes */}
              <Route element={<ProtectedRoute />}>
                <Route path="dashboard" element={<DashboardHome />}>
                <Route path="change-password" element={<ChangePassword />} />
                <Route index element={<OrderHistory />} />
                <Route index element={<DashboardOverview />} />
                <Route path="orders" element={<OrderHistory />} />
                <Route path="orders/:orderNumber" element={<OrderDetail />} />
                <Route path="profile" element={<Profile />} />
                <Route path="addresses" element={<Addresses />} />
              </Route>
                <Route path="checkout" element={<Checkout />} />
                <Route path="order-confirmation/:orderNumber" element={<OrderConfirmation />} />
              </Route>

              {/* Admin Routes */}
              <Route element={<AdminRoute />}>
                <Route path="admin" element={<AdminLayout />}>
                  <Route path="products" element={<AdminProducts />} />
                  <Route path="products/new" element={<AdminProductForm />} />
                  <Route path="products/:slug/edit" element={<AdminProductForm />} />
                  <Route path="categories" element={<AdminCategories />} />
                  <Route path="brands" element={<AdminBrands />} />
                  <Route path="orders" element={<AdminOrders />} />
                  <Route path="inventory" element={<AdminInventory />} />
                </Route>
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