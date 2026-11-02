#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les pages du site SMART BIKER France."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _partials import head, header, FOOTER, pic, pillars_html, TEL, TEL_RAW

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://smartbiker-france.fr"

def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("%-26s %6d octets" % (name, len(html)))

def page(name, title, desc, canon, body, ld="", nav=""):
    write(name, "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n"
          + head(title, desc, canon, ld) + "\n</head>\n\n<body>\n"
          + header(nav) + "\n<main id=\"main\">\n" + body
          + "\n</main>\n\n" + FOOTER + "\n</body>\n</html>\n")

# ===========================================================================
#  DONNÉES  (tout le contenu vit dans content/, modifiable depuis /admin)
# ===========================================================================
import medias
medias.preparer()

import blocks
from blocks import SITE, T, Tb, pic as bpic

ACC       = blocks.charger("accueil.yml")
GAL       = blocks.charger("galerie.yml")
PRIX      = SITE["prix"]
LIVRAISON = SITE["livraison"]
AGENCES   = [(a["ville"], a["departement"], a["adresse"]) for a in SITE["agences"]]
COLORIS   = [(c["nom"], c["couleur"]) for c in SITE["coloris"]]
FAQ       = [(T(q["question"]), T(q["reponse"]))
             for q in blocks.charger("faq.yml")["questions"]]

def faq_html():
    out = ['<div class="faq rv">']
    for i, (q, a) in enumerate(FAQ):
        op = " open" if i == 0 else ""
        out.append('  <details%s><summary>%s</summary><div class="ans"><p>%s</p></div></details>' % (op, q, a))
    out.append('</div>')
    return "\n".join(out)

def faq_ld():
    return ",\n".join(
        '        { "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }'
        % (q.replace("&#8239;", " ").replace('"', "'"), a.replace('"', "'"))
        for q, a in FAQ)

# ===========================================================================
#  SCHÉMA ANIMÉ
# ===========================================================================
HATCH = "".join(
    '<line x1="%d" y1="252" x2="%d" y2="262"/>' % (x, x - 10) for x in range(30, 541, 30))

