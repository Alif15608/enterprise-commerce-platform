import { useSearchParams } from "react-router-dom";

export default function Pagination({ hasNext, hasPrevious }: { hasNext: boolean; hasPrevious: boolean }) {
  const [params, setParams] = useSearchParams();
  const currentPage = Number(params.get("page") || "1");

  const goTo = (page: number) => {
    const next = new URLSearchParams(params);
    next.set("page", String(page));
    setParams(next);
    window.scrollTo({ top: 0 });
  };

  return (
    <div className="flex justify-center gap-4 py-6">
      <button disabled={!hasPrevious} onClick={() => goTo(currentPage - 1)} className="disabled:opacity-30">
        ← Previous
      </button>
      <span className="text-sm text-gray-500">Page {currentPage}</span>
      <button disabled={!hasNext} onClick={() => goTo(currentPage + 1)} className="disabled:opacity-30">
        Next →
      </button>
    </div>
  );
}