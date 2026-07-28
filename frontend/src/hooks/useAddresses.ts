import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { addressApi } from "../api/addresses";

export function useAddresses() {
  return useQuery({
    queryKey: ["addresses"],
    queryFn: addressApi.list,
  });
}

export function useCreateAddress() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: addressApi.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["addresses"] }),
  });
}