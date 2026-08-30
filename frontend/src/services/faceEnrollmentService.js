import api from "./api";

export const enrollFaceFromImages = async (employeeId, files) => {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  // Debug: inspect FormData
  for (const [key, value] of formData.entries()) {
    console.log(
      "FormData:",
      key,
      value instanceof File
        ? {
            name: value.name,
            type: value.type,
            size: value.size,
          }
        : value,
    );
  }

  const response = await api.post(
    `/employees/${employeeId}/face-enrollment/images`,
    formData,
    {
      headers: {
        "Content-Type": undefined,
      }
    }
  );

  return response.data;
};
