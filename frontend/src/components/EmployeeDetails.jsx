function EmployeeDetails({ employee, onClose }) {
  if (!employee) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-2xl bg-white shadow-2xl">
        {/* Header */}

        <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
          <div>
            <h2 className="text-xl font-bold text-slate-800">
              Employee Details
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Employee profile information
            </p>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg px-3 py-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
          >
            ✕
          </button>
        </div>

        {/* Profile */}

        <div className="px-6 py-6">
          <div className="mb-6 flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-900 text-xl font-bold text-white">
              {employee.name?.charAt(0).toUpperCase()}
            </div>

            <div>
              <h3 className="text-xl font-semibold text-slate-800">
                {employee.name}
              </h3>

              <p className="text-sm text-slate-500">{employee.employee_code}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <InfoItem label="Email" value={employee.email} />

            <InfoItem label="Department" value={employee.department} />

            <InfoItem label="Designation" value={employee.designation} />

            <InfoItem
              label="Status"
              value={employee.is_active ? "Active" : "Inactive"}
            />

            <InfoItem label="Employee ID" value={employee.id} />

            <InfoItem
              label="Created"
              value={new Date(employee.created_at).toLocaleDateString()}
            />
          </div>
        </div>

        {/* Footer */}

        <div className="flex justify-end border-t border-slate-200 px-6 py-4">
          <button
            onClick={onClose}
            className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function InfoItem({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-50 p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-medium text-slate-700">
        {value || "Not specified"}
      </p>
    </div>
  );
}

export default EmployeeDetails;
