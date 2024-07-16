# syntax = docker/dockerfile:1.3

FROM docker.io/node:18-slim

EXPOSE 5173

USER node
RUN mkdir /home/node/ui
WORKDIR /home/node/ui/
COPY --chown=node:node ./ui/package.json ./ui/package-lock.json /home/node/ui/.
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --include=dev

ENV PATH ./node_modules/.bin/:$PATH

ENTRYPOINT ["npm", "run", "dev"]
