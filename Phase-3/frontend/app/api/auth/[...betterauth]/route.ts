import { NextRequest } from "next/server";
import { betterAuth } from "better-auth";

if (!process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET) {
  throw new Error("NEXT_PUBLIC_BETTER_AUTH_SECRET missing");
}

const auth = betterAuth({
  secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET,
  baseURL: process.env.NEXT_PUBLIC_API_BASE, // your backend
});

export const GET = (req: NextRequest) => auth.handler(req);
export const POST = (req: NextRequest) => auth.handler(req);
