import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RegisterForm from "../components/register-form";


describe("RegisterForm", () => {
  it("allows the user to enter registration details", async () => {
    const user = userEvent.setup();

    render(<RegisterForm onSubmit={jest.fn()} />);

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

    expect(screen.getByLabelText(/username/i)).toHaveValue("john");
    expect(screen.getByLabelText(/email/i)).toHaveValue(
      "john@example.com",
    );
    expect(screen.getByLabelText(/password/i)).toHaveValue(
      "StrongPassword123!",
    );
  });

  it("submits registration details", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<RegisterForm onSubmit={onSubmit} />);

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

    expect(onSubmit).toHaveBeenCalledWith({
      username: "john",
      email: "john@example.com",
      password: "StrongPassword123!",
    });
  });

  it("requires all registration fields", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<RegisterForm onSubmit={onSubmit} />);

    await user.click(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    );

    expect(onSubmit).not.toHaveBeenCalled();

    expect(
      screen.getByLabelText(/username/i),
    ).toBeInvalid();

    expect(
      screen.getByLabelText(/email/i),
    ).toBeInvalid();

    expect(
      screen.getByLabelText(/password/i),
    ).toBeInvalid();
  });

  it("requires a valid email address", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<RegisterForm onSubmit={onSubmit} />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );

    await user.type(
      screen.getByLabelText(/email/i),
      "not-an-email",
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

    expect(onSubmit).not.toHaveBeenCalled();

    expect(
      screen.getByLabelText(/email/i),
    ).toBeInvalid();
  });

  it("requires a password of at least 8 characters", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<RegisterForm onSubmit={onSubmit} />);

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
      "short",
    );

    await user.click(
      screen.getByRole("button", {
        name: /create account/i,
      }),
    );

    const passwordInput = screen.getByLabelText(/password/i);

    expect(passwordInput).toHaveAttribute("minlength", "8");
    expect(onSubmit).not.toHaveBeenCalled();
  });
});