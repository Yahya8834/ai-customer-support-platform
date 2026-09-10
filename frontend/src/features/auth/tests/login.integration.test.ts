/**
 * @jest-environment node
 */

import { loginUser } from "../services/auth-service";

describe("login integration", () => {
  it("logs in through the real Django API", async () => {
    process.env.NEXT_PUBLIC_API_BASE_URL =
      process.env.API_TEST_BASE_URL;

    const result = await loginUser({
      username: "frontend-integration-user",
      password: "FrontendIntegration123!",
    });

    expect(result).toEqual(
      expect.objectContaining({
        access: expect.any(String),
        refresh: expect.any(String),
      }),
    );
  });
});