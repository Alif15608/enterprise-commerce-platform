import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import apiClient from "../../api/client";
import { useCreateBrand } from "../../hooks/useAdminProducts";

function useBrands() {
  return useQuery({
    queryKey: ["brands"],
    queryFn: () => apiClient.get("/catalog/brands/").then((r) => r.data),
  });
}

export default function AdminBrands() {
  const { data: brands } = useBrands();
  const createBrand = useCreateBrand();
  const [name, setName] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createBrand.mutate({ name });
    setName("");
  };

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Brands</h1>
      <ul className="mb-4 text-sm">
        {brands?.results?.map((b: any) => (
          <li key={b.id} className="border-b py-1">{b.name}</li>
        ))}
      </ul>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Brand name"
          className="rounded border px-3 py-2 text-sm"
          required
        />
        <button type="submit" className="rounded bg-black px-4 py-2 text-sm text-white">
          Add
        </button>
      </form>
    </div>
  );
}