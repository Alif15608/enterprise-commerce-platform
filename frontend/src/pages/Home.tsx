import { usePopularProducts } from "../hooks/useCatalog";
import ProductCard from "../components/catalog/ProductCard";
import Spinner from "../components/ui/Spinner";

export default function Home() {
  const { data: popular, isLoading } = usePopularProducts();

  return (
    <div className="p-8">
      <h1 className="mb-6 text-3xl font-bold">Welcome to Enterprise Commerce</h1>
      <h2 className="mb-4 text-lg font-semibold">Popular right now</h2>
      {isLoading ? (
        <Spinner />
      ) : (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {popular?.map((product: any) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}