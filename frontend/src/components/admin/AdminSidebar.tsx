import { NavLink } from "react-router-dom";

const links = [
  { to: "/admin/products", label: "Products" },
  { to: "/admin/categories", label: "Categories" },
  { to: "/admin/brands", label: "Brands" },
  { to: "/admin/orders", label: "Orders" },
  { to: "/admin/inventory", label: "Inventory" },
  { to: "/admin/coupons", label: "Coupons"  },
];

export default function AdminSidebar() {
  return (
    <aside className="w-48 shrink-0 border-r p-4">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `block py-2 text-sm ${isActive ? "font-semibold" : "text-gray-500"}`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
}