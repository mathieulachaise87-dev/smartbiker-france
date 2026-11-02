# SMART BIKER France — le site

Site statique : des pages HTML pures, sans base de données, sans PHP. Elles sont
fabriquées à partir des fichiers du dossier `content/`, eux-mêmes modifiables
depuis un back-office à l'adresse `/admin`.

---

## 1. Pour celui qui modifie le site

Tout se passe sur **`smartbiker-france.fr/admin`**.

Vous vous connectez avec votre e-mail et votre mot de passe. Pas besoin de compte
GitHub, pas besoin de savoir ce qu'est un dépôt.

Ce que vous y trouvez :

| Rubrique | Ce qu'on y change |
|---|---|
| **Réglages du site** | Le prix, le prix de la livraison, le téléphone, l'e-mail, les trois agences, les coloris, le menu |
| **Pages du site › Accueil** | Chaque section de la page d'accueil, bloc par bloc |
| **Pages du site › Galerie** | Les photos, leur ordre, leurs légendes |
| **Pages du site › Questions fréquentes** | Les questions et les réponses |
| **Pages du site › Page Conseils** | Le chapeau de la page qui liste les articles |
| **Conseils et guides** | Les articles. C'est ici qu'on gagne du référencement |

Vous modifiez, vous cliquez **Publier**. Le site se refabrique tout seul et se met
en ligne en une minute environ.

### Le prix ne se change qu'à un seul endroit

Dans **Réglages du site**. Il se met à jour partout : le bandeau d'ouverture, le
tableau comparatif, l'encadré tarif, les questions fréquentes, la page devis, et
jusque dans ce que Google affiche dans ses résultats.

Dans n'importe quel texte, écrire `{prix}` affiche le prix du moment, `{livraison}`
le supplément de livraison, `{tel}` le téléphone. Vous n'avez jamais à retaper un
montant.

### Mettre un mot en valeur

- `**en gras**` → **en gras**
- `*en rouge*` → le mot s'affiche en rouge, comme « abaissable » dans le grand titre

### Ajouter une photo

Dans n'importe quel champ photo, bouton **Choose an image**, puis **Upload**.
Rien d'autre à faire : les versions légères et les formats modernes sont fabriqués
automatiquement à la publication.

**La description de la photo compte.** C'est ce que lit Google et ce qu'entendent
les personnes malvoyantes. Écrivez ce que montre la photo avec les mots que vos
clients tapent : « remorque porte-moto abaissable blanche, plateau au sol », pas
« IMG_4821 ».

### Ajouter un bloc dans une section

Dans **Accueil**, ouvrez une section, descendez jusqu'à **Blocs**, cliquez
**Add Blocs** et choisissez le type. Vous pouvez aussi faire glisser un bloc pour
le déplacer, ou une section entière pour la remonter.

Les types disponibles :

| Bloc | Ce que ça donne |
|---|---|
| Texte | Un sous-titre, des paragraphes, des puces |
| Texte + photo | Deux colonnes, photo à gauche ou à droite |
| Rangée de photos | 2, 3 ou 4 photos avec légendes |
| Grande photo pleine largeur | Une image qui occupe toute la largeur |
| Photo verticale centrée | Une photo en portrait, cliquable pour agrandir |
| Deux photos côte à côte | Deux images en 16/9 |
| Étapes numérotées | Les cartes 1, 2, 3 |
| Boutons | Un ou plusieurs boutons d'appel à l'action |
| Note discrète | Une petite précision en bas de section |
| Liste de villes | Les pastilles des villes livrées |
| Tableau comparatif | Le tableau des concurrents |
| Fiche technique | La liste des caractéristiques + encadrés |
| Encadré prix | Le bloc tarif complet |
| Les cinq promesses | La rangée d'icônes oranges |
| Pastilles de coloris | Les ronds de couleur |
| Questions fréquentes | Le dépliant des questions |
| Schéma animé | Le schéma du mécanisme en trois positions |

### Écrire un article

**Conseils et guides › New Article**. Titre, description pour Google, résumé,
date, photo, puis le texte. Les sous-titres se font avec `## Mon sous-titre`.

Un article publié crée une page de plus, ajoutée automatiquement au plan du site
envoyé à Google. C'est le levier le plus direct pour apparaître sur de nouvelles
recherches.

### Si quelqu'un casse quelque chose

Rien n'est définitif. Chaque modification est enregistrée au nom de son auteur et
peut être annulée. Demandez, on revient à la version d'avant.

---

## 1 bis. Essayer sans rien installer en ligne

### Voir le site

Décompressez le dossier et double-cliquez sur **`index.html`**. Tout fonctionne
hors ligne : les photos, la vidéo, le schéma animé, la galerie. Seul le formulaire
de devis a besoin d'être en ligne.

### Essayer le back-office sur votre ordinateur

Double-cliquez sur **`TESTER-LE-BACK-OFFICE.bat`**.

Il démarre deux petits serveurs sur votre machine et ouvre le back-office dans
votre navigateur, à l'adresse `http://localhost:8080/admin/`. **Aucun compte, aucun
mot de passe, aucune connexion Internet au site** : vous modifiez directement les
fichiers du dossier, sur votre disque.

C'est la façon de prendre le CMS en main avant de créer quoi que ce soit, et de
voir à quoi ressemblera l'écran de vos commerciaux.

Il faut **Node.js** installé sur le poste. Si ce n'est pas le cas, le script vous
l'indique et ouvre la page de téléchargement : prenez la version LTS, bouton vert.
Le tout premier démarrage prend une minute, le temps que les outils se téléchargent.

