# -*- coding: utf-8 -*-
"""
Moteur de rendu : transforme les fichiers de content/ en HTML.

Un bloc = un type + ses champs. Pour ajouter un nouveau type de bloc,
écrire une fonction b_<type>(bloc, ctx) et l'ajouter au dictionnaire BLOCS
tout en bas. Elle reçoit le bloc tel qu'il est dans le fichier YAML.
"""
import os, re, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))

def charger(nom):
    with open(os.path.join(ROOT, "content", nom), encoding="utf-8") as f:
        return yaml.safe_load(f)

SITE = charger("site.yml")

# --- Texte ------------------------------------------------------------------

_VARS = {
    "{prix}": SITE["prix"],
    "{livraison}": SITE["livraison"],
    "{tel}": SITE["telephone"],
    "{tel_lien}": SITE["telephone_lien"],
    "{email}": SITE["email"],
    "{entreprise}": SITE["entreprise"],
}

def T(s):
    """Remplace les variables et applique le gras et la mise en rouge."""
    if s is None:
        return ""
    s = str(s)
    for k, v in _VARS.items():
        s = s.replace(k, v)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r'<span class="rouge">\1</span>', s)
    return s

def Tb(s):
    """Variables seules, sans mise en forme (attributs, titres de page)."""
    if s is None:
        return ""
    s = str(s)
    for k, v in _VARS.items():
        s = s.replace(k, v)
    return s

# --- Images -----------------------------------------------------------------

def slug_of(v):
    """Accepte « assets/img/photo-900.jpg » comme « photo » et renvoie le slug."""
    v = str(v or "").replace("assets/img/", "").strip()
    v = re.sub(r"\.(jpe?g|png|webp)$", "", v, flags=re.I)
    return v[:-4] if v.endswith("-900") else v

def _existe(nom):
    return os.path.exists(os.path.join(ROOT, "assets", "img", nom))

def pic(slug, alt, w=1600, h=900, lazy=True, sizes="100vw", big=None, fw=None):
    """<picture> avec WebP, repli JPEG et jeu de tailles. big est déduit des
    fichiers réellement présents : inutile de le renseigner à la main."""
    slug = slug_of(slug)
    if big is None:
        big = _existe(slug + ".jpg")
    if fw is None:
        fw = 1600
        p = os.path.join(ROOT, "assets", "img", slug + ".jpg")
        if os.path.exists(p):
            try:
                from PIL import Image
                fw = Image.open(p).width
            except Exception:
                pass
    load = ('loading="lazy" decoding="async"' if lazy
            else 'fetchpriority="high" decoding="async"')
    if not _existe(slug + "-900.jpg"):
        # photo tout juste déposée, variantes pas encore fabriquées
        src = slug + (".jpg" if _existe(slug + ".jpg") else ".png")
        return ('<img src="assets/img/%s" width="%d" height="%d" %s alt="%s">'
                % (src, w, h, load, Tb(alt)))
    if big:
        srcw = ('srcset="assets/img/%s-900.webp 900w, assets/img/%s.webp %dw" sizes="%s"'
                % (slug, slug, fw, sizes))
        srcj = ('srcset="assets/img/%s-900.jpg 900w, assets/img/%s.jpg %dw" sizes="%s"'
                % (slug, slug, fw, sizes))
    else:
        srcw = 'srcset="assets/img/%s-900.webp"' % slug
        srcj = 'srcset="assets/img/%s-900.jpg"' % slug
    return ('<picture><source type="image/webp" %s>'
            '<img src="assets/img/%s-900.jpg" %s width="%d" height="%d" %s alt="%s"></picture>'
            % (srcw, slug, srcj, w, h, load, Tb(alt)))

_RATIOS = {"4/3": ("r43", 1600, 900), "16/9": ("r169", 1600, 900),
           "3/2": ("r32", 1400, 933), "3/4": ("r34", 900, 1201)}

