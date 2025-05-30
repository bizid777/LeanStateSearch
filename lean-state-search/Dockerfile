
FROM node:22-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm config set registry https://registry.npmmirror.com && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN yarn global add pnpm && pnpm build

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1


EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"
ENV MODE="docker"

CMD ["pnpm", "start"]