import { apiClient } from "@/lib/api/client";

import type {
  LoginRequest,
  LoginResponse,
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

export function loginUser(
  data: LoginRequest,
): Promise<LoginResponse> {
  return apiClient<LoginResponse>(`${AUTH_BASE_PATH}/login/`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}