FIG = '''<figure class="fig rv">
  <div class="fig-head">
    <span class="fig-title">Schéma de fonctionnement · profil</span>
    <span class="fig-title" id="stagenum">01 / 03</span>
  </div>
  <svg viewBox="0 20 560 270" role="img" aria-labelledby="figtitle figdesc">
    <title id="figtitle">Mécanisme d'abaissement de la remorque porte-moto SMART BIKER</title>
    <desc id="figdesc">Vue de profil, véhicule tracteur à gauche. Trois positions : plateau basculé vers l'arrière jusqu'au sol pour le chargement, plateau relevé et verrouillé pour la route, remorque dressée à la verticale sur son extrémité arrière pour le rangement.</desc>

    <line class="sv-ground" x1="20" y1="252" x2="540" y2="252"/>
    <g class="sv-thin" opacity=".45">''' + HATCH + '''</g>

    <g id="whole" style="transform-origin:358px 252px">

      <!-- timon repliable : tête d'attelage et béquille -->
      <g id="draw" style="transform-origin:152px 212px">
        <path class="sv-line" d="M152 212 L69 201"/>
        <circle class="sv-line" cx="62" cy="200" r="7"/>
        <path class="sv-thin" d="M152 217 L99 208"/>
        <path class="sv-thin" d="M96 205 L96 245 M86 245 L106 245"/>
      </g>

      <!-- châssis fixe, jusqu'à l'axe de basculement -->
      <path class="sv-line" d="M152 212 L175 214"/>

      <!-- roue et garde-boue, en dehors du châssis -->
      <circle class="sv-thin" cx="250" cy="228" r="24"/>
      <circle class="sv-fill" cx="250" cy="228" r="4"/>
      <path class="sv-thin" d="M250 228 L228 214 M250 228 L272 214"/>

      <!-- partie basse : elle bascule vers l'arrière et se pose au sol -->
      <g id="bed" style="transform-origin:175px 214px">
        <path class="sv-acc" d="M175 214 L340 214"/>
        <path class="sv-acc" d="M340 214 L358 221"/>
        <path class="sv-thin" d="M188 220 L334 220"/>
        <path class="sv-acc" d="M186 214 L186 190 M199 214 L199 190 M186 190 L199 190"/>
        <path class="sv-thin" d="M232 214 L232 207 M272 214 L272 207 M312 214 L312 207"/>
      </g>
      <circle class="sv-accfill" cx="175" cy="214" r="5"/>

      <!-- la moto -->
      <g id="bike" style="transform-origin:175px 214px">
        <circle class="sv-line" cx="192" cy="197" r="17"/>
        <circle class="sv-line" cx="290" cy="197" r="17"/>
        <path class="sv-line" d="M290 197 L254 186"/>
        <path class="sv-line" d="M254 186 L248 167 L219 165"/>
        <path class="sv-line" d="M219 165 L209 183 L205 196"/>
        <path class="sv-line" d="M219 165 L205 152"/>
        <path class="sv-line" d="M205 152 L192 197"/>
        <path class="sv-line" d="M213 147 L195 154"/>
        <path class="sv-line" d="M248 167 L240 156 L223 155 L219 165"/>
        <path class="sv-line" d="M275 167 L248 165"/>
        <path class="sv-thin" d="M280 203 L242 197"/>
      </g>
    </g>

    <g id="dim-vert" opacity="0">
      <path class="sv-dim" d="M352 46 L352 252"/>
      <path class="sv-dim" d="M344 46 L360 46 M344 252 L360 252"/>
      <text class="sv-txt" x="308" y="152">2 m</text>
    </g>
  </svg>
  <div class="stagebtns" role="group" aria-label="Positions de la remorque">
    <button class="stagebtn" type="button" data-stage="0" aria-pressed="true">Abaissée<small>chargement</small></button>
    <button class="stagebtn" type="button" data-stage="1" aria-pressed="false">Relevée<small>route</small></button>
    <button class="stagebtn" type="button" data-stage="2" aria-pressed="false">Pliée<small>rangement</small></button>
  </div>
  <figcaption class="fig-cap" id="figcap">La partie basse bascule vers l'arrière et vient toucher le sol.</figcaption>
</figure>'''

