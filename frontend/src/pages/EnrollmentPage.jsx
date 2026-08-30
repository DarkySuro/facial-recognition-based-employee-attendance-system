import { useState } from "react";
import { enrollFaceFromImages } from "../services/faceEnrollmentService";

function EnrollmentPage() {
  const [employeeId, setEmployeeId] = useState("");
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------
  // Handle image selection
  // ------------------------------------------

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files || []);

    setFiles((previousFiles) => [...previousFiles, ...selectedFiles]);

    setMessage("");
    setError("");

    // Allow selecting the same file again if needed
    event.target.value = "";
  };

  // ------------------------------------------
  // Submit enrollment
  // ------------------------------------------

  const handleSubmit = async (event) => {
    event.preventDefault();

    setMessage("");
    setError("");

    if (!employeeId) {
      setError("Please enter an employee ID.");
      return;
    }

    if (files.length < 5) {
      setError(
        `Please select at least 5 face images. ${files.length}/5`
      );
      return;
    }

    try {
      setLoading(true);

      const result = await enrollFaceFromImages(employeeId, files);

      console.log("Enrollment response:", result);

      setMessage(
        `Face enrollment successful. ${result.embeddings_saved} embeddings saved.`,
      );

      setFiles([]);
      // event.target.reset();
    } catch (err) {
      console.error("Face enrollment failed:", err);
      console.error("Response data:", err.response?.data);

      console.error(
        "Validation detail:",
        JSON.stringify(err.response?.data?.detail, null, 2),
      );

      const responseData = err.response?.data;

      if (Array.isArray(responseData?.detail)) {
        const validationErrors = responseData.detail
          .map((item) => {
            const location = item.loc?.join(" → ") || "request";
            return `${location}: ${item.msg}`;
          })
          .join("\n");

        setError(validationErrors);
      } else {
        setError(
          responseData?.detail || "Face enrollment failed. Please try again.",
        );
      }
    } finally {
      console.log("Finally reached");
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">

      {/* -------------------------------------- */}
      {/* Page Header                            */}
      {/* -------------------------------------- */}

      <div>
        <h1 className="text-3xl font-bold text-slate-800">
          Face Enrollment
        </h1>

        <p className="text-slate-500 mt-2">
          Register employee face embeddings
        </p>
      </div>

      {/* -------------------------------------- */}
      {/* Enrollment Form                        */}
      {/* -------------------------------------- */}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 max-w-2xl">

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Employee ID */}

          <div>
            <label
              htmlFor="employeeId"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              Employee ID
            </label>

            <input
              id="employeeId"
              type="number"
              min="1"
              value={employeeId}
              onChange={(event) =>
                setEmployeeId(event.target.value)
              }
              placeholder="Enter employee ID"
              className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-400"
            />
          </div>

          {/* Image Upload */}

          <div>
            <label
              htmlFor="faceImages"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              Face Images
            </label>

            <input
              id="faceImages"
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileChange}
              className="block w-full text-sm text-slate-600
                         file:mr-4 file:py-2.5 file:px-4
                         file:rounded-lg file:border-0
                         file:text-sm file:font-medium
                         file:bg-slate-100 file:text-slate-700
                         hover:file:bg-slate-200"
            />

            <p className="text-xs text-slate-500 mt-2">
              Select at least 5 clear face images.
            </p>
          </div>

          {/* Selected Files */}

          {files.length > 0 && (
            <div className="border border-slate-200 rounded-lg p-4">

              <p className="text-sm font-medium text-slate-700 mb-3">
                Selected Images ({files.length})
              </p>

              <div className="space-y-2">

                {files.map((file, index) => (
                  <div
                    key={`${file.name}-${index}`}
                    className="flex items-center justify-between bg-slate-50 px-3 py-2 rounded-md"
                  >
                    <span className="text-sm text-slate-700 truncate">
                      {index + 1}. {file.name}
                    </span>

                    <span className="text-xs text-slate-400 ml-4">
                      {(file.size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                ))}

              </div>

            </div>
          )}

          {/* Success Message */}

          {message && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
              {message}
            </div>
          )}

          {/* Error Message */}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm whitespace-pre-line">
              {error}
            </div>
          )}

          {/* Submit */}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-slate-800 text-white py-3 rounded-lg font-medium hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Enroll Face"}
          </button>

        </form>

      </div>
    </div>
  );
}

export default EnrollmentPage;

