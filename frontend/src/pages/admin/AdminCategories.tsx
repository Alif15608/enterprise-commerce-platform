// AdminCategories.tsx
import { useState } from "react";
import { useCategories } from "../../hooks/useCatalog";
import { useCreateCategory } from "../../hooks/useAdminProducts";

export default function AdminCategories() {
  const { data: categories } = useCategories();
  const createCategory = useCreateCategory();
  const [name, setName] = useState("");

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Categories</h1>
      <ul className="mb-4 text-sm">
        {categories?.map((c: any) => <li key={c.id}>{c.name}</li>)}
      </ul>
      <form
        onSubmit={(e) => { e.preventDefault(); createCategory.mutate({ name }); setName(""); }}
        className="flex gap-2"
      >
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Category name" className="rounded border px-3 py-2 text-sm" />
        <button type="submit" className="rounded bg-black px-4 py-2 text-sm text-white">Add</button>
      </form>
    </div>
  );
}