def shot(p, format="4/3", zoom=False, sizes="100vw", extra=""):
    cls, w, h = _RATIOS.get(format, _RATIOS["4/3"])
    classes = "shot " + ("cut " if p.get("detouree") else "") + cls + (" zoom" if zoom else "")
    big = None
    if format == "3/4":
        big = False
    return ('<div class="%s"%s>%s</div>'
            % (classes.strip(), (' style="%s"' % extra) if extra else "",
               pic(p["image"], p.get("alt", ""), w=w, h=h, sizes=sizes, big=big)))

# --- Briques réutilisées ----------------------------------------------------

def puces(items, orange=False):
    cls = "bul or" if orange else "bul"
    return ('<ul class="%s">\n%s\n        </ul>'
            % (cls, "\n".join("          <li>%s</li>" % T(x) for x in items)))

def paras(items, first_no_margin=False):
    out = []
    for i, p in enumerate(items):
        st = ' style="margin-top:0"' if (first_no_margin and i == 0) else ""
        out.append("        <p%s>%s</p>" % (st, T(p)))
    return "\n".join(out)

# --- Les blocs --------------------------------------------------------------

def b_piliers(b, ctx):
    out = ['<div class="pillars rv">']
    for p in charger("piliers.yml")["piliers"]:
        out.append('  <div class="pillar">\n'
                   '    <div class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></div>\n'
                   '    <span>%s</span><small>%s</small>\n  </div>'
                   % (p["icone"], T(p["nom"]), T(p["sous_titre"])))
    out.append("</div>")
    return "\n".join(out)

def b_etapes(b, ctx):
    out = ['<div class="steps">']
    for e in b["etapes"]:
        out.append('      <article class="stepcard rv"><div class="num" aria-hidden="true"></div>\n'
                   '        <h3>%s</h3>\n        <p>%s</p></article>'
                   % (T(e["titre"]), T(e["texte"])))
    out.append("    </div>")
    return "\n".join(out)

def b_photos(b, ctx):
    n = b.get("colonnes", 3)
    sizes = ("(max-width:700px) 100vw, 33vw" if n == 3
             else "(max-width:700px) 50vw, 25vw")
    fmt = "3/2" if b.get("style") == "coloris" else "4/3"
    cls = "gallery colorshots" if b.get("style") == "coloris" else "gallery"
    style = '' if b.get("style") == "coloris" else ' style="margin-top:34px"'
    out = ['<div class="%s"%s>' % (cls, style)]
    for p in b["photos"]:
        out.append('      <figure class="rv">%s\n        <figcaption>%s</figcaption></figure>'
                   % (shot(p, format=fmt, sizes=sizes), T(p.get("legende", ""))))
    out.append("    </div>")
    return "\n".join(out)

def b_bandeau(b, ctx):
    return ('<figure class="band rv">\n      %s\n'
            '      <figcaption>%s</figcaption>\n    </figure>'
            % (shot(b, format="16/9", zoom=True, sizes="100vw"), T(b.get("legende", ""))))

def b_texte_photo(b, ctx):
    photo = shot(b, format=b.get("format", "4/3"),
                 zoom=not b.get("detouree"),
                 sizes="(max-width:900px) 100vw, 50vw")
    photo_html = photo.replace('"><picture>', ' rv"><picture>', 1)
    texte = []
    if b.get("titre"):
        texte.append("        <h3>%s</h3>" % T(b["titre"]))
    if b.get("paragraphes"):
        texte.append(paras(b["paragraphes"], first_no_margin=b.get("haut")))
    if b.get("puces"):
        texte.append("        " + puces(b["puces"], b.get("puces_orange")))
    bloc_texte = '<div class="rv">\n%s\n      </div>' % "\n".join(texte)
    cls = "two top" if b.get("haut") else "two"
    if b.get("photo_a") == "droite":
        return '<div class="%s">\n      %s\n      %s\n    </div>' % (cls, bloc_texte, photo_html)
    return '<div class="%s">\n      %s\n      %s\n    </div>' % (cls, photo_html, bloc_texte)

def b_schema(b, ctx):
    photo = shot(b, format="4/3", sizes="(max-width:900px) 100vw, 50vw",
                 extra="margin-top:22px")
    return ('<div class="two">\n      %s\n'
            '      <div class="rv">\n'
            '        <h3>%s</h3>\n        <p>%s</p>\n        %s\n      </div>\n    </div>'
            % (ctx["FIG"], T(b["titre"]), T(b["texte"]), photo))

