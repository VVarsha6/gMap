const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.header("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.sendStatus(200);
  next();
});

app.use(
  "/",
  createProxyMiddleware({
    target: "https://gmap-0emf.onrender.com",
    changeOrigin: true,
  })
);

app.listen(3001, () => console.log("✅ CORS proxy running on http://localhost:3001"));
