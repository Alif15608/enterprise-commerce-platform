import { useState } from "react";
import { useRegister } from "../hooks/useAuth";

export default function Register() {
  const [form, setForm] = useState({ email: "", password: "", first_name: "", last_name: "" });
  const register = useRegister();
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    register.mutate(form, { onSuccess: () => setSubmitted(true) });
  };

  if (submitted) {
    return (
      <div className="mx-auto max-w-sm py-16 text-center">
        <h1 className="mb-2 text-xl font-bold">Check your email</h1>
        <p className="text-gray-500">We sent a verification link to {form.email}.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-sm py-16">
      <h1 className="mb-6 text-2xl font-bold">Create an account</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input placeholder="First name" value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
          className="rounded border px-3 py-2" />
        <input placeholder="Last name" value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
          className="rounded border px-3 py-2" />
        <input type="email" placeholder="Email" required value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="rounded border px-3 py-2" />
        <input type="password" placeholder="Password" required value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          className="rounded border px-3 py-2" />
        <button type="submit" disabled={register.isPending}
          className="rounded bg-black py-2 text-white disabled:opacity-50">
          {register.isPending ? "Creating..." : "Create account"}
        </button>
      </form>
    </div>
  );
}