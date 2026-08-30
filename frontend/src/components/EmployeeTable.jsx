function EmployeeTable({ employees, onSelect }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
              Employee
            </th>

            <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
              Department
            </th>

            <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
              Designation
            </th>

            <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
              Status
            </th>

            <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-500">
              Action
            </th>
          </tr>
        </thead>

        <tbody className="divide-y divide-slate-100">
          {employees.map((employee) => (
            <tr key={employee.id} className="transition hover:bg-slate-50">
              <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">
                    {employee.name?.charAt(0).toUpperCase()}
                  </div>

                  <div>
                    <p className="font-medium text-slate-800">
                      {employee.name}
                    </p>

                    <p className="text-xs text-slate-500">
                      {employee.employee_code}
                    </p>
                  </div>
                </div>
              </td>

              <td className="px-6 py-4 text-sm text-slate-600">
                {employee.department || "—"}
              </td>

              <td className="px-6 py-4 text-sm text-slate-600">
                {employee.designation || "—"}
              </td>

              <td className="px-6 py-4">
                <span
                  className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                    employee.is_active
                      ? "bg-green-100 text-green-700"
                      : "bg-slate-100 text-slate-500"
                  }`}
                >
                  {employee.is_active ? "Active" : "Inactive"}
                </span>
              </td>

              <td className="px-6 py-4 text-right">
                <button
                  onClick={() => onSelect(employee)}
                  className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {employees.length === 0 && (
        <div className="px-6 py-12 text-center text-sm text-slate-500">
          No employees found.
        </div>
      )}
    </div>
  );
}

export default EmployeeTable;