# ===========================================================================
#  ACCUEIL
# ===========================================================================
LD_ACCUEIL = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "@id": "''' + BASE + '''/#produit",
      "name": "Remorque porte-moto abaissable et pliable SMART BIKER",
      "alternateName": "SMART BIKER 1",
      "description": "Remorque porte-moto abaissable, pliable et ultra compacte permettant de charger une moto seul, sans rampe et sans aide. Le plateau se pose au sol, la moto se cale dans le bloque-roue avant, puis le plateau se relève et se verrouille. Une fois pliée, la remorque se range verticalement sur 2 m de haut.",
      "image": [
        "''' + BASE + '''/assets/img/remorque-porte-moto-abaissable-sur-route.jpg",
        "''' + BASE + '''/assets/img/remorque-porte-moto-abaissable-blanche.jpg",
        "''' + BASE + '''/assets/img/remorque-porte-moto-pliee-rangement-vertical-900.jpg"
      ],
      "brand": { "@type": "Brand", "name": "SMART BIKER" },
      "category": "Remorque porte-moto",
      "sku": "SMARTBIKER-1",
      "color": "Blanc, noir, orange, bleu",
      "material": "Acier galvanisé",
      "offers": {
        "@type": "Offer",
        "url": "''' + BASE + '''/",
        "priceCurrency": "EUR",
        "price": "1990",
        "priceValidUntil": "2027-12-31",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "seller": { "@id": "''' + BASE + '''/#entreprise" },
        "areaServed": { "@type": "Country", "name": "France" },
        "shippingDetails": {
          "@type": "OfferShippingDetails",
          "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "FR" },
          "shippingRate": { "@type": "MonetaryAmount", "value": "200", "currency": "EUR" }
        }
      },
      "additionalProperty": [
        { "@type": "PropertyValue", "name": "PTAC", "value": "450 kg" },
        { "@type": "PropertyValue", "name": "Charge utile", "value": "325 kg" },
        { "@type": "PropertyValue", "name": "Empattement maximum", "value": "1650 mm" },
        { "@type": "PropertyValue", "name": "Dimensions", "value": "248 x 188 x 60 cm" },
        { "@type": "PropertyValue", "name": "Hauteur de rangement vertical", "value": "2 m" },
        { "@type": "PropertyValue", "name": "Roues", "value": "195/55 R10C" },
        { "@type": "PropertyValue", "name": "Chargement sans rampe", "value": "Oui" }
      ]
    },
    {
      "@type": "AutoPartsStore",
      "@id": "''' + BASE + '''/#entreprise",
      "name": "REMORQU & CO — SMART BIKER France",
      "description": "Distributeur exclusif en France de la remorque porte-moto abaissable SMART BIKER. Agences à Limoges, La Souterraine et Angoulême.",
      "url": "''' + BASE + '''/",
      "telephone": "''' + TEL_RAW + '''",
      "priceRange": "€€",
      "image": "''' + BASE + '''/assets/img/remorque-porte-moto-abaissable-sur-route.jpg",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "28 rue Nicolas Appert",
        "addressLocality": "Limoges",
        "postalCode": "87280",
        "addressCountry": "FR"
      },
      "areaServed": { "@type": "Country", "name": "France" }
    },
    {
      "@type": "FAQPage",
      "@id": "''' + BASE + '''/#faq",
      "mainEntity": [
''' + faq_ld() + '''
      ]
    },
    {
      "@type": "WebSite",
      "@id": "''' + BASE + '''/#site",
      "url": "''' + BASE + '''/",
      "name": "SMART BIKER France",
      "inLanguage": "fr-FR",
      "publisher": { "@id": "''' + BASE + '''/#entreprise" }
    }
  ]
}
</script>
'''

agences_html = "\n".join(
    '    <div class="agence"><b>%s</b><span>%s</span><p>%s</p></div>' % (v, d, a)
    for v, d, a in AGENCES)

coloris_html = "\n".join(
    '    <div class="colorchip"><div class="sw" style="background:%s"></div><b>%s</b></div>' % (c, n)
    for n, c in COLORIS)

ACCUEIL = "\n\n".join([
    blocks.hero_html(ACC["hero"]),
    blocks.chiffres_html(ACC["chiffres"]),
    blocks.rendre_sections(ACC["sections"], {"FIG": FIG}),
])

page("index.html",
     Tb(ACC["meta"]["titre"]),
     Tb(ACC["meta"]["description"]),
     BASE + "/", ACCUEIL, LD_ACCUEIL, "accueil")

# ===========================================================================
#  GALERIE
# ===========================================================================
PHOTOS = [
 # --- studio, fond blanc : le produit ---------------------------------
 ("smart-biker-blanche-trois-quarts", "Remorque porte-moto abaissable SMART BIKER blanche, vue de trois quarts, sur fond blanc", "Blanche, de trois quarts", True),
 ("smart-biker-noire-trois-quarts", "Remorque porte-moto abaissable SMART BIKER noire, vue de trois quarts, sur fond blanc", "Noire, de trois quarts", True),
 ("smart-biker-noire-plateau-au-sol", "Remorque porte-moto SMART BIKER noire, plateau abaissé au sol", "Plateau au sol", True),
 ("smart-biker-blanche-plateau-abaisse", "Remorque porte-moto SMART BIKER blanche, plateau abaissé et bloque-roue avant", "Le bloque-roue", True),
 ("smart-biker-blanche-vue-arriere-studio", "Remorque porte-moto SMART BIKER blanche vue de l'arrière, sur fond blanc", "Blanche, de l'arrière", True),
 ("smart-biker-noire-vue-arriere", "Remorque porte-moto SMART BIKER noire vue de l'arrière, plateau et feux", "Noire, de l'arrière", True),
 ("smart-biker-noire-profil", "Remorque porte-moto SMART BIKER noire vue de profil", "De profil", True),
 ("smart-biker-blanche-pliee", "Remorque porte-moto SMART BIKER blanche pliée, prête à être dressée", "Pliée", True),
 # --- le chargement, en conditions réelles ----------------------------
 ("remorque-porte-moto-plateau-pose-au-sol", "Plateau de la remorque porte-moto SMART BIKER posé au sol derrière une voiture", "Le plateau au sol", True),
 ("charger-sa-moto-seul-remorque-abaissee", "Un homme charge seul un BMW GS sur la remorque porte-moto abaissée", "Charger seul, sans rampe", True),
 ("bloque-roue-avant-moto-remorque", "Roue avant d'une BMW GS calée dans le bloque-roue de la remorque", "La roue calée", True),
 ("remorque-porte-moto-chargee-plein-ciel", "BMW GS sanglé sur la remorque porte-moto SMART BIKER, prêt à partir", "Prête à partir", True),
 # --- sur la route ----------------------------------------------------
 ("remorque-porte-moto-attelee-sur-route", "Remorque porte-moto SMART BIKER attelée et chargée d'un roadster, sur la route", "Sur la route", True),
 ("convoi-remorques-porte-moto-livraison", "Deux voitures tractant des remorques porte-moto SMART BIKER chargées", "Deux attelages", True),
 ("trois-motos-remorques-porte-moto", "Trois motos chargées sur des remorques porte-moto SMART BIKER", "Trois motos, trois remorques", True),
 # --- toutes les motos -------------------------------------------------
 ("moto-chargee-remorque-blanche-atelier", "Roadster BMW chargé sur une remorque porte-moto SMART BIKER blanche", "Un roadster", True),
 ("roadster-charge-remorque-smart-biker", "Roadster sanglé sur la remorque porte-moto SMART BIKER", "Sanglé, prêt", True),
 ("mains-sur-le-bloque-roue-remorque", "Réglage du bloque-roue avant de la remorque porte-moto SMART BIKER", "Le bloque-roue réglable", True),
 ("remorque-porte-moto-grosse-cylindree-trail", "Gros trail routier chargé sur la remorque porte-moto SMART BIKER", "Un gros trail", True),
 ("remorque-porte-moto-moto-roadster", "Roadster chargé sur la remorque porte-moto SMART BIKER", "Un roadster sportif", True),
 ("remorque-porte-moto-scooter-3-roues-kit-mp3", "Scooter à trois roues sur la remorque SMART BIKER avec kit MP3", "Un scooter 3 roues", True),
 ("chargement-moto-custom-remorque-abaissable", "Chargement d'un custom sur la remorque porte-moto abaissable", "Un custom", False),
 # --- les coloris livrés ----------------------------------------------
 ("smart-biker-coloris-blanc-studio", "Remorque porte-moto abaissable SMART BIKER blanche sur fond blanc", "Coloris blanc", False),
 ("smart-biker-coloris-noir-studio", "Remorque porte-moto abaissable SMART BIKER noire sur fond blanc", "Coloris noir", False),
 ("smart-biker-coloris-orange-studio", "Remorque porte-moto abaissable SMART BIKER orange sur fond blanc", "Coloris orange", False),
 ("smart-biker-coloris-bleu-studio", "Remorque porte-moto abaissable SMART BIKER bleue sur fond blanc", "Coloris bleu", False),
 ("smart-biker-orange-trois-quarts", "Remorque porte-moto SMART BIKER orange livrée, vue de trois quarts", "Une orange livrée", False),
 ("smart-biker-coloris-bleu", "Remorque porte-moto SMART BIKER bleue livrée", "Une bleue livrée", False),
 ("remorques-porte-moto-orange-et-bleue", "Remorques porte-moto SMART BIKER orange et bleue côte à côte", "Orange et bleue", False),
 # --- rangement --------------------------------------------------------
 ("remorque-porte-moto-pliee-rangement-vertical", "Remorque porte-moto SMART BIKER pliée et dressée à la verticale", "Dressée contre un mur", False),
]
OPTIONS_PHOTOS = [
 ("option-antivol-permanent", "Antivol permanent pour remorque porte-moto", "Antivol permanent"),
 ("option-antivol-de-tete", "Antivol de tête d'attelage pour remorque porte-moto", "Antivol de tête"),
 ("option-sangles-retractables", "Sangles rétractables automatiques pour l'arrimage de la moto", "Sangles rétractables"),
 ("option-sangle-roue-arriere", "Sangle d'arrimage pour la roue arrière de la moto", "Sangle roue arrière"),
]

def gal(items, sizes="(max-width:700px) 50vw, 25vw"):
    out = ['<div class="gallery">']
    for it in items:
        slug, alt, cap = it[0], it[1], it[2]
        big = it[3] if len(it) > 3 else False
        slug = blocks.slug_of(slug)
        full = "assets/img/%s.jpg" % slug if big else "assets/img/%s-900.jpg" % slug
        CUT = {"smart-biker-blanche-trois-quarts","smart-biker-noire-trois-quarts",
               "smart-biker-noire-plateau-au-sol","smart-biker-blanche-plateau-abaisse",
               "smart-biker-blanche-vue-arriere-studio","smart-biker-noire-vue-arriere",
               "smart-biker-noire-profil","smart-biker-blanche-pliee",
               "smart-biker-coloris-blanc-studio","smart-biker-coloris-noir-studio",
               "smart-biker-coloris-orange-studio","smart-biker-coloris-bleu-studio"}
        cls = " cut" if slug in CUT else ""
        out.append('  <figure class="rv%s"><button class="zoomable" type="button" data-full="%s">%s</button>'
                   '<figcaption>%s</figcaption></figure>'
                   % (cls, full, pic(slug, alt, sizes=sizes, big=big), cap))
    out.append('</div>')
    return "\n".join(out)

GALERIE = '''
<section>
  <div class="wrap">
    <span class="kicker rv">Galerie</span>
    <h1 class="rv" style="margin-top:20px">La remorque porte-moto abaissable en images</h1>
    <p class="lede rv">Le mécanisme d'abaissement, le bloque-roue, l'attelage, les quatre coloris et le rangement
    vertical. Toutes les photos sont celles de la SMART BIKER livrée en France. Cliquez pour agrandir.</p>
    <div class="cta-row rv">
      <a class="btn" href="devis.html">Demander un devis</a>
      <a class="btn ghost" href="index.html#technique">Voir la fiche technique</a>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="sec-k rv">La vidéo</p>
    <h2 class="rv">La démonstration complète</h2>
    <div class="videoblock rv" style="margin-top:28px">
      <video controls preload="none" playsinline poster="assets/video/poster-demo.jpg"
             aria-label="Vidéo de démonstration de la remorque porte-moto abaissable SMART BIKER">
        <source src="assets/video/demo-smart-biker.mp4" type="video/mp4">
        Votre navigateur ne peut pas lire cette vidéo.
      </video>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <p class="sec-k rv">Le produit</p>
    <h2 class="rv">La remorque sous tous les angles</h2>
