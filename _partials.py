# Fragments partagés entre les pages du site SMART BIKER.
# Les coordonnées et le menu viennent de content/site.yml.
import blocks
SITE = blocks.SITE
TEL = SITE["telephone"]
TEL_RAW = SITE["telephone_lien"]

def head(title, desc, canon, extra="", og_img="remorque-porte-moto-attelee-sur-route"):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="REMORQU &amp; CO">
<meta name="geo.region" content="FR-87">
<meta name="geo.placename" content="Limoges">
<meta name="theme-color" content="#e63935">

<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="SMART BIKER France">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://smartbiker-france.fr/assets/img/{og_img}.jpg">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="900">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://smartbiker-france.fr/assets/img/{og_img}.jpg">

<link rel="icon" href="assets/img/logo-smart-biker.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,600;0,700;0,800;1,600;1,700;1,800&family=Figtree:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add("js");</script>
{extra}'''

def header(page=""):
    def cur(p): return ' aria-current="page"' if p == page else ''
    liens = "\n".join(
        '    <a href="%s"%s>%s</a>'
        % (m["lien"], cur(m["texte"].lower().replace("é", "e")), m["texte"])
        for m in SITE["menu"])
    baseline = SITE["baseline"]
    return f'''<a href="#main" class="skip">Aller au contenu</a>

<div class="topbar">
  <div class="wrap topbar-in">
    <a href="index.html" class="logo" aria-label="SMART BIKER France, accueil">
      <img src="assets/img/logo-smart-biker.svg" width="38" height="54" alt="" aria-hidden="true">
      <span class="w">SMART<i>BIKER</i><span class="rouge">-FRANCE</span></span>
    </a>
    <div class="right">
      <a class="tel" href="tel:{TEL_RAW}">{TEL}</a>
      <button class="themebtn" id="themebtn" type="button" aria-label="Changer de thème">&#9680;</button>
      <a class="btn sm" href="devis.html">Devis gratuit</a>
    </div>
  </div>
</div>

<nav class="redbar" aria-label="Navigation principale">
  <div class="wrap redbar-in">
    <span class="tag">{baseline}</span>
{liens}
  </div>
</nav>
'''

FOOTER = f'''<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a href="index.html" class="logo" style="margin-bottom:16px">
          <img src="assets/img/logo-smart-biker.svg" width="38" height="54" alt="" aria-hidden="true">
          <span class="w">SMART<i>BIKER</i><span class="rouge">-FRANCE</span></span>
        </a>
        <p style="font-size:15px;max-width:42ch">
          La remorque porte-moto abaissable, pliable et ultra compacte, distribuée en exclusivité en France
          par REMORQU &amp; CO. Livrée chez vous déjà montée, partout en France métropolitaine.
        </p>
      </div>
      <div>
        <h3>Le produit</h3>
        <ul>
          <li><a href="index.html#chargement">Charger sa moto seul</a></li>
          <li><a href="index.html#rangement">Le rangement vertical</a></li>
          <li><a href="index.html#coloris">Les 4 coloris</a></li>
          <li><a href="index.html#technique">Caractéristiques techniques</a></li>
          <li><a href="index.html#comparatif">Comparatif des remorques</a></li>
          <li><a href="index.html#prix">Prix et options</a></li>
          <li><a href="galerie.html">Photos et vidéos</a></li>
        </ul>
      </div>
      <div>
        <h3>REMORQU &amp; CO</h3>
        <address>
          Distributeur exclusif en France<br>
          28 rue Nicolas Appert<br>
          87280 Limoges<br>
          <a href="tel:{TEL_RAW}">{TEL}</a><br>
          <a href="https://remorqueco.fr">remorqueco.fr</a>
        </address>
        <p style="font-size:14.5px;margin-top:14px">
          Agences de retrait&#8239;: Limoges (87), La Souterraine (23), Angoulême (16).
        </p>
      </div>
    </div>
    <div class="foot-legal">
      <span>© 2026 REMORQU &amp; CO</span>
      <a href="mentions-legales.html">Mentions légales</a>
      <a href="confidentialite.html">Confidentialité</a>
    </div>
  </div>
</footer>

<div class="mobilebar">
  <a class="btn" href="devis.html">Devis gratuit</a>
  <a class="btn ghost" href="tel:{TEL_RAW}">Appeler</a>
</div>

<script src="assets/js/main.js" defer></script>'''

def pic(slug, alt, cls="", w=1600, h=900, lazy=True, sizes="100vw", big=True, fw=1600):
    """Balise <picture> avec WebP + JPEG et jeu de tailles."""
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    if big:
        srcw = f'srcset="assets/img/{slug}-900.webp 900w, assets/img/{slug}.webp {fw}w" sizes="{sizes}"'
        srcj = f'srcset="assets/img/{slug}-900.jpg 900w, assets/img/{slug}.jpg {fw}w" sizes="{sizes}"'
    else:
        srcw = f'srcset="assets/img/{slug}-900.webp"'
        srcj = f'srcset="assets/img/{slug}-900.jpg"'
    return (f'<picture>'
            f'<source type="image/webp" {srcw}>'
            f'<img src="assets/img/{slug}-900.jpg" {srcj} width="{w}" height="{h}" {load} alt="{alt}">'
            f'</picture>')

PILLARS = [
    ("fiabilité", "Châssis galvanisé, homologué",
     '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>'),
    ("simplicité", "Trois gestes, aucun outil",
     '<path d="M14.7 6.3a4 4 0 0 0 5.3 5.3l-8 8a2.8 2.8 0 0 1-4-4l8-8z"/><path d="M14.7 6.3 18 3l3 3-3.3 3.3"/>'),
    ("autonomie", "Une seule personne suffit",
     '<circle cx="12" cy="5.5" r="2.8"/><path d="M12 8.5v8M8 12h8M9.5 21l2.5-4.5L14.5 21"/>'),
    ("sécurité", "10 points d\'arrimage, verrouillage",
     '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V7a3.5 3.5 0 0 1 7 0v3.5"/><circle cx="12" cy="15.5" r="1.3"/>'),
    ("compact", "2 m de haut, 1 m² au sol",
     '<path d="M4 20V8l8-5 8 5v12"/><path d="M9 20v-6h6v6"/><path d="M2 20h20"/>'),
]

def pillars_html():
    out = ['<div class="pillars rv">']
    for name, sub, path in PILLARS:
        out.append(f'''  <div class="pillar">
    <div class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{path}</svg></div>
    <span>{name}</span><small>{sub}</small>
  </div>''')
    out.append('</div>')
    return "\n".join(out)
