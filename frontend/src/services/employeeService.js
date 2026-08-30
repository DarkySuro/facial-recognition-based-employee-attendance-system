import api from "./api";

export const getEmployees = async () => {
  const response = await api.get("/employees");

  return response.data;
};

export const getEmployee = async (employeeId) => {
  const response = await api.get(`/employees/${employeeId}`);
  return response.data;
};