''' + gal(PHOTOS) + '''
  </div>
</section>

<section>
  <div class="wrap">
    <p class="sec-k rv">Les options</p>
    <h2 class="rv">Antivols et arrimage</h2>
    <p class="lede rv">Les accessoires disponibles à la commande, pour sécuriser la remorque et la moto.</p>
''' + gal(OPTIONS_PHOTOS, sizes="(max-width:700px) 50vw, 25vw") + '''
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="sec-k rv">Devis gratuit</p>
    <h2 class="rv">Une question sur votre moto&#8239;?</h2>
    <p class="rv">Dites-nous le modèle et votre département, nous vous indiquons le prix final et le délai.</p>
    <div class="cta-row rv">
      <a class="btn white" href="devis.html">Demander un devis</a>
      <a class="btn outlight" href="tel:''' + TEL_RAW + '''">''' + TEL + '''</a>
    </div>
  </div>
</section>
'''

page("galerie.html",
     "Remorque porte-moto abaissable en photos | SMART BIKER France",
     "Photos de la remorque porte-moto abaissable SMART BIKER : mécanisme d'abaissement, chargement sans rampe, rangement vertical, quatre coloris et options d'arrimage.",
     BASE + "/galerie/", GALERIE, "", "galerie")

# ===========================================================================
#  DEVIS
# ===========================================================================
LD_DEVIS = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Demande de devis — remorque porte-moto SMART BIKER",
  "url": "''' + BASE + '''/devis/",
  "mainEntity": {
    "@type": "AutoPartsStore",
    "name": "REMORQU & CO — SMART BIKER France",
    "telephone": "''' + TEL_RAW + '''",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "28 rue Nicolas Appert",
      "addressLocality": "Limoges",
      "postalCode": "87280",
      "addressCountry": "FR"
    },
    "areaServed": { "@type": "Country", "name": "France" }
  }
}
</script>
'''

