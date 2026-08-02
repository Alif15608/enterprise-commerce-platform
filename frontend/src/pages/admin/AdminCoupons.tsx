import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "../../api/client";

export default function AdminCoupons() {
  const queryClient = useQueryClient();
  const { data: coupons } = useQuery({
    queryKey: ["admin", "coupons"],
    queryFn: () => apiClient.get("/orders/coupons/").then((r) => r.data),
  });

  const createCoupon = useMutation({
    mutationFn: (data: any) => apiClient.post("/orders/coupons/", data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "coupons"] }),
  });

  const [form, setForm] = useState({
    code: "", discount_type: "percentage", amount: "",
    valid_from: "", valid_until: "", max_uses: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createCoupon.mutate({
      ...form,
      max_uses: form.max_uses ? Number(form.max_uses) : null,
      valid_from: new Date(form.valid_from).toISOString(),
      valid_until: new Date(form.valid_until).toISOString(),
    });
    setForm({ code: "", discount_type: "percentage", amount: "", valid_from: "", valid_until: "", max_uses: "" });
  };

  const deleteCoupon = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/orders/coupons/${id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "coupons"] }),
  });

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Coupons</h1>
      <table className="mb-6 w-full text-left text-sm">
        <thead><tr className="border-b"><th>Code</th><th>Type</th><th>Amount</th><th>Used</th><th>Max</th><th>Valid Until</th><th></th></tr></thead>
        <tbody>
          {coupons?.map((c: any) => (
            <tr key={c.id} className="border-b">
              <td className="py-2">{c.code}</td>
              <td>{c.discount_type}</td>
              <td>{c.amount}</td>
              <td>{c.times_used}</td>
              <td>{c.max_uses ?? "∞"}</td>
              <td>{new Date(c.valid_until).toLocaleDateString()}</td>
              <td>
                <button onClick={() => deleteCoupon.mutate(c.id)} className="text-sm text-red-500 hover:underline">
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 className="mb-2 font-semibold">New Coupon</h2>
      <form onSubmit={handleSubmit} className="flex max-w-md flex-col gap-2">
        <input placeholder="Code (e.g. SAVE10)" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })} className="rounded border px-3 py-2" required />
        <select value={form.discount_type} onChange={(e) => setForm({ ...form, discount_type: e.target.value })} className="rounded border px-3 py-2">
          <option value="percentage">Percentage</option>
          <option value="flat">Flat amount</option>
        </select>
        <input type="number" placeholder="Amount" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} className="rounded border px-3 py-2" required />
        <label className="text-xs text-gray-500">Valid from</label>
        <input type="datetime-local" value={form.valid_from} onChange={(e) => setForm({ ...form, valid_from: e.target.value })} className="rounded border px-3 py-2" required />
        <label className="text-xs text-gray-500">Valid until</label>
        <input type="datetime-local" value={form.valid_until} onChange={(e) => setForm({ ...form, valid_until: e.target.value })} className="rounded border px-3 py-2" required />
        <input type="number" placeholder="Max uses (blank = unlimited)" value={form.max_uses} onChange={(e) => setForm({ ...form, max_uses: e.target.value })} className="rounded border px-3 py-2" />
        <button type="submit" className="rounded bg-black py-2 text-white">Create coupon</button>
      </form>
    </div>
  );
}