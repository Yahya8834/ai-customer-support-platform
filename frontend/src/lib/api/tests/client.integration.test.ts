/**
 * @jest-environment node
 */

import { apiClient } from "../client";

describe("apiClient integration", () => {
  it("communicates with the real Django API", async () => {
    process.env.NEXT_PUBLIC_API_BASE_URL =
      process.env.API_TEST_BASE_URL;

    const response = await apiClient<{ status: string }>(
      "/api/v1/health/",
    );

    expect(response).toEqual({
      status: "ok",
    });
  });
});