coloris_radios = "\n".join(
    '          <label><input type="radio" name="coloris" value="%s"%s> %s</label>' %
    (n, ' checked' if i == 0 else '', n) for i, (n, c) in enumerate(COLORIS))

DEVIS = '''
<section>
  <div class="wrap">
    <span class="kicker rv">Devis gratuit · réponse sous 24 h</span>
    <h1 class="rv" style="margin-top:20px">Demandez votre devis</h1>
    <p class="lede rv">Dites-nous votre moto et votre département. Nous vous indiquons le prix final, options
    comprises, et le délai. Sans engagement.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap two top">
    <form class="form rv" id="devisForm" data-mode="mailto" method="post" action="#" novalidate>
      <div class="fieldrow">
        <div class="field">
          <label for="nom">Nom et prénom <span class="required">*</span></label>
          <input type="text" id="nom" name="nom" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="tel">Téléphone <span class="required">*</span></label>
          <input type="tel" id="tel" name="tel" autocomplete="tel" required>
        </div>
      </div>

      <div class="fieldrow">
        <div class="field">
          <label for="email">E-mail <span class="required">*</span></label>
          <input type="email" id="email" name="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="cp">Code postal <span class="required">*</span></label>
          <p class="help">Pour le délai et le mode de retrait</p>
          <input type="text" id="cp" name="cp" inputmode="numeric" pattern="[0-9]{5}" autocomplete="postal-code" required>
        </div>
      </div>

      <div class="field">
        <label for="moto">Votre moto</label>
        <p class="help">Marque et modèle, pour vérifier l'empattement</p>
        <input type="text" id="moto" name="moto" placeholder="Ex. : trail 1000, custom, scooter 3 roues">
      </div>

      <div class="field">
        <label for="livraison">Retrait ou livraison</label>
        <select id="livraison" name="livraison">
          <option>Retrait à Limoges (87) — ''' + PRIX + ''' € TTC</option>
          <option>Retrait à La Souterraine (23) — ''' + PRIX + ''' € TTC</option>
          <option>Retrait à Angoulême (16) — ''' + PRIX + ''' € TTC</option>
          <option>Livraison chez moi — ''' + PRIX + ''' € + ''' + LIVRAISON + ''' € TTC</option>
          <option>Je ne sais pas encore</option>
        </select>
      </div>

      <div class="field">
        <label>Coloris souhaité</label>
        <div class="checks">
''' + coloris_radios + '''
        </div>
      </div>

      <div class="field">
        <label>Options souhaitées</label>
        <div class="checks">
          <label><input type="checkbox" name="options" value="Kit MP3"> Kit MP3</label>
          <label><input type="checkbox" name="options" value="Jantes aluminium"> Jantes alu</label>
          <label><input type="checkbox" name="options" value="Kit antivol"> Antivol</label>
          <label><input type="checkbox" name="options" value="Sangles rétractables"> Sangles rétractables</label>
          <label><input type="checkbox" name="options" value="Roue de secours"> Roue de secours</label>
        </div>
      </div>

      <div class="field">
        <label for="message">Votre message</label>
        <textarea id="message" name="message" placeholder="Une question, une contrainte particulière…"></textarea>
      </div>

      <label class="consent">
        <input type="checkbox" name="consent" required>
        <span>J'accepte d'être recontacté par REMORQU &amp; CO au sujet de ma demande. Mes coordonnées ne seront
        ni revendues ni transmises à un tiers.</span>
      </label>

      <div class="cta-row">
        <button class="btn" type="submit">Envoyer ma demande</button>
        <a class="btn ghost" href="tel:''' + TEL_RAW + '''">Ou appelez le ''' + TEL + '''</a>
      </div>

      <p class="formnote" id="formResult" hidden></p>
      <p class="formnote">Champs marqués <span class="required">*</span> obligatoires. Réponse sous 24 heures ouvrées.</p>
    </form>

    <div class="rv">
      <h2>Ce que contient votre devis</h2>
      <ul class="bul">
        <li>Le prix final, options et coloris compris</li>
        <li>Le délai réel, en retrait agence ou en livraison</li>
        <li>La vérification que votre moto passe (empattement et poids)</li>
        <li>Les conditions de garantie et la disponibilité des pièces</li>
      </ul>

      <h2 style="margin-top:44px">Nous joindre</h2>
      <p><a class="tel" href="tel:''' + TEL_RAW + '''" style="font-size:24px">''' + TEL + '''</a><br>
      Du lundi au vendredi, 9 h – 18 h.</p>

      <h2 style="margin-top:44px">Nos agences</h2>
      <div class="agences">
''' + agences_html + '''
      </div>

      <h2 style="margin-top:44px">Professionnels</h2>
      <p>Concessions moto, loueurs, circuits et écoles de pilotage : conditions dédiées à partir de deux
      remorques. Précisez-le dans votre message.</p>
    </div>
  </div>
</section>
'''

