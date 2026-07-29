import { Link, Outlet, useLocation } from "react-router-dom";

const tabs = [
  { path: "", label: "Overview" },
  { path: "orders", label: "Orders" },
  { path: "profile", label: "Profile" },
  { path: "addresses", label: "Addresses" },
  { path: "change-password", label: "Change Password" }
];

export default function DashboardHome() {
  const location = useLocation();

  return (
    <div className="mx-auto flex max-w-4xl gap-8 p-8">
      <aside className="w-40 shrink-0">
        {tabs.map((tab) => (
          <Link
            key={tab.path}
            to={`/dashboard/${tab.path}`}
            className={`block py-2 text-sm ${
              location.pathname === `/dashboard/${tab.path}` ? "font-semibold" : "text-gray-500"
            }`}
          >
            {tab.label}
          </Link>
        ))}
      </aside>
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  );
}