def b_photo_centree(b, ctx):
    return ('<figure class="solo rv">\n'
            '      <button class="zoomable" type="button" data-full="assets/img/%s-900.jpg">%s</button>\n'
            '      <figcaption>%s</figcaption>\n    </figure>'
            % (slug_of(b["image"]),
               pic(b["image"], b.get("alt", ""), w=900, h=1201,
                   sizes="(max-width:700px) 80vw, 380px", big=False),
               T(b.get("legende", ""))))

def b_nuancier(b, ctx):
    chips = "\n".join(
        '    <div class="colorchip"><div class="sw" style="background:%s"></div><b>%s</b></div>'
        % (c["couleur"], T(c["nom"])) for c in SITE["coloris"])
    return '<div class="colors rv">\n%s\n    </div>' % chips

def b_note(b, ctx):
    return '<p class="note rv">%s</p>' % T(b["texte"])

def b_boutons(b, ctx):
    links = []
    for x in b["boutons"]:
        style = x.get("style", "")
        cls = "btn" + (" " + style if style else "")
        links.append('      <a class="%s" href="%s">%s</a>' % (cls, Tb(x["lien"]), T(x["texte"])))
    return '<div class="cta-row rv">\n%s\n    </div>' % "\n".join(links)

def b_fiche_technique(b, ctx):
    lignes = "\n".join('        <div><span>%s</span><span>%s</span></div>'
                       % (T(l["libelle"]), T(l["valeur"])) for l in b["lignes"])
    sous = []
    for i, s in enumerate(b.get("sous_blocs", [])):
        mt = ' style="margin-top:34px"' if i else ""
        sous.append('        <h3%s>%s</h3>\n        <p>%s</p>\n        %s'
                    % (mt, T(s["titre"]), T(s["texte"]),
                       shot(s, format="4/3", zoom=not s.get("detouree"),
                            sizes="(max-width:900px) 100vw, 50vw",
                            extra="margin-top:20px")))
    return ('<div class="two top">\n'
            '      <div class="speclist rv">\n%s\n      </div>\n'
            '      <div class="rv">\n%s\n      </div>\n    </div>'
            % (lignes, "\n".join(sous)))

def b_tableau(b, ctx):
    rows = []
    for l in b["lignes"]:
        cls = ' class="me"' if l.get("nous") else ""
        def mark(v):
            v = T(v)
            return ('<td class="yes">%s</td>' % v if v.lower() in ("oui",)
                    else '<td class="no">%s</td>' % v)
        rows.append('          <tr%s><td>%s</td><td class="n">%s</td><td class="n">%s</td>'
                    '<td class="n">%s</td>%s%s</tr>'
                    % (cls, T(l["modele"]), T(l["prix"]), T(l["ptac"]), T(l["charge"]),
                       mark(l["sans_rampe"]), mark(l["vertical"])))
    return ('<div class="tw rv">\n      <table>\n        <caption>%s</caption>\n'
            '        <thead><tr><th scope="col">Modèle</th><th scope="col">Prix TTC</th>'
            '<th scope="col">PTAC</th>\n'
            '        <th scope="col">Charge utile</th><th scope="col">Sans rampe</th>'
            '<th scope="col">Rangement vertical</th></tr></thead>\n'
            '        <tbody>\n%s\n        </tbody>\n      </table>\n    </div>'
            % (T(b["legende"]), "\n".join(rows)))

