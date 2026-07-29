import { useState } from "react";
import { useAddresses, useCreateAddress } from "../../hooks/useAddresses";

export default function Addresses() {
  const { data: addresses, isLoading } = useAddresses();
  const createAddress = useCreateAddress();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    full_name: "", phone: "", line1: "", line2: "",
    city: "", state: "", postal_code: "", country: "",
  });

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Addresses</h1>
      {addresses?.map((addr: any) => (
        <div key={addr.id} className="mb-2 rounded border p-3 text-sm">
          {addr.full_name}, {addr.line1}, {addr.city}, {addr.country}
          {addr.is_default && <span className="ml-2 text-xs text-green-600">(default)</span>}
        </div>
      ))}

      {!showForm ? (
        <button onClick={() => setShowForm(true)} className="mt-2 text-sm underline">
          + Add address
        </button>
      ) : (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            createAddress.mutate(form, { onSuccess: () => setShowForm(false) });
          }}
          className="mt-2 flex flex-col gap-2"
        >
          {Object.keys(form).map((field) => (
            <input
              key={field}
              placeholder={field.replace("_", " ")}
              value={(form as any)[field]}
              onChange={(e) => setForm({ ...form, [field]: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
          ))}
          <button type="submit" className="rounded bg-black py-2 text-white">Save</button>
        </form>
      )}
    </div>
  );
}