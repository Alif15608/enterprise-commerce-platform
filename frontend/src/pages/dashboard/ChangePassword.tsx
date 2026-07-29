// pages/dashboard/ChangePassword.tsx (new)
import { useState } from "react";
import { useChangePassword } from "../../hooks/useAuth";

export default function ChangePassword() {
  const [form, setForm] = useState({ old_password: "", new_password: "" });
  const changePassword = useChangePassword();
  return (
    <form onSubmit={(e) => { e.preventDefault(); changePassword.mutate(form); }} className="flex max-w-sm flex-col gap-3">
      <h1 className="text-xl font-bold">Change Password</h1>
      <input type="password" placeholder="Current password" value={form.old_password} onChange={(e) => setForm({ ...form, old_password: e.target.value })} className="rounded border px-3 py-2" required />
      <input type="password" placeholder="New password" value={form.new_password} onChange={(e) => setForm({ ...form, new_password: e.target.value })} className="rounded border px-3 py-2" required />
      <button type="submit" className="rounded bg-black py-2 text-white">Update password</button>
    </form>
  );
}