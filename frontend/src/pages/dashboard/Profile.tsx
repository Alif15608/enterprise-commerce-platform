import { useAuthStore } from "../../store/authStore";

export default function Profile() {
  const user = useAuthStore((s) => s.user);

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Profile</h1>
      <div className="flex flex-col gap-2 text-sm">
        <p><span className="text-gray-500">Email:</span> {user?.email}</p>
        <p><span className="text-gray-500">Name:</span> {user?.first_name} {user?.last_name}</p>
        {/* <p><span className="text-gray-500">Roles:</span> {user?.roles.join(", ")}</p> */}
      </div>
      {/* Editing profile fields would call a PATCH /accounts/me/ endpoint —
          not built in Phase 5 (UserSerializer is read-only). Flagging as
          a real gap: adding profile editing needs a small backend addition
          (an UpdateProfileView), same pattern as everything above. */}
    </div>
  );
}