page("devis.html",
     "Devis remorque porte-moto abaissable | SMART BIKER France",
     "Demandez votre devis gratuit pour la remorque porte-moto abaissable SMART BIKER. Réponse sous 24 h, retrait en agence ou livraison partout en France.",
     BASE + "/devis/", DEVIS, LD_DEVIS, "devis")

# ===========================================================================
#  PAGES LÉGALES
# ===========================================================================
def simple(name, title, h1, blocks, nav=""):
    body = '<section><div class="wrap"><span class="kicker">Informations</span>' \
           '<h1 style="margin-top:20px">%s</h1>%s</div></section>' % (h1, blocks)
    page(name, title + " | SMART BIKER France",
         "Informations légales du site SMART BIKER France, distribué par REMORQU & CO.",
         BASE + "/" + name.replace(".html", "") + "/", body, "", nav)

simple("mentions-legales.html", "Mentions légales", "Mentions légales", '''
<h2 style="margin-top:40px">Éditeur du site</h2>
<p>REMORQU &amp; CO — distributeur exclusif en France de la remorque SMART BIKER.<br>
28 rue Nicolas Appert, 87280 Limoges, France.<br>
Téléphone&#8239;: <a href="tel:''' + TEL_RAW + '''">''' + TEL + '''</a>.</p>
<p class="formnote">À compléter&#8239;: forme juridique, capital social, numéro SIRET, numéro de TVA
intracommunautaire, nom du directeur de la publication.</p>

<h2 style="margin-top:40px">Hébergement</h2>
<p class="formnote">À compléter&#8239;: nom, adresse et téléphone de l'hébergeur du site.</p>

<h2 style="margin-top:40px">Propriété intellectuelle</h2>
<p>L'ensemble des contenus de ce site — textes, photographies, schémas et marques — est la propriété de
REMORQU &amp; CO ou de ses partenaires. Toute reproduction sans autorisation écrite est interdite.</p>

<h2 style="margin-top:40px">Responsabilité</h2>
<p>Les caractéristiques techniques et les tarifs indiqués sont donnés à titre informatif et peuvent évoluer.
Seul le devis signé fait foi.</p>
''')

