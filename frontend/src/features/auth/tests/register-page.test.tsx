import { render, screen, waitFor } from "@testing-library/react";
import RegisterPage from "@/app/(auth)/register/page";
import userEvent from "@testing-library/user-event";



const mockRegisterUser = jest.fn();

jest.mock("@/features/auth/services/auth-service", () => ({
  registerUser: (...args: unknown[]) => mockRegisterUser(...args),
}));

describe("RegisterPage", () => {
    
    beforeEach(() => {
        mockRegisterUser.mockReset();
        mockRegisterUser.mockResolvedValue({
            uuid: "550e8400-e29b-41d4-a716-446655440000",
            username: "john",
            email: "john@example.com",
        });
    });

  it("renders the registration form", () => {
    render(<RegisterPage />);

    expect(
      screen.getByRole("heading", {
        name: /create account/i,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/username/i),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/email/i),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/password/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    ).toBeInTheDocument();
  });

  beforeEach(() => {
      mockRegisterUser.mockReset();
      mockRegisterUser.mockResolvedValue({
          uuid: "550e8400-e29b-41d4-a716-446655440000",
          username: "john",
          email: "john@example.com",
      });
  });

  it("submits registration details through the auth service", async () => {
    const user = userEvent.setup();

    render(<RegisterPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );

    await user.type(
      screen.getByLabelText(/email/i),
      "john@example.com",
    );

    await user.type(
      screen.getByLabelText(/password/i),
      "StrongPassword123!",
    );

    await user.click(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    );

    expect(mockRegisterUser).toHaveBeenCalledWith({
      username: "john",
      email: "john@example.com",
      password: "StrongPassword123!",
    });
  });

  it("shows a submitting state while registration is in progress", async () => {
    const user = userEvent.setup();

    let resolveRegistration: (
      value: {
        uuid: string;
        username: string;
        email: string;
      },
    ) => void = () => {};

    mockRegisterUser.mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveRegistration = resolve;
        }),
    );

    render(<RegisterPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );

    await user.type(
      screen.getByLabelText(/email/i),
      "john@example.com",
    );

    await user.type(
      screen.getByLabelText(/password/i),
      "StrongPassword123!",
    );

    const submitButton = screen.getByRole("button", {
      name: /create account/i,
    });

    await user.click(submitButton);

    expect(
      screen.getByRole("button", {
        name: /creating account/i,
      }),
    ).toBeDisabled();

    resolveRegistration({
      uuid: "550e8400-e29b-41d4-a716-446655440000",
      username: "john",
      email: "john@example.com",
    });

    await waitFor(() => {
      expect(
        screen.getByRole("button", {
          name: /create account/i,
        }),
      ).not.toBeDisabled();
    });
  });

  it("displays an error when registration fails", async () => {
    const user = userEvent.setup();

    mockRegisterUser.mockRejectedValue(
      new Error("A user with this email already exists."),
    );

    render(<RegisterPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );

    await user.type(
      screen.getByLabelText(/email/i),
      "john@example.com",
    );

    await user.type(
      screen.getByLabelText(/password/i),
      "StrongPassword123!",
    );

    await user.click(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    );

    expect(
      await screen.findByText(
        "A user with this email already exists.",
      ),
    ).toBeInTheDocument();
  });

  it("displays a success message after registration", async () => {
    const user = userEvent.setup();

    mockRegisterUser.mockResolvedValue({
      uuid: "550e8400-e29b-41d4-a716-446655440000",
      username: "john",
      email: "john@example.com",
    });

    render(<RegisterPage />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );

    await user.type(
      screen.getByLabelText(/email/i),
      "john@example.com",
    );

    await user.type(
      screen.getByLabelText(/password/i),
      "StrongPassword123!",
    );

    await user.click(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    );

    expect(
      await screen.findByText(
        /account created successfully/i,
      ),
    ).toBeInTheDocument();
    
    expect(
      screen.getByRole("link", {
        name: /sign in/i,
      }),
    ).toHaveAttribute("href", "/login");
  });
});