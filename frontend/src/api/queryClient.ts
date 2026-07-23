import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,        // 1 minute — matches the general "freshness" feel of a storefront
      retry: 1,                     // don't hammer a genuinely broken endpoint
      refetchOnWindowFocus: false,  // avoid surprise refetches interrupting a checkout flow
    },
  },
});