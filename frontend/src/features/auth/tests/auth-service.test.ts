import { registerUser } from "../services/auth-service";

const mockApiClient = jest.fn();

jest.mock("@/lib/api/client", () => ({
  apiClient: (...args: unknown[]) => mockApiClient(...args),
}));

describe("registerUser", () => {
  beforeEach(() => {
    mockApiClient.mockReset();
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

    mockApiClient.mockResolvedValue(response);

    const result = await registerUser(request);

    expect(mockApiClient).toHaveBeenCalledWith("/api/v1/register/", {
      method: "POST",
      body: JSON.stringify(request),
    });

    expect(result).toEqual(response);
  });
});