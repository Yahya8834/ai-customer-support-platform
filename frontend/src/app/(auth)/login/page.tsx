"use client";

import { useState } from "react";

import LoginForm from "@/features/auth/components/login-form";
import { loginUser } from "@/features/auth/services/auth-service";

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(data: {
    username: string;
    password: string;
  }) {
    setError(null);
    setSuccess(false);

    try {
      await loginUser(data);
      setSuccess(true);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to sign in.",
      );
    }
  }

  return (
    <main>
      <h1>Sign in</h1>

      {error && <p role="alert">{error}</p>}

      {success && (
        <p role="status">
          Signed in successfully.
        </p>
      )}

      <LoginForm onSubmit={handleSubmit} />
    </main>
  );
}