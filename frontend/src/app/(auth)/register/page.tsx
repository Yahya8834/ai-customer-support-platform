"use client";
import { useState } from "react";
import RegisterForm from "@/features/auth/components/register-form";
import { registerUser } from "@/features/auth/services/auth-service";



export default function RegisterPage() {
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(data: {
    username: string;
    email: string;
    password: string;
  }) {
    setError(null);
    setSuccess(false);

    try {
      await registerUser(data);
      setSuccess(true);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to create account.",
      );
    }
  }

  return (
    <main>
      <h1>Create account</h1>

      {error && <p role="alert">{error}</p>}

      {success && (
        <>
          <p role="status">
            Account created successfully.
          </p>

          <a href="/login">Sign in</a>
        </>
      )}

      <RegisterForm onSubmit={handleSubmit} />
    </main>
  );
}