import { ApiError } from "../api-error";
import { apiClient } from "../client";

describe("apiClient", () => {
  it("throws ApiError when the API returns a failed response", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 401,
    });

    await expect(apiClient("/api/v1/me/")).rejects.toEqual(
      expect.objectContaining({
        message: "API request failed with status 401",
        status: 401,
      }),
    );

    try {
      await apiClient("/api/v1/me/");
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
    }
  });
});