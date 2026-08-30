import { useEffect, useState } from "react";

import EmployeeTable from "../components/EmployeeTable";
import EmployeeDetails from "../components/EmployeeDetails";

import { getEmployees } from "../services/employeeService";

function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await getEmployees();

      setEmployees(data);
    } catch (err) {
      console.error("Failed to load employees:", err);

      setError("Unable to load employee data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEmployees();
  }, []);

  const activeCount = employees.filter((employee) => employee.is_active).length;

  return (
    <div className="space-y-8">
      {/* Header */}

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Employees</h1>

          <p className="mt-2 text-slate-500">
            Manage registered employees and their profiles.
          </p>
        </div>

        <div className="flex gap-3">
          <div className="rounded-xl border border-slate-200 bg-white px-5 py-3 shadow-sm">
            <p className="text-xs font-medium text-slate-500">Total</p>

            <p className="mt-1 text-xl font-bold text-slate-800">
              {employees.length}
            </p>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white px-5 py-3 shadow-sm">
            <p className="text-xs font-medium text-slate-500">Active</p>

            <p className="mt-1 text-xl font-bold text-green-600">
              {activeCount}
            </p>
          </div>
        </div>
      </div>

      {/* Error */}

      {error && (
        <div className="flex items-center justify-between rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
          <span>{error}</span>

          <button onClick={loadEmployees} className="font-medium underline">
            Retry
          </button>
        </div>
      )}

      {/* Employee table */}

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-6 py-5">
          <h2 className="font-semibold text-slate-800">Employee Directory</h2>

          <p className="mt-1 text-sm text-slate-500">
            All employees registered in the system.
          </p>
        </div>

        {loading ? (
          <div className="px-6 py-16 text-center">
            <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-slate-800" />

            <p className="text-sm text-slate-500">Loading employees...</p>
          </div>
        ) : (
          <EmployeeTable employees={employees} onSelect={setSelectedEmployee} />
        )}
      </div>

      {/* Employee details */}

      <EmployeeDetails
        employee={selectedEmployee}
        onClose={() => setSelectedEmployee(null)}
      />
    </div>
  );
}

export default EmployeesPage;
