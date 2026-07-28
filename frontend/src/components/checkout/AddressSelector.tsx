import { useState } from "react";
import { useAddresses, useCreateAddress } from "../../hooks/useAddresses";

export default function AddressSelector({ onSelect }: { onSelect: (id: number) => void }) {
  const { data: addresses, isLoading } = useAddresses();
  const createAddress = useCreateAddress();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    full_name: "", phone: "", line1: "", line2: "",
    city: "", state: "", postal_code: "", country: "",
  });

  if (isLoading) return <p>Loading addresses...</p>;

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    createAddress.mutate(form, {
      onSuccess: (newAddress) => {
        onSelect(newAddress.id);
        setShowForm(false);
      },
    });
  };

  return (
    <div>
      {addresses?.length > 0 && (
        <div className="mb-4 flex flex-col gap-2">
          {addresses.map((addr: any) => (
            <label key={addr.id} className="flex items-center gap-2 rounded border p-3">
              <input type="radio" name="address" onChange={() => onSelect(addr.id)} />
              <span className="text-sm">
                {addr.full_name}, {addr.line1}, {addr.city}, {addr.country}
              </span>
            </label>
          ))}
        </div>
      )}

      {!showForm ? (
        <button onClick={() => setShowForm(true)} className="text-sm underline">
          + Add a new address
        </button>
      ) : (
        <form onSubmit={handleCreate} className="mt-2 flex flex-col gap-2">
          {(["full_name", "phone", "line1", "line2", "city", "state", "postal_code", "country"] as const).map((field) => (
            <input
              key={field}
              placeholder={field.replace("_", " ")}
              value={(form as any)[field]}
              onChange={(e) => setForm({ ...form, [field]: e.target.value })}
              required={field !== "line2"}
              className="rounded border px-3 py-2 text-sm"
            />
          ))}
          <button type="submit" disabled={createAddress.isPending} className="rounded bg-black py-2 text-white">
            Save address
          </button>
        </form>
      )}
    </div>
  );
}