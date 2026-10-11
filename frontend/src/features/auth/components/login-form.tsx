"use client";

import { FormEvent, useState } from "react";

interface LoginFormProps {
  onSubmit: (data: {
    username: string;
    password: string;
  }) => Promise<void>;
}

const labelClass =
  "mb-2 block text-sm font-medium text-[#2A3046] dark:text-[#C9CEE0]";

const inputClass =
  "block h-11 w-full rounded-lg border border-[#DDE1EC] bg-white px-3.5 text-[15px] " +
  "text-[#0E1220] outline-none transition-[border-color,box-shadow] " +
  "hover:border-[#C3C9DA] " +
  "focus:border-[#3B4BFF] focus:ring-4 focus:ring-[#3B4BFF]/15 " +
  "disabled:cursor-not-allowed disabled:opacity-60 " +
  "dark:border-[#252A3A] dark:bg-[#10131D] dark:text-[#EEF0F8] " +
  "dark:hover:border-[#343B52] dark:focus:border-[#8E9AFF] dark:focus:ring-[#8E9AFF]/20";

export default function LoginForm({
  onSubmit,
}: LoginFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!event.currentTarget.checkValidity()) {
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit({
        username,
        password,
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label htmlFor="username" className={labelClass}>
          Username
        </label>
        <input
          id="username"
          name="username"
          type="text"
          autoComplete="username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          disabled={isSubmitting}
          required
          className={inputClass}
        />
      </div>

      <div>
        <label htmlFor="password" className={labelClass}>
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          disabled={isSubmitting}
          required
          className={inputClass}
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="mt-2 flex h-11 w-full items-center justify-center rounded-lg bg-[#3B4BFF] text-[15px] font-medium text-white transition hover:bg-[#2F3EE6] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[#3B4BFF]/30 active:bg-[#2735CC] disabled:cursor-not-allowed disabled:opacity-70 dark:bg-[#4A58FF] dark:hover:bg-[#5B68FF]"
      >
        {isSubmitting ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}