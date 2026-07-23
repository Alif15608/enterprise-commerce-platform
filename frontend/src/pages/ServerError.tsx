// ServerError.tsx
export default function ServerError() {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-24 text-center">
      <h1 className="text-3xl font-bold">Something went wrong</h1>
      <p className="text-gray-500">Please try again shortly.</p>
    </div>
  );
}