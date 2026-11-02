# -*- coding: utf-8 -*-
"""
Prépare les images déposées depuis /admin.

Une photo téléversée arrive seule dans assets/img/. Le site, lui, a besoin
de quatre fichiers par photo : deux largeurs × deux formats (WebP et JPEG).
Ce script fabrique ce qui manque, à chaque génération du site. Il ne touche
jamais à une photo déjà complète.
"""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
LARGE, PETITE = 1600, 900
SOURCES = (".jpg", ".jpeg", ".png", ".webp")

def _slug(nom):
    base = os.path.splitext(nom)[0]
    return base[:-4] if base.endswith("-900") else base

def preparer(verbeux=True):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return 0
    faits = 0
    slugs = {}
    for p in glob.glob(os.path.join(IMG, "*")):
        nom = os.path.basename(p)
        ext = os.path.splitext(nom)[1].lower()
        if ext not in SOURCES:
            continue
        slugs.setdefault(_slug(nom), []).append(p)

    for slug, fichiers in sorted(slugs.items()):
        attendus = [os.path.join(IMG, slug + s + e)
                    for s in ("", "-900") for e in (".jpg", ".webp")]
        if all(os.path.exists(f) for f in attendus):
            continue
        # on part du fichier le plus large disponible
        source, largeur = None, 0
        for f in fichiers:
            try:
                w = Image.open(f).width
            except Exception:
                continue
            if w > largeur:
                source, largeur = f, w
        if source is None:
            continue
        try:
            im = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
        except Exception:
            continue
        for cible, maxi in ((slug, LARGE), (slug + "-900", PETITE)):
            w = min(maxi, im.width)
            h = max(1, round(im.height * w / im.width))
            red = im.resize((w, h), Image.LANCZOS) if w != im.width else im
            for ext, kw in ((".jpg", dict(quality=84, optimize=True, progressive=True)),
                            (".webp", dict(quality=80, method=5))):
                out = os.path.join(IMG, cible + ext)
                if not os.path.exists(out):
                    red.save(out, **kw)
                    faits += 1
                    if verbeux:
                        print("  image préparée : %s" % os.path.basename(out))
    return faits

if __name__ == "__main__":
    n = preparer()
    print("%d fichier(s) image généré(s)." % n)
