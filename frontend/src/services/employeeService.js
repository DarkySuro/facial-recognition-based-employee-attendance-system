import api from "./api";

export const getEmployees = async () => {
  const response = await api.get("/employees");

  return response.data;
};

export const getEmployee = async (employeeId) => {
  const response = await api.get(`/employees/${employeeId}`);
  return response.data;
};

export const createEmployee = async (employeeData) => { 
  const response = await api.post("/employees", employeeData);
  return response.data;
};