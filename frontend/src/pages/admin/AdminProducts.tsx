import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useProducts, useCategories } from "../../hooks/useCatalog";

import { useDeleteProduct } from "../../hooks/useAdminProducts";

import apiClient from "../../api/client";

export default function AdminProducts() {
  const { data } = useProducts({});
  const { data: categories } = useCategories();
  const { data: brandsData } = useQuery({
    queryKey: ["brands"],
    queryFn: () => apiClient.get("/catalog/brands/").then((r) => r.data),
  });

  const catName = (id: number) => categories?.find((c: any) => c.id === id)?.name || "—";
  const brandName = (id: number) => brandsData?.results?.find((b: any) => b.id === id)?.name || "—";

  const deleteProduct = useDeleteProduct();

  return (
    <div>
      <div className="mb-4 flex justify-between">
        <h1 className="text-xl font-bold">Products</h1>
        <Link to="/admin/products/new" className="rounded bg-black px-4 py-2 text-sm text-white">
          + New Product
        </Link>
      </div>
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b">
            <th>Name</th><th>Category</th><th>Brand</th><th>Price</th><th>Quantity</th><th></th><th></th>
          </tr>
        </thead>
        <tbody>
          {data?.results.map((p: any) => (
            <tr key={p.id} className="border-b">
              <td className="py-2">{p.name}</td>
              <td>{catName(p.category)}</td>
              <td>{brandName(p.brand)}</td>
              <td>${p.price}</td>
              <td>{p.stock_quantity}</td>
              <td><Link to={`/admin/products/${p.slug}/edit`} className="text-blue-600 underline">Edit</Link></td>
              <td>
                <button
                  onClick={() => confirm(`Delete ${p.name}?`) && deleteProduct.mutate(p.slug)}
                  className="text-sm text-red-500 hover:underline"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}