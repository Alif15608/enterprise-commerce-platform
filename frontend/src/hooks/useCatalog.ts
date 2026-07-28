import { useQuery } from "@tanstack/react-query";
import { catalogApi, type ProductFilters } from "../api/catalog";

export function useProducts(filters: ProductFilters) {
  return useQuery({
    // Filters embedded in the query key — a change in any filter value
    // (which lives in the URL, per Decision 3) automatically triggers a
    // refetch and a distinctly cached entry for that exact filter combo.
    queryKey: ["products", filters],
    queryFn: () => catalogApi.listProducts(filters),
    placeholderData: (previousData) => previousData, // avoid layout flash while paginating
  });
}

export function useProduct(slug: string) {
  return useQuery({
    queryKey: ["product", slug],
    queryFn: () => catalogApi.getProduct(slug),
    enabled: !!slug,
  });
}

export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: catalogApi.getCategories,
    staleTime: 5 * 60 * 1000, // categories change rarely — cache longer than the 1min default
  });
}

export function usePopularProducts() {
  return useQuery({
    queryKey: ["products", "popular"],
    queryFn: catalogApi.getPopularProducts,
  });
}