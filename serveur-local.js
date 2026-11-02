// Petit serveur web local, sans aucune dépendance à télécharger.
// Il sert les fichiers de ce dossier pour que le back-office puisse s'ouvrir.
// Lancé automatiquement par TESTER-LE-BACK-OFFICE.bat.

const http = require("http");
const fs = require("fs");
const path = require("path");

const RACINE = __dirname;
const PORTS = [8090, 8091, 8092, 8093, 8094, 8095];

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".yml": "text/yaml; charset=utf-8",
  ".yaml": "text/yaml; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".svg": "image/svg+xml",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
};

const serveur = http.createServer((req, res) => {
  let rel;
  try {
    rel = decodeURIComponent(new URL(req.url, "http://x").pathname);
  } catch (e) {
    rel = "/";
  }
  if (rel.endsWith("/")) rel += "index.html";

  // on ne sort jamais du dossier
  const cible = path.join(RACINE, path.normalize(rel).replace(/^([/\\])+/, ""));
  if (!cible.startsWith(RACINE)) {
    res.writeHead(403).end("Interdit");
    return;
  }

  fs.stat(cible, (err, st) => {
    if (err || st.isDirectory()) {
      res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
      res.end("<h1>404</h1><p>Fichier introuvable : " + rel + "</p>");
      return;
    }
    res.writeHead(200, {
      "Content-Type": TYPES[path.extname(cible).toLowerCase()] || "application/octet-stream",
      "Content-Length": st.size,
      "Cache-Control": "no-store",
    });
    fs.createReadStream(cible).pipe(res);
  });
});

function essayer(i) {
  if (i >= PORTS.length) {
    console.log("");
    console.log("  Aucun port libre entre 8090 et 8095.");
    console.log("  Fermez les autres serveurs qui tournent, puis relancez.");
    return;
  }
  serveur.once("error", (e) => {
    if (e.code === "EADDRINUSE") return essayer(i + 1);
    console.log("  Erreur : " + e.message);
  });
  serveur.listen(PORTS[i], "127.0.0.1", () => {
    const port = PORTS[i];
    try {
      fs.writeFileSync(path.join(RACINE, "port.txt"), String(port));
    } catch (e) {}
    console.log("");
    console.log("  =========================================");
    console.log("   Serveur du site demarre.");
    console.log("");
    console.log("     Le site        http://localhost:" + port + "/");
    console.log("     Le back-office http://localhost:" + port + "/admin/");
    console.log("");
    console.log("   NE FERMEZ PAS cette fenetre pendant que");
    console.log("   vous travaillez.");
    console.log("  =========================================");
    console.log("");
  });
}

essayer(0);
