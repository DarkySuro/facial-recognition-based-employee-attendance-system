import { useEffect, useState } from "react";

import { getAllRecognitionLogs } from "../services/recognitionLogService";

function RecognitionLogPage() {
  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);

  // ----------------------------------------
  // Load recognition logs
  // ----------------------------------------

  const loadLogs = async () => {
    try {
      setLoading(true);

      setError(null);

      const data = await getAllRecognitionLogs();

      setLogs(data);
    } catch (err) {
      console.error("Failed to load recognition logs:", err);

      setError("Unable to load recognition logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  // ----------------------------------------
  // Statistics
  // ----------------------------------------

  const totalLogs = logs.length;

  const recognizedCount = logs.filter((log) => log.recognized).length;

  const unknownCount = logs.filter((log) => !log.recognized).length;

  // ----------------------------------------
  // Helpers
  // ----------------------------------------

  const formatDateTime = (timestamp) => {
    if (!timestamp) {
      return "—";
    }

    return new Date(timestamp).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const formatConfidence = (confidence) => {
    if (confidence === null || confidence === undefined) {
      return "—";
    }

    return `${(confidence * 100).toFixed(1)}%`;
  };

  return (
    <div className="space-y-8">
      {/* Header */}

      <div>
        <h1 className="text-3xl font-bold text-slate-800">Recognition Logs</h1>

        <p className="mt-2 text-slate-500">
          Monitor facial recognition activity and system performance.
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
        <RecognitionStatCard
          title="Total Events"
          value={totalLogs}
          description="Recognition attempts"
        />

        <RecognitionStatCard
          title="Recognized"
          value={recognizedCount}
          description="Successful recognitions"
        />

        <RecognitionStatCard
          title="Unknown"
          value={unknownCount}
          description="Unrecognized faces"
        />
      </div>

      {/* Error state */}

      {error && (
        <div className="flex items-center justify-between rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
          <span>{error}</span>

          <button onClick={loadLogs} className="font-medium underline">
            Retry
          </button>
        </div>
      )}

      {/* Recognition log table */}

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 px-6 py-5">
          <h2 className="font-semibold text-slate-800">Recognition Activity</h2>

          <p className="mt-1 text-sm text-slate-500">
            Recent recognition events recorded by the AI system.
          </p>
        </div>

        {loading ? (
          <div className="px-6 py-16 text-center">
            <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-slate-800" />

            <p className="text-sm text-slate-500">
              Loading recognition logs...
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Event ID
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Employee
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Camera
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Result
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Confidence
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Processing
                  </th>

                  <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Timestamp
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-100">
                {logs.map((log) => (
                  <tr key={log.id} className="transition hover:bg-slate-50">
                    <td className="px-6 py-4 text-sm text-slate-500">
                      #{log.id}
                    </td>

                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      {log.employee_id
                        ? `Employee ${log.employee_id}`
                        : "Unknown"}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {log.camera_id ? `Camera ${log.camera_id}` : "—"}
                    </td>

                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                          log.recognized
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {log.recognized ? "Recognized" : "Unknown"}
                      </span>
                    </td>

                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      {formatConfidence(log.confidence)}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {log.processing_time_ms !== null
                        ? `${log.processing_time_ms} ms`
                        : "—"}
                    </td>

                    <td className="px-6 py-4 text-sm text-slate-600">
                      {formatDateTime(log.timestamp)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {logs.length === 0 && (
              <div className="px-6 py-12 text-center text-sm text-slate-500">
                No recognition logs found.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function RecognitionStatCard({ title, value, description }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{title}</p>

      <p className="mt-3 text-3xl font-bold text-slate-800">{value}</p>

      <p className="mt-2 text-sm text-slate-400">{description}</p>
    </div>
  );
}

export default RecognitionLogPage;
