import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "@/app/(auth)/login/page";
import { loginUser } from "@/features/auth/services/auth-service";

const mockPush = jest.fn();

jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

jest.mock("@/features/auth/services/auth-service", () => ({
  loginUser: jest.fn(),
}));



describe("LoginPage", () => {

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the login form", () => {
    render(<LoginPage />);

    expect(
      screen.getByRole("heading", {
        name: /sign in/i,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/username/i),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/password/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", {
        name: /sign in/i,
      }),
    ).toBeInTheDocument();
  });

  it("logs in the user through the auth service", async () => {
    const user = userEvent.setup();

    jest.mocked(loginUser).mockResolvedValue({
      access: "access-token",
      refresh: "refresh-token",
    });

    render(<LoginPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );
    await user.type(
      screen.getByLabelText(/password/i),
      "password123",
    );

    await user.click(
      screen.getByRole("button", {
        name: /sign in/i,
      }),
    );

    expect(
      await screen.findByRole("button", {
        name: /sign in/i,
      }),
    ).toBeEnabled();

    expect(loginUser).toHaveBeenCalledWith({
      username: "john",
      password: "password123",
    });
  });

  it("redirects to the dashboard after successful login", async () => {
    const user = userEvent.setup();

    jest.mocked(loginUser).mockResolvedValue({
      access: "access-token",
      refresh: "refresh-token",
    });

    render(<LoginPage />);

    await user.type(screen.getByLabelText(/username/i), "john");
    await user.type(screen.getByLabelText(/password/i), "password123");

    await user.click(
      screen.getByRole("button", {
        name: /sign in/i,
      }),
    );

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/dashboard");
    });

    expect(loginUser).toHaveBeenCalledWith({
      username: "john",
      password: "password123",
    });
  });

  it("displays an error when login fails", async () => {
    const user = userEvent.setup();

    jest.mocked(loginUser).mockRejectedValue(
      new Error("Invalid username or password."),
    );

    render(<LoginPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );
    await user.type(
      screen.getByLabelText(/password/i),
      "wrong-password",
    );

    await user.click(
      screen.getByRole("button", {
        name: /sign in/i,
      }),
    );

    expect(
      await screen.findByRole("alert"),
    ).toHaveTextContent(
      "Invalid username or password.",
    );
  });
});