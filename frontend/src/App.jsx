import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import EnrollmentPage from "./pages/EnrollmentPage";
import AttendancePage from "./pages/AttendancePage";
import RecognitionLogPage from "./pages/RecognitionLogPage";

function App() {
  return (
    <BrowserRouter>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />

          <Route path="/employees" element={<EmployeesPage />} />

          <Route path="/enrollment" element={<EnrollmentPage />} />

          <Route path="/attendance" element={<AttendancePage />} />

          <Route path="/recognition-log" element={<RecognitionLogPage />} />
        </Routes>
      </DashboardLayout>
    </BrowserRouter>
  );
}

export default App;
