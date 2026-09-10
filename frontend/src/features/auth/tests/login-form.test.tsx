import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginForm from "../components/login-form";


describe("LoginForm", () => {
  it("allows the user to enter login credentials", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(
      screen.getByLabelText(/username/i),
      "john",
    );
    await user.type(
      screen.getByLabelText(/password/i),
      "password123",
    );

    expect(screen.getByLabelText(/username/i)).toHaveValue("john");
    expect(screen.getByLabelText(/password/i)).toHaveValue(
      "password123",
    );
  });

  it("requires username and password", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.click(
      screen.getByRole("button", {
        name: /sign in/i,
      }),
    );
  
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByLabelText(/username/i)).toBeInvalid();
    expect(screen.getByLabelText(/password/i)).toBeInvalid();
  });

    it("submits the entered login credentials", async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn().mockResolvedValue(undefined);

    render(<LoginForm onSubmit={onSubmit} />);

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

    expect(onSubmit).toHaveBeenCalledWith({
        username: "john",
        password: "password123",
    });
    });

    it("shows a submitting state while login is in progress", async () => {
    const user = userEvent.setup();

    let resolveSubmit: () => void = () => {};

    const onSubmit = jest.fn(
        () =>
        new Promise<void>((resolve) => {
            resolveSubmit = resolve;
        }),
    );

    render(<LoginForm onSubmit={onSubmit} />);

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
        screen.getByRole("button", {
        name: /signing in/i,
        }),
    ).toBeDisabled();

    resolveSubmit();
    });
});