simple("confidentialite.html", "Politique de confidentialité", "Politique de confidentialité", '''
<h2 style="margin-top:40px">Données collectées</h2>
<p>Le formulaire de devis collecte votre nom, votre téléphone, votre e-mail, votre code postal et les
informations relatives à votre projet. Ces données servent uniquement à vous répondre.</p>

<h2 style="margin-top:40px">Conservation</h2>
<p>Les demandes de devis sont conservées trois ans à compter du dernier contact, puis supprimées.</p>

<h2 style="margin-top:40px">Destinataires</h2>
<p>Vos coordonnées ne sont ni revendues, ni louées, ni transmises à un tiers à des fins commerciales.</p>

<h2 style="margin-top:40px">Vos droits</h2>
<p>Vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition sur vos données.
Pour l'exercer, écrivez-nous ou appelez le <a href="tel:''' + TEL_RAW + '''">''' + TEL + '''</a>.</p>

<h2 style="margin-top:40px">Cookies</h2>
<p>Ce site ne dépose aucun cookie publicitaire ni de mesure d'audience. Seule une préférence d'affichage
(thème clair ou sombre) est enregistrée dans votre navigateur.</p>
''')

# ===========================================================================
#  CONSEILS  (articles, content/articles/*.md)
# ===========================================================================
CONS = blocks.charger("conseils.yml")
ARTICLES = blocks.charger_articles()

