import { useState } from "react";
import { useCreateProduct, useUpdateProduct, useUploadProductImage } from "../../hooks/useAdminProducts";
import { useCategories } from "../../hooks/useCatalog";

import { useQuery } from "@tanstack/react-query";
import apiClient from "../../api/client";

export default function ProductForm({ existingProduct }: { existingProduct?: any }) {
  const isEdit = !!existingProduct;
  const { data: categories } = useCategories();
  const createProduct = useCreateProduct();
  const updateProduct = useUpdateProduct();
  const uploadImage = useUploadProductImage();

  // Add alongside the categories fetch:
  const { data: brandsData } = useQuery({
    queryKey: ["brands"],
    queryFn: () => apiClient.get("/catalog/brands/").then((r) => r.data),
  });


  const [form, setForm] = useState({
    name: existingProduct?.name || "",
    sku: existingProduct?.sku || "",
    description: existingProduct?.description || "",
    price: existingProduct?.price || "",
    // stock_quantity: existingProduct?.stock_quantity || 0,
    stock_quantity: existingProduct?.stock_quantity || "",
    category: existingProduct?.category?.id || "",
    brand: existingProduct?.brand?.id || existingProduct?.brand || "",
  });
  const [imageFile, setImageFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      updateProduct.mutate({ slug: existingProduct.slug, data: form });
    } else {
      createProduct.mutate(form, {
        onSuccess: (newProduct) => {
          if (imageFile) uploadImage.mutate({ slug: newProduct.slug, file: imageFile });
        },
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex max-w-md flex-col gap-3">
      <input placeholder="Product Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="rounded border px-3 py-2" required />
      <input placeholder="SKU" value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} className="rounded border px-3 py-2" required />
      <textarea placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} className="rounded border px-3 py-2" />
      <input type="number" placeholder="Price" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} className="rounded border px-3 py-2" required />
      <input type="number" placeholder="Stock" value={form.stock_quantity} onChange={(e) => setForm({ ...form, stock_quantity: Number(e.target.value) })} className="rounded border px-3 py-2" />
      <select value={form.category} onChange={(e) => setForm({ ...form, category: Number(e.target.value) })} className="rounded border px-3 py-2" required>
        <option value="">Select category</option>
        {categories?.map((c: any) => <option key={c.id} value={c.id}>{c.name}</option>)}
      </select>
      {/* Add to the JSX, near the category select: */}
      <select value={form.brand} onChange={(e) => setForm({ ...form, brand: e.target.value || null })} className="rounded border px-3 py-2">
        <option value="">Select Brand</option>
        {brandsData?.results?.map((b: any) => <option key={b.id} value={b.id}>{b.name}</option>)}
      </select>

      {!isEdit && (
        <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files?.[0] || null)} />
      )}
      <button type="submit" className="rounded bg-black py-2 text-white">
        {isEdit ? "Save changes" : "Create product"}
      </button>
    </form>
  );
}