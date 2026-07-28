import { useCategories } from "../../hooks/useCatalog";
import CategoryNode from "./CategoryNode";
import Spinner from "../ui/Spinner";

export default function CategorySidebar() {
  const { data: categories, isLoading } = useCategories();

  if (isLoading) return <Spinner />;

  return (
    <aside className="w-56 shrink-0 border-r p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">Categories</h2>
      {categories?.map((cat: any) => (
        <CategoryNode key={cat.id} category={cat} />
      ))}
    </aside>
  );
}