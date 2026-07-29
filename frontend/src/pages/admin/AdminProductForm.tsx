import { useParams } from "react-router-dom";
import { useProduct } from "../../hooks/useCatalog";
import ProductForm from "../../components/admin/ProductForm";
import Spinner from "../../components/ui/Spinner";

export default function AdminProductForm() {
  const { slug } = useParams<{ slug: string }>();
  const { data: product, isLoading } = useProduct(slug || "");

  if (slug && isLoading) return <Spinner />;

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">{slug ? "Edit Product" : "New Product"}</h1>
      <ProductForm existingProduct={slug ? product : undefined} />
    </div>
  );
}