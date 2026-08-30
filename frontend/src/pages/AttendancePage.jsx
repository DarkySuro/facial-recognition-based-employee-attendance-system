import { useEffect, useState } from "react";

import { getAllAttendance, getAttendanceByEmployee } from "../services/attendanceService";

function AttendancePage() {
  const [attendance, setAttendance] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  // ----------------------------------------
  // Load attendance
  // ----------------------------------------

  const loadAttendance = async () => {
    try {
      setLoading(true);

      setError(null);

      const data = await getAllAttendance();

      setAttendance(data);
    } catch (err) {
      console.error("Failed to load attendance:", err);

      setError("Unable to load attendance data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAttendance();
  }, []);

  // ----------------------------------------
  // Statistics
  // ----------------------------------------

  const totalRecords = attendance.length;

  const presentCount = attendance.filter(
    (record) => record.status === "present",
  ).length;

  const uniqueEmployees = new Set(
    attendance.map((record) => record.employee_id),
  ).size;

  // ----------------------------------------
  // Helpers
  // ----------------------------------------

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };

  const formatTime = (dateTimeString) => {
    if (!dateTimeString) {
      return "—";
    }

    return new Date(dateTimeString).toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-8">
      {/* Header */}

      <div>
        <h1 className="text-3xl font-bold text-slate-800">Attendance</h1>

        <p className="mt-2 text-slate-500">
          Monitor employee attendance records and check-in activity.
        </p>
      </div>

      {/* Statistics */}

      <div
        className="
          grid
          grid-cols-1
          gap-5
          sm:grid-cols-2
          lg:grid-cols-3
        "
      >
        <AttendanceStatCard
          title="Total Records"
          value={totalRecords}
          description="Attendance entries"
        />

        <AttendanceStatCard
          title="Present"
          value={presentCount}
          description="Marked as present"
        />

        <AttendanceStatCard
          title="Employees"
          value={uniqueEmployees}
          description="Unique employees"
        />
      </div>

      {/* Error */}

      {error && (
        <div
          className="
            flex
            items-center
            justify-between
            rounded-xl
            border
            border-red-200
            bg-red-50
            px-5
            py-4
            text-sm
            text-red-700
          "
        >
          <span>{error}</span>

          <button
            onClick={loadAttendance}
            className="
              font-medium
              underline
            "
          >
            Retry
          </button>
        </div>
      )}

      {/* Attendance Table */}

      <div
        className="
          overflow-hidden
          rounded-2xl
          border
          border-slate-200
          bg-white
          shadow-sm
        "
      >
        <div
          className="
            border-b
            border-slate-200
            px-6
            py-5
          "
        >
          <h2
            className="
              font-semibold
              text-slate-800
            "
          >
            Attendance History
          </h2>

          <p
            className="
              mt-1
              text-sm
              text-slate-500
            "
          >
            Recent employee attendance records.
          </p>
        </div>

        {loading ? (
          <div
            className="
              px-6
              py-16
              text-center
            "
          >
            <div
              className="
                mx-auto
                mb-4
                h-8
                w-8
                animate-spin
                rounded-full
                border-4
                border-slate-200
                border-t-slate-800
              "
            />

            <p
              className="
                text-sm
                text-slate-500
              "
            >
              Loading attendance...
            </p>
          </div>
        ) : (
          <div
            className="
              overflow-x-auto
            "
          >
            <table
              className="
                w-full
              "
            >
              <thead
                className="
                  bg-slate-50
                "
              >
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    ID
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Employee ID
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Date
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Check In
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Check Out
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Status
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Confidence
                  </th>
                </tr>
              </thead>

              <tbody
                className="
                  divide-y
                  divide-slate-100
                "
              >
                {attendance.map((record) => (
                  <tr
                    key={record.id}
                    className="
                        transition
                        hover:bg-slate-50
                      "
                  >
                    <td className="px-6 py-4 text-sm text-slate-500">
                      #{record.id}
                    </td>

                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      {record.employee_id}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {formatDate(record.attendance_date)}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {formatTime(record.check_in_time)}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {formatTime(record.check_out_time)}
                    </td>

                    <td className="px-6 py-4">
                      <span
                        className="
                            inline-flex
                            rounded-full
                            bg-green-100
                            px-3
                            py-1
                            text-xs
                            font-medium
                            text-green-700
                          "
                      >
                        {record.status}
                      </span>
                    </td>

                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      {record.recognition_confidence
                        ? `${(record.recognition_confidence * 100).toFixed(1)}%`
                        : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {attendance.length === 0 && (
              <div
                className="
                  px-6
                  py-12
                  text-center
                  text-sm
                  text-slate-500
                "
              >
                No attendance records found.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function AttendanceStatCard({ title, value, description }) {
  return (
    <div
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
      "
    >
      <p
        className="
          text-sm
          font-medium
          text-slate-500
        "
      >
        {title}
      </p>

      <p
        className="
          mt-3
          text-3xl
          font-bold
          text-slate-800
        "
      >
        {value}
      </p>

      <p
        className="
          mt-2
          text-sm
          text-slate-400
        "
      >
        {description}
      </p>
    </div>
  );
}

export default AttendancePage;
