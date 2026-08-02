import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { adminApi } from "../api/admin";

export function useCreateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: adminApi.createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("Product created.");
    },
    onError: (err: any) => toast.error(err.response?.data?.detail || "Failed to create product."),
  });
}

export function useUpdateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ slug, data }: { slug: string; data: any }) => adminApi.updateProduct(slug, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      queryClient.invalidateQueries({ queryKey: ["product", variables.slug] });
      toast.success("Product updated.");
    },
  });
}

export function useUploadProductImage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ slug, file }: { slug: string; file: File }) => adminApi.uploadProductImage(slug, file),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["product", variables.slug] });
      toast.success("Image uploaded.");
    },
  });
}

export function useCreateCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: adminApi.createCategory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
      toast.success("Category created.");
    },
  });
}

export function useCreateBrand() {
  return useMutation({
    mutationFn: adminApi.createBrand,
    onSuccess: () => toast.success("Brand created."),
  });
}

// frontend/src/hooks/useAdminProducts.ts — add
export function useDeleteProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (slug: string) => adminApi.deleteProduct(slug),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("Product deleted.");
    },
  });
}