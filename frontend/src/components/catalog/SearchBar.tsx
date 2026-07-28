import { useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function SearchBar() {
  const [params, setParams] = useSearchParams();
  const [value, setValue] = useState(params.get("search") || "");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const next = new URLSearchParams(params);
    if (value) next.set("search", value); else next.delete("search");
    next.delete("page"); // reset pagination on a new search
    setParams(next);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Search products..."
        className="flex-1 rounded border px-3 py-2"
      />
      <button type="submit" className="rounded bg-black px-4 py-2 text-white">Search</button>
    </form>
  );
}