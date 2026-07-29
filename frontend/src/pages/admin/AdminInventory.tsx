import { useQuery } from "@tanstack/react-query";
import { useProducts, useCategories } from "../../hooks/useCatalog";
import apiClient from "../../api/client";

export default function AdminInventory() {
  const { data } = useProducts({});
  const { data: categories } = useCategories();
  const { data: brandsData } = useQuery({
    queryKey: ["brands"],
    queryFn: () => apiClient.get("/catalog/brands/").then((r) => r.data),
  });

  const catName = (id: number) => categories?.find((c: any) => c.id === id)?.name || "—";
  const brandName = (id: number) => brandsData?.results?.find((b: any) => b.id === id)?.name || "—";

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Inventory</h1>
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b">
            <th>Product</th><th>SKU</th><th>Category</th><th>Brand</th><th>Unit Price</th><th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {data?.results.map((p: any) => (
            <tr key={p.id} className={`border-b ${p.stock_quantity < 5 ? "bg-red-50" : ""}`}>
              <td className="py-2">{p.name}</td>
              <td>{p.sku}</td>
              <td>{catName(p.category)}</td>
              <td>{brandName(p.brand)}</td>
              <td>${p.price}</td>
              <td>{p.stock_quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}