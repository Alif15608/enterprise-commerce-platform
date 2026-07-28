import { useParams } from "react-router-dom";
import { useProduct } from "../hooks/useCatalog";
import AddToCartButton from "../components/cart/AddToCartButton";
import Spinner from "../components/ui/Spinner";

export default function ProductDetail() {
  const { slug } = useParams<{ slug: string }>();
  const { data: product, isLoading, isError } = useProduct(slug!);

  if (isLoading) return <Spinner />;
  if (isError || !product) return <p className="p-8 text-red-600">Product not found.</p>;

  return (
    <div className="mx-auto max-w-4xl p-8">
      <div className="grid grid-cols-2 gap-8">
        <div className="flex flex-col gap-2">
          {product.images?.map((img: any) => (
            <img key={img.id} src={img.image} alt={product.name} className="rounded" />
          ))}
        </div>
        <div>
          <h1 className="text-2xl font-bold">{product.name}</h1>
          <p className="mt-2 text-xl">${product.price}</p>
          <p className={product.is_in_stock ? "text-green-600" : "text-red-500"}>
            {product.is_in_stock ? `${product.stock_quantity} in stock` : "Out of stock"}
          </p>
          <p className="mt-4 text-sm text-gray-600">{product.description}</p>
          <AddToCartButton productId={product.id} disabled={!product.is_in_stock} />
        </div>
      </div>
    </div>
  );
}