Une fois une modification publiée dans le back-office, double-cliquez sur
**`REGENERER-LE-SITE.bat`** pour reconstruire les pages, puis rouvrez `index.html`.
En ligne, cette étape sera automatique.

---

## 2. Pour celui qui installe

### Les trois comptes

1. **GitHub** — contient le site. Un seul compte suffit, celui du propriétaire.
2. **DecapBridge** — gère les connexions. C'est là qu'on invite les commerciaux
   par e-mail. Gratuit jusqu'à 10 personnes.
3. **L'hébergement** — ici, celui déjà en place.

### Les deux lignes à compléter

Dans `admin/config.yml` :

```yaml
repo: VOTRE-COMPTE/smartbiker-france                                   # À REMPLIR
identity_url: https://auth.decapbridge.com/sites/VOTRE-ID-DECAPBRIDGE  # À REMPLIR
```

### Les secrets de publication

Dans GitHub › Settings › Secrets and variables › Actions :

| Nom | Onglet | Contenu |
|---|---|---|
| `FTP_HOST` | Secrets | l'adresse FTP de l'hébergeur |
| `FTP_USER` | Secrets | l'identifiant FTP |
| `FTP_PASS` | Secrets | le mot de passe FTP |
| `FTP_DIR` | Variables | le dossier sur le serveur, souvent `/www` ou `/public_html` |

Le script `.github/workflows/publier.yml` fait le reste : il régénère les pages et
les envoie par FTP à chaque publication.

Il exige une connexion FTP chiffrée (FTPS). Si l'hébergeur ne la propose pas, il
faut le lui demander plutôt que de désactiver la vérification : les identifiants
circuleraient en clair.

### Au moment de basculer

Le site actuel est un WordPress. Déposer ces fichiers à côté ne suffira pas :
tant que `index.php` est présent, c'est lui qui s'affichera. Il faut demander à
l'hébergeur de vider ou de mettre de côté l'installation WordPress du dossier
racine avant la première publication.

---

## 3. Pour celui qui développe

```
content/              Tout le contenu éditable
  site.yml              prix, coordonnées, agences, coloris, menu
  accueil.yml           la page d'accueil : hero, chiffres, sections, blocs
  galerie.yml           les photos de la galerie
  faq.yml               les questions fréquentes
  piliers.yml           les cinq promesses
  conseils.yml          l'en-tête de la page qui liste les articles
  articles/*.md         un fichier par article (entête YAML + markdown)

blocks.py             Le moteur de rendu : un bloc = une fonction b_<type>()
medias.py             Fabrique les variantes des photos déposées
_partials.py          En-tête, pied de page, balises <head>
build.py              Assemble le tout et écrit les pages

admin/                Le back-office (Decap CMS)
assets/               CSS, JavaScript, images, vidéos
.github/workflows/    La publication automatique
```

Pour régénérer les pages en local :

```
pip install pyyaml markdown pillow
python3 build.py
```

### Ajouter un nouveau type de bloc

1. Écrire `b_mon_bloc(b, ctx)` dans `blocks.py`, qui renvoie du HTML.
2. L'ajouter au dictionnaire `BLOCS` en bas du fichier.
3. Déclarer ses champs dans `admin/config.yml`, sous `contenu › types`.

Le nom utilisé dans les trois endroits doit être identique.

---

## 4. Le référencement

Déjà en place :

- un seul `<h1>` par page, hiérarchie de titres cohérente ;
- titres et descriptions uniques, rédigés sur les mots réellement recherchés ;
- données structurées JSON-LD : fiche produit avec prix et frais de port,
  établissement local, questions-réponses, articles ;
- Open Graph et Twitter Card pour les partages ;
- images en WebP avec repli JPEG, deux tailles, chargement différé, dimensions
  déclarées ;
- `robots.txt` et `sitemap.xml` régénéré à chaque publication, articles compris.

Après la mise en ligne : soumettre `sitemap.xml` dans Google Search Console, et
ajouter un lien depuis `remorqueco.fr` vers ce site.

---

## 5. Les photos

Trois familles, et elles ne se mélangent pas :

1. **Les rendus studio** — fond blanc, même angle, même lumière. Ce sont les
   visuels officiels de la marque. Ils servent partout où l'on montre **le
   produit**. Cochez « Photo détourée » pour qu'elles s'affichent entières sur
   fond blanc.
2. **Les images du film** — extraites en 4K du film officiel, elles servent
   partout où l'on montre **l'usage**.
3. **Les photos de terrain** — remorques livrées, coloris réels : uniquement dans
   la galerie, jamais sur l'accueil.

Une photo de produit va sur fond blanc, une photo d'usage montre quelqu'un ou un
véhicule. Un cliché de parking sur l'accueil fait baisser la page entière.

---

## 6. Reste à compléter avant la mise en ligne

- `mentions-legales.html` : forme juridique, capital, SIRET, TVA, directeur de la
  publication, coordonnées de l'hébergeur. C'est une obligation légale.
- L'adresse e-mail de contact (actuellement `contact@smartbiker-france.fr`).
- Les adresses complètes des agences de La Souterraine et d'Angoulême.
- Le formulaire de devis fonctionne en mode « ouvrir le logiciel de messagerie ».
  Pour un envoi par le serveur, retirer `data-mode="mailto"` du formulaire dans
  `build.py` et renseigner l'adresse fournie par l'hébergeur.
