import api from "./api";

export const getAttendance = async () => {
  const response = await api.get("/attendance");

  return response.data;
};
