import { Toaster as HotToaster } from "react-hot-toast";

export default function Toaster() {
  return (
    <HotToaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: { fontSize: "0.875rem" },
      }}
    />
  );
}