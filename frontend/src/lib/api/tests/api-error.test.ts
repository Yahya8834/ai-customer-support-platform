import { ApiError } from "../api-error";

describe("ApiError", () => {
  it("stores the error message and HTTP status", () => {
    const error = new ApiError("Invalid credentials", 401);

    expect(error).toBeInstanceOf(Error);
    expect(error).toBeInstanceOf(ApiError);
    expect(error.message).toBe("Invalid credentials");
    expect(error.status).toBe(401);
    expect(error.name).toBe("ApiError");
  });
});