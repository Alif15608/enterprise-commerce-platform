import { useQuery } from "@tanstack/react-query";
import { useSearchParams, Link } from "react-router-dom";
import apiClient from "../api/client";

export default function VerifyEmail() {
  const [params] = useSearchParams();
  const uid = params.get("uid");
  const token = params.get("token");

  const { isPending, isSuccess, isError } = useQuery({
    // Keyed by the actual token — React Query's own request deduplication
    // (which correctly handles StrictMode's double-invoke out of the box)
    // guarantees this fires exactly once for a given token, no manual
    // ref-guard needed.
    queryKey: ["verify-email", uid, token],
    queryFn: () =>
      apiClient.post("/accounts/verify-email/", { uid, token }).then((r) => r.data),
    enabled: !!uid && !!token,
    retry: false,           // a failed/used token should never be retried
    staleTime: Infinity,    // never refetch — this action is genuinely one-time
    gcTime: Infinity,
  });

  if (!uid || !token) {
    return <p className="p-8 text-center text-red-600">Invalid verification link.</p>;
  }

  return (
    <div className="mx-auto max-w-sm py-24 text-center">
      {isPending && (
        <div className="flex flex-col items-center gap-3">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-black" />
          <p>Verifying your email...</p>
        </div>
      )}
      {isSuccess && (
        <>
          <h1 className="mb-2 text-xl font-bold">Email verified!</h1>
          <Link to="/login" className="underline">Log in now</Link>
        </>
      )}
      {isError && <p className="text-red-600">This link is invalid or has expired.</p>}
    </div>
  );
}