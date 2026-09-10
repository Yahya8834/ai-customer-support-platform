import { apiClient } from "@/lib/api/client";

import type {
  RegisterRequest,
  RegisterResponse,
} from "../types/auth";

const AUTH_BASE_PATH = "/api/v1";

export function registerUser(
  data: RegisterRequest,
): Promise<RegisterResponse> {
  return apiClient<RegisterResponse>(`${AUTH_BASE_PATH}/register/`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}