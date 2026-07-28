import { useState } from "react";
import { Link } from "react-router-dom";

interface Category {
  id: number;
  name: string;
  slug: string;
  children: Category[];
}

export default function CategoryNode({ category }: { category: Category }) {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = category.children?.length > 0;

  return (
    <div className="pl-2">
      <div className="flex items-center gap-1">
        {hasChildren && (
          <button onClick={() => setExpanded(!expanded)} className="text-xs text-gray-400">
            {expanded ? "▾" : "▸"}
          </button>
        )}
        <Link to={`/products?category=${category.id}`} className="text-sm hover:underline">
          {category.name}
        </Link>
      </div>
      {expanded && hasChildren && (
        <div className="border-l pl-2">
          {category.children.map((child) => (
            <CategoryNode key={child.id} category={child} />
          ))}
        </div>
      )}
    </div>
  );
}