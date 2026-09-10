import { apiClient } from "@/lib/api/client";
import {loginUser, registerUser} from "../services/auth-service";


jest.mock("@/lib/api/client", () => ({
  apiClient: jest.fn(),
}));

const mockedApiClient = jest.mocked(apiClient);

describe("auth-service", () => {
  beforeEach(() => {
    mockedApiClient.mockReset();
  });

  it("sends registration data to the registration endpoint", async () => {
    const request = {
      username: "john",
      email: "john@example.com",
      password: "StrongPassword123!",
    };

    const response = {
      uuid: "550e8400-e29b-41d4-a716-446655440000",
      username: "john",
      email: "john@example.com",
    };

    mockedApiClient.mockResolvedValue(response);

    const result = await registerUser(request);

    expect(mockedApiClient).toHaveBeenCalledWith(
      "/api/v1/register/",
      {
        method: "POST",
        body: JSON.stringify(request),
      },
    );

    expect(result).toEqual(response);
  });

  it("logs in a user", async () => {
    const request = {
      username: "john",
      password: "password123",
    };

    const response = {
      access: "access-token",
      refresh: "refresh-token",
    };

    mockedApiClient.mockResolvedValue(response);

    const result = await loginUser(request);

    expect(mockedApiClient).toHaveBeenCalledWith(
      "/api/v1/login/",
      {
        method: "POST",
        body: JSON.stringify(request),
      },
    );

    expect(result).toEqual(response);
  });
});