import { useSearchParams } from "react-router-dom";

export default function Filters() {
  const [params, setParams] = useSearchParams();

  const updateParam = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value); else next.delete(key);
    next.delete("page");
    setParams(next);
  };

  return (
    <div className="flex flex-wrap items-center gap-3 border-b pb-4 text-sm">
      <input
        type="number" placeholder="Min price"
        defaultValue={params.get("min_price") || ""}
        onBlur={(e) => updateParam("min_price", e.target.value)}
        className="w-24 rounded border px-2 py-1"
      />
      <input
        type="number" placeholder="Max price"
        defaultValue={params.get("max_price") || ""}
        onBlur={(e) => updateParam("max_price", e.target.value)}
        className="w-24 rounded border px-2 py-1"
      />
      <select
        defaultValue={params.get("ordering") || ""}
        onChange={(e) => updateParam("ordering", e.target.value)}
        className="rounded border px-2 py-1"
      >
        <option value="">Sort by</option>
        <option value="-created_at">Newest</option>
        <option value="price">Price: Low to High</option>
        <option value="-price">Price: High to Low</option>
      </select>
    </div>
  );
}