page("conseils.html",
     Tb(CONS["meta"]["titre"]), Tb(CONS["meta"]["description"]),
     BASE + "/conseils/",
     '''
<section>
  <div class="wrap">
    <span class="kicker rv">''' + T(CONS["kicker"]) + '''</span>
    <h1 class="rv" style="margin-top:20px">''' + T(CONS["titre"]) + '''</h1>
    <p class="lede rv">''' + T(CONS["chapo"]) + '''</p>
''' + blocks.liste_articles_html(ARTICLES) + '''
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="sec-k rv">Devis gratuit</p>
    <h2 class="rv">Une question sur votre moto ou votre véhicule&#8239;?</h2>
    <p class="rv">Dites-nous votre modèle et votre département, nous vous répondons sous 24 heures ouvrées.</p>
    <div class="cta-row rv">
      <a class="btn white" href="devis.html">Demander un devis</a>
      <a class="btn outlight" href="tel:''' + TEL_RAW + '''">Appeler le ''' + TEL + '''</a>
    </div>
  </div>
</section>
''', "", "conseils")

for _a in ARTICLES:
    _ld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "%s",
  "description": "%s",
  "datePublished": "%s",
  "inLanguage": "fr-FR",
  "author": { "@type": "Organization", "name": "REMORQU & CO" },
  "publisher": { "@id": "%s/#entreprise" },
  "mainEntityOfPage": "%s/conseils/%s/"
}
</script>''' % (_a["titre"].replace('"', "'"), _a.get("description", "").replace('"', "'"),
                _a.get("date", ""), BASE, BASE, _a["slug"])
    _img = ""
    if _a.get("image"):
        _img = ('<figure class="band rv" style="margin-top:0"><div class="shot r169">'
                + blocks.pic(_a["image"], _a.get("alt", ""), sizes="100vw") + '</div></figure>')
    page(_a["fichier"], Tb(_a["titre"]) + " | SMART BIKER France",
         Tb(_a.get("description", "")), BASE + "/conseils/" + _a["slug"] + "/",
         '''
<section>
  <div class="wrap narrow">
    <p class="sec-k rv"><a href="conseils.html">Conseils</a> · ''' + blocks.date_fr(_a.get("date", "")) + '''</p>
    <h1 class="rv">''' + T(_a["titre"]) + '''</h1>
    <p class="lede rv">''' + T(_a.get("resume", "")) + '''</p>
    ''' + _img + '''
    <div class="prose rv">
''' + _a["corps"] + '''
    </div>
    <div class="cta-row rv" style="margin-top:40px">
      <a class="btn" href="devis.html">Demander un devis</a>
      <a class="btn ghost" href="conseils.html">Tous les conseils</a>
    </div>
  </div>
</section>
''', _ld, "conseils")

# ===========================================================================
#  FICHIERS TECHNIQUES
# ===========================================================================
write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")

urls = [("/", "1.0", "monthly"), ("/galerie/", "0.7", "monthly"), ("/devis/", "0.8", "yearly"),
        ("/conseils/", "0.8", "weekly")]
urls += [("/conseils/%s/" % a["slug"], "0.6", "monthly") for a in ARTICLES]
urls += [("/mentions-legales/", "0.2", "yearly"), ("/confidentialite/", "0.2", "yearly")]
write("sitemap.xml",
      '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join('  <url><loc>%s%s</loc><priority>%s</priority><changefreq>%s</changefreq></url>\n' % (BASE, u, p, c)
                for u, p, c in urls)
      + '</urlset>\n')
