import { Link } from "react-router-dom";

export default function ProductCard({ product }: { product: any }) {
  return (
    <Link
      to={`/products/${product.slug}`}
      className="flex flex-col rounded border p-3 transition hover:shadow-md"
    >
      {product.primary_image ? (
        <img src={product.primary_image.image} alt={product.name} className="mb-2 h-40 w-full object-cover" />
      ) : (
        <div className="mb-2 h-40 w-full bg-gray-100" />
      )}
      <span className="text-sm font-medium">{product.name}</span>
      <span className="text-sm text-gray-500">${product.price}</span>
      {!product.is_in_stock && <span className="text-xs text-red-500">Out of stock</span>}
    </Link>
  );
}