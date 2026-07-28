import { useSearchParams } from "react-router-dom";
import { useProducts } from "../hooks/useCatalog";
import CategorySidebar from "../components/catalog/CategorySidebar";
import SearchBar from "../components/catalog/SearchBar";
import Filters from "../components/catalog/Filters";
import ProductCard from "../components/catalog/ProductCard";
import Pagination from "../components/catalog/Pagination";
import Spinner from "../components/ui/Spinner";

export default function ProductList() {
  const [params] = useSearchParams();
  const filters = Object.fromEntries(params.entries());
  const { data, isLoading, isError } = useProducts(filters);

  return (
    <div className="flex">
      <CategorySidebar />
      <div className="flex-1 p-6">
        <div className="mb-4 flex flex-col gap-4">
          <SearchBar />
          <Filters />
        </div>

        {isLoading && <Spinner />}
        {isError && <p className="text-red-600">Failed to load products.</p>}

        {data && (
          <>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
              {data.results.map((product: any) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
            <Pagination hasNext={!!data.next} hasPrevious={!!data.previous} />
          </>
        )}
      </div>
    </div>
  );
}