# Karaoke

Karaoke is a web application designed for listening to music on YouTube.

It allows users to clip specific sections of karaoke streams on YouTube and play those clipped parts.

Karaoke utilizes a simple model to predict the singing sections of the stream, making the clipping process easier for users.

## Training model

Before training model, make sure environment is ready.

```base
cd api
make prepare
make train
```

## Start services

Open two terminal, one for backend another for front-end.

```base
cd api
make migrate
make dev
```

```base
cd web
npm install
npm run dev
```
