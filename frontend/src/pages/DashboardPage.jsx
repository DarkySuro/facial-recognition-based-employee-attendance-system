import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";

import { getEmployees } from "../services/employeeService";
import { getAllAttendance } from "../services/attendanceService";
import { getAllRecognitionLogs } from "../services/recognitionLogService";
import { getLocalDateString } from "../helpers/localDate";

function DashboardPage() {
  const [employees, setEmployees] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [recognitionLogs, setRecognitionLogs] = useState([]);

  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState(false);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setApiError(false);

        const [employeesData, attendanceData, recognitionLogsData] =
          await Promise.all([
            getEmployees(),
            getAllAttendance(),
            getAllRecognitionLogs(),
          ]);

        setEmployees(employeesData);
        setAttendance(attendanceData);
        setRecognitionLogs(recognitionLogsData);
      } catch (error) {
        console.error("Failed to load dashboard:", error);

        setApiError(true);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();

    const interval = setInterval(loadDashboard, 50000);

    return () => clearInterval(interval);
  }, []);
  
  const activeEmployees = employees.filter((employee) => employee.is_active);

  const today = getLocalDateString();

  console.log("Local today:", today);
  console.log("Attendance data:", attendance);

  attendance.forEach((record) => {
    console.log({
      id: record.id,
      attendance_date: record.attendance_date,
      type: typeof record.attendance_date,
      matches: record.attendance_date === today,
    });
  });


  const todayAttendance = attendance.filter(
    (record) => record.attendance_date === today,
  );

  console.log("Today's attendance:", todayAttendance);

  if (loading) {
    return (
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Dashboard</h1>

        <p className="text-slate-500 mt-2">Loading system data...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Dashboard</h1>

          <p className="text-slate-500 mt-2">
            AI-powered employee attendance overview
          </p>
        </div>

        <div
          className={`
            flex items-center gap-2
            px-3 py-2
            rounded-lg
            text-sm font-medium
            ${
              apiError
                ? "bg-red-100 text-red-700"
                : "bg-green-100 text-green-700"
            }
          `}
        >
          <span className="w-2 h-2 rounded-full bg-current" />

          {apiError ? "API Disconnected" : "API Connected"}
        </div>
      </div>

      {/* Error */}

      {apiError && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">
          Unable to load dashboard data. Please make sure the FastAPI backend is
          running.
        </div>
      )}

      {/* Statistics */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <StatCard
          title="Total Employees"
          value={employees.length}
          subtitle={"Registered employee" + (employees.length > 1 ? "s" : "")}
          icon="👥"
        />

        <StatCard
          title="Active Employees"
          value={activeEmployees.length}
          subtitle="Currently active"
          icon="✓"
        />

        <StatCard
          title="Today's Attendance"
          value={todayAttendance.length}
          subtitle={
            "Employee" + (todayAttendance.length > 1 ? "s" : "") + " checked in"
          }
          icon="📅"
        />

        <StatCard
          title="Recognition Events"
          value={recognitionLogs.length}
          subtitle="Recorded recognition events"
          icon="👁"
        />
      </div>

      {/* Recent Attendance */}

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div className="p-6 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800">
            Recent Attendance
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            Latest employee attendance records
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase">
                  Employee
                </th>

                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase">
                  Date
                </th>

                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase">
                  Check-in
                </th>

                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase">
                  Confidence
                </th>

                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase">
                  Status
                </th>
              </tr>
            </thead>

            <tbody>
              {attendance.slice(0, 5).map((record) => {
                const employee = employees.find(
                  (item) => item.id === record.employee_id,
                );

                return (
                  <tr key={record.id} className="border-t border-slate-100">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-800">
                        {employee
                          ? employee.name
                          : `Employee #${record.employee_id}`}
                      </div>

                      {employee && (
                        <div className="text-xs text-slate-500">
                          {employee.employee_code}
                        </div>
                      )}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {record.attendance_date}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {new Date(record.check_in_time).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </td>

                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      {(record.recognition_confidence * 100).toFixed(1)}%
                    </td>

                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 text-xs font-medium rounded-full bg-green-100 text-green-700">
                        {record.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recognition Activity */}

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div className="p-6 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800">
            Recognition Activity
          </h2>

          <p className="text-sm text-slate-500 mt-1">
            Latest face recognition events
          </p>
        </div>

        <div className="divide-y divide-slate-100">
          {recognitionLogs.slice(0, 5).map((log) => {
            const employee = employees.find(
              (item) => item.id === log.employee_id,
            );

            return (
              <div
                key={log.id}
                className="px-6 py-4 flex items-center justify-between"
              >
                <div>
                  <p className="font-medium text-slate-800">
                    {employee ? employee.name : "Unknown person"}
                  </p>

                  <p className="text-xs text-slate-500 mt-1">
                    {new Date(log.timestamp).toLocaleString()}
                  </p>
                </div>

                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-700">
                    {log.confidence !== null
                      ? `${(log.confidence * 100).toFixed(1)}%`
                      : "N/A"}
                  </p>

                  <p className="text-xs text-slate-500">
                    {log.processing_time_ms} ms
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
