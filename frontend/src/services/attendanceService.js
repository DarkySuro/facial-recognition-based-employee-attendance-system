import api from "./api";

export const getAllAttendance = async () => {
  const response = await api.get("/attendance");

  return response.data;
};

export const getAttendanceByEmployee = async (employeeId) => {
  const response = await api.get(`/attendance/employee/${employeeId}`);

  return response.data;
};