def b_bloc_prix(b, ctx):
    incl = "\n".join("          <li>%s</li>" % T(x) for x in b["inclus"])
    opts = "\n".join('          <span class="opt">+ %s</span>' % T(x) for x in b["options"])
    agences = "\n".join(
        '    <div class="agence"><b>%s</b><span>%s</span><p>%s</p></div>'
        % (T(a["ville"]), T(a["departement"]), T(a["adresse"])) for a in SITE["agences"])
    col = []
    for i, c in enumerate(b["colonne"]):
        mt = ' style="margin-top:36px"' if i else ""
        col.append('        <h3%s>%s</h3>\n        <p>%s</p>' % (mt, T(c["titre"]), T(c["texte"])))
        if c.get("agences"):
            col.append('        <div class="agences">\n%s\n        </div>' % agences)
    return ('<div class="two top">\n'
            '      <div class="pricebox rv">\n'
            '        <div class="price">%s <sup>€ TTC</sup></div>\n'
            '        <p class="pricesub">%s</p>\n'
            '        <div class="pricerow"><span>%s</span><b>+ %s € TTC</b></div>\n'
            '        <ul class="incl">\n%s\n        </ul>\n'
            '        <div class="opts">\n%s\n        </div>\n'
            '        <div class="cta-row">\n'
            '          <a class="btn" href="devis.html">Demander un devis</a>\n'
            '          <a class="btn ghost" href="tel:%s">%s</a>\n'
            '        </div>\n      </div>\n'
            '      <div class="rv">\n%s\n      </div>\n    </div>'
            % (SITE["prix"], T(b["sous_prix"]), T(b["ligne_livraison"]), SITE["livraison"],
               incl, opts, SITE["telephone_lien"], SITE["telephone"], "\n".join(col)))

def b_deux_photos(b, ctx):
    ph = "\n      ".join(
        shot(p, format="16/9", zoom=True, sizes="(max-width:900px) 100vw, 50vw")
        .replace('"><picture>', ' rv"><picture>', 1) for p in b["photos"])
    return '<div class="two">\n      %s\n    </div>' % ph

def b_villes(b, ctx):
    return ('<div class="cities rv">\n      %s\n    </div>'
            % "".join("<span>%s</span>" % T(v) for v in b["villes"]))

def b_faq(b, ctx):
    out = ['<div class="faq rv">']
    for i, q in enumerate(charger("faq.yml")["questions"]):
        op = " open" if i == 0 else ""
        out.append('  <details%s><summary>%s</summary><div class="ans"><p>%s</p></div></details>'
                   % (op, T(q["question"]), T(q["reponse"])))
    out.append("</div>")
    return "\n".join(out)

def b_texte(b, ctx):
    out = []
    if b.get("titre"):
        out.append("    <h3>%s</h3>" % T(b["titre"]))
    out.append(paras(b.get("paragraphes", [])))
    if b.get("puces"):
        out.append("    " + puces(b["puces"], b.get("puces_orange")))
    return '<div class="rv prose">\n%s\n    </div>' % "\n".join(out)

BLOCS = {
    "piliers": b_piliers, "etapes": b_etapes, "photos": b_photos, "bandeau": b_bandeau,
    "texte_photo": b_texte_photo, "schema": b_schema, "photo_centree": b_photo_centree,
    "nuancier": b_nuancier, "note": b_note, "boutons": b_boutons,
    "fiche_technique": b_fiche_technique, "tableau": b_tableau, "bloc_prix": b_bloc_prix,
    "deux_photos": b_deux_photos, "villes": b_villes, "faq": b_faq, "texte": b_texte,
}

_FONDS = {"clair": "", "gris": "alt", "sombre": "dark"}

def rendre_section(s, ctx):
    cls = _FONDS.get(s.get("fond", "clair"), "")
    attrs = ' id="%s"' % s["id"] if s.get("id") else ""
    attrs += ' class="%s"' % cls if cls else ""
    tete = []
    if s.get("kicker"):
        tete.append('    <p class="sec-k rv">%s</p>' % T(s["kicker"]))
    if s.get("titre"):
        tete.append('    <h2 class="rv">%s</h2>' % T(s["titre"]))
    if s.get("chapo"):
        tete.append('    <p class="lede rv">%s</p>' % T(s["chapo"]))
    if s.get("texte"):
        tete.append('    <p class="rv">%s</p>' % T(s["texte"]))
    corps = []
    for b in s.get("contenu", []):
        fn = BLOCS.get(b["type"])
        if fn is None:
            raise SystemExit("Type de bloc inconnu : %r (section %s)" % (b["type"], s.get("id")))
        corps.append("    " + fn(b, ctx))
    return ('<section%s>\n  <div class="wrap">\n%s\n%s\n  </div>\n</section>'
            % (attrs, "\n".join(tete), "\n".join(corps)))

def rendre_sections(sections, ctx):
    return "\n\n".join(rendre_section(s, ctx) for s in sections)

# --- Haut de page -----------------------------------------------------------

def hero_html(h):
    return ('<section class="hero">\n'
            '  <video id="herovid" autoplay muted loop playsinline preload="metadata"\n'
            '         poster="assets/video/poster-hero.jpg" aria-hidden="true" tabindex="-1">\n'
            '    <source src="assets/video/hero-smart-biker.mp4" type="video/mp4">\n'
            '  </video>\n'
            '  <button class="vidctl" id="vidctl" type="button" aria-label="Mettre la vidéo en pause">&#10073;&#10073;</button>\n'
            '  <div class="wrap hero-in">\n'
            '    <span class="kicker">%s</span>\n'
            '    <h1>%s</h1>\n'
            '    <p class="intro">%s</p>\n'
            '    <div class="cta-row">\n'
            '      <a class="btn onphoto" href="%s">%s</a>\n'
            '      <a class="btn outlight" href="%s">%s</a>\n'
            '    </div>\n'
            '    <button class="playfull" id="playfull" type="button">\n'
            '      <span class="pl" aria-hidden="true">&#9654;</span>\n'
            '      %s <i>%s</i>\n'
            '    </button>\n'
            '    <p class="hero-note">%s</p>\n'
            '  </div>\n'
            '</section>'
            % (T(h["kicker"]), T(h["titre"]), T(h["intro"]),
               Tb(h["bouton_lien"]), T(h["bouton"]),
               Tb(h["bouton2_lien"]), T(h["bouton2"]),
               T(h["bouton_film"]), T(h["bouton_film_duree"]), T(h["note"])))

def chiffres_html(items):
    cells = "\n".join('    <div><b>%s<i> %s</i></b><span>%s</span></div>'
                      % (T(c["valeur"]), T(c["unite"]), T(c["libelle"])) for c in items)
    return '<div class="wrap">\n  <div class="specstrip">\n%s\n  </div>\n</div>' % cells

# --- Articles ---------------------------------------------------------------

def charger_articles():
    """Lit content/articles/*.md : entête YAML + corps en markdown."""
    import glob, markdown
    arts = []
    for p in sorted(glob.glob(os.path.join(ROOT, "content", "articles", "*.md"))):
        brut = open(p, encoding="utf-8").read()
        if not brut.startswith("---"):
            continue
        _, entete, corps = brut.split("---", 2)
        a = yaml.safe_load(entete) or {}
        if a.get("publie") is False:
            continue
        a["slug"] = os.path.basename(p)[:-3]
        a["fichier"] = "conseil-%s.html" % a["slug"]
        a["corps"] = markdown.markdown(Tb(corps), extensions=["extra", "sane_lists"])
        arts.append(a)
    arts.sort(key=lambda a: str(a.get("date", "")), reverse=True)
    return arts

def date_fr(d):
    MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
            "août", "septembre", "octobre", "novembre", "décembre"]
    try:
        return "%d %s %d" % (d.day, MOIS[d.month - 1], d.year)
    except Exception:
        return str(d)

def liste_articles_html(arts):
    out = ['<div class="gallery arts">']
    for a in arts:
        img = ""
        if a.get("image"):
            img = ('<div class="shot r169">%s</div>'
                   % pic(a["image"], a.get("alt", ""), w=1600, h=900,
                         sizes="(max-width:700px) 100vw, 33vw"))
        out.append('  <article class="artcard rv">\n'
                   '    <a href="%s">%s\n'
                   '      <h3>%s</h3>\n'
                   '      <p>%s</p>\n'
                   '      <span class="artdate">%s</span>\n'
                   '    </a>\n  </article>'
                   % (a["fichier"], img, T(a["titre"]), T(a.get("resume", "")),
                      date_fr(a.get("date", ""))))
    out.append("</div>")
    return "\n".join(out)
