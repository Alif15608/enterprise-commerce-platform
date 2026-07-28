import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useConfirmPasswordReset } from "../hooks/useAuth";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [newPassword, setNewPassword] = useState("");
  const confirmReset = useConfirmPasswordReset();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const uid = params.get("uid");
    const token = params.get("token");
    if (!uid || !token) return;

    confirmReset.mutate(
      { uid, token, new_password: newPassword },
      { onSuccess: () => navigate("/login") }
    );
  };

  return (
    <div className="mx-auto max-w-sm py-16">
      <h1 className="mb-6 text-2xl font-bold">Reset password</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input type="password" placeholder="New password" required
          value={newPassword} onChange={(e) => setNewPassword(e.target.value)}
          className="rounded border px-3 py-2" />
        <button type="submit" disabled={confirmReset.isPending}
          className="rounded bg-black py-2 text-white disabled:opacity-50">
          Reset password
        </button>
      </form>
    </div>
  );
}