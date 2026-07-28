import { useState } from "react";
import { useRequestPasswordReset } from "../hooks/useAuth";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const requestReset = useRequestPasswordReset();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    requestReset.mutate(email, { onSuccess: () => setSent(true) });
  };

  if (sent) {
    return (
      <div className="mx-auto max-w-sm py-24 text-center">
        <p>If that email is registered, a reset link has been sent.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-sm py-16">
      <h1 className="mb-6 text-2xl font-bold">Forgot password</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input type="email" placeholder="Email" required value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="rounded border px-3 py-2" />
        <button type="submit" disabled={requestReset.isPending}
          className="rounded bg-black py-2 text-white disabled:opacity-50">
          Send reset link
        </button>
      </form>
    </div>
  );
}