"use client";

import Link from "next/link";
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
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#F7F8FB] px-6 py-16 text-[#0E1220] dark:bg-[#0A0C14] dark:text-[#EEF0F8]">
      {/* Dot grid that fades out toward the edges */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 [background-image:radial-gradient(#C9CEDD_1px,transparent_1px)] [background-size:22px_22px] [mask-image:radial-gradient(ellipse_60%_55%_at_50%_42%,black,transparent)] dark:[background-image:radial-gradient(#242A3D_1px,transparent_1px)]"
      />

      <div className="relative w-full max-w-[22rem]">
        <div
          aria-hidden
          className="mb-8 flex h-11 w-11 items-center justify-center rounded-xl bg-[#3B4BFF] text-white"
        >
          <svg
            viewBox="0 0 24 24"
            className="h-6 w-6"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-7l-4 3.5V16H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
            <path d="M8.5 9.5h7M8.5 12.5h4" />
          </svg>
        </div>

        <h1 className="text-[2.5rem] font-semibold leading-none tracking-[-0.035em]">
          Sign in
        </h1>
        <p className="mb-8 mt-3 text-[15px] text-[#5E657C] dark:text-[#8C93AB]">
          Welcome back. Your conversations are right where you left them.
        </p>

        {error && (
          <p
            role="alert"
            className="mb-5 rounded-lg border-l-[3px] border-[#D93A3A] bg-[#FDECEC] px-4 py-3 text-sm text-[#9B2222] dark:bg-[#2A1215] dark:text-[#F4A3A3]"
          >
            {error}
          </p>
        )}

        {success && (
          <p
            role="status"
            className="mb-5 rounded-lg border-l-[3px] border-[#1E9E6A] bg-[#E8F7F0] px-4 py-3 text-sm text-[#146B48] dark:bg-[#0F2A20] dark:text-[#8BD9B5]"
          >
            Signed in successfully.
          </p>
        )}

        <LoginForm onSubmit={handleSubmit} />

        <p className="mt-8 text-sm text-[#5E657C] dark:text-[#8C93AB]">
          New here?{" "}
          <Link
            href="/register"
            className="font-medium text-[#3B4BFF] underline-offset-4 hover:underline dark:text-[#8E9AFF]"
          >
            Create an account
          </Link>
        </p>
      </div>
    </main>
  );
}