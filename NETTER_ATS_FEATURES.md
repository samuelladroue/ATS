# Netter ATS - Fonctionnalités complètes

## Vue d'ensemble

Netter ATS est un système de suivi des candidatures (Applicant Tracking System) moderne et épuré, conçu pour simplifier le processus de recrutement. La plateforme offre deux espaces distincts : un espace public pour les candidats et un espace d'administration pour les recruteurs.

---

## 🎯 Espace Candidat

### Page d'accueil publique
- **Affichage des offres d'emploi** : Liste visuelle de toutes les offres d'emploi ouvertes avec un design moderne et épuré
- **Informations essentielles** : Chaque offre affiche le titre, la localisation, le département et un bouton "Learn more" pour accéder aux détails
- **Navigation intuitive** : Interface claire permettant aux candidats de découvrir facilement les opportunités disponibles

### Page de détail d'une offre
- **Description complète** : Affichage de la description de l'offre au format Markdown avec sections structurées :
  - About the company
  - The Role
  - Responsibilities
  - Profile / What we're looking for
  - What we offer
  - Practical info
- **Informations pratiques** : Localisation, département, et autres détails pertinents
- **Formulaire de candidature intégré** : Formulaire simple et efficace permettant aux candidats de postuler directement depuis la page de l'offre
  - Nom complet
  - Email
  - Lien LinkedIn (optionnel)
- **Page de confirmation** : Redirection vers une page de succès après soumission de la candidature

---

## 🔐 Espace Administration

### Gestion des offres d'emploi

#### Liste des offres
- **Vue d'ensemble** : Affichage de toutes les offres d'emploi (ouvertes et fermées)
- **Création d'offres** : Formulaire complet pour créer de nouvelles offres avec :
  - Slug (identifiant unique URL-friendly)
  - Titre de l'offre
  - Description au format Markdown
  - Localisation
  - Département
  - Statut (ouvert/fermé)
- **Navigation rapide** : Accès direct aux candidatures de chaque offre via un bouton "Learn more"

### Gestion des candidatures - Vue Kanban

#### Organisation par stages
Le système propose **6 stages de recrutement** organisés en colonnes Kanban :

1. **New applicants** - Nouvelles candidatures
2. **Screening interview** - Entretien de présélection
3. **Technical interview** - Entretien technique
4. **Offer sent** - Offre envoyée
5. **Hired** - Embauché
6. **Refused** - Refusé

#### Fonctionnalités du Kanban
- **Vue d'ensemble** : Affichage visuel de toutes les candidatures organisées par stage
- **Compteur par colonne** : Nombre de candidatures dans chaque stage affiché en temps réel
- **Cartes candidats** : Chaque candidature est représentée par une carte affichant :
  - Nom du candidat
  - Badge indiquant le numéro du stage actuel
  - Lien LinkedIn (logo cliquable)
  - Résumé des notes et évaluations (affichage des 4 dernières notes avec leur note sur 4)
  - Note moyenne calculée automatiquement
  - Boutons numérotés (1-6) pour changer rapidement de stage
- **Déplacement entre stages** : Glisser-déposer ou clic sur les boutons numérotés pour déplacer une candidature d'un stage à l'autre
- **Mise en évidence du stage actuel** : Le bouton correspondant au stage actuel est mis en évidence avec une bordure noire épaisse

### Détails d'une candidature

#### Modal de détails complet
Lorsqu'un recruteur clique sur "Voir détails", une fenêtre modale s'ouvre avec deux colonnes :

**Colonne gauche (informations fixes)** :
- **Informations candidat** :
  - Nom complet
  - Email
  - Lien LinkedIn (cliquable)
  - Date de candidature
- **Changement de stage** : Liste de tous les stages disponibles avec le stage actuel mis en évidence (fond blanc, texte noir, bordure noire épaisse, taille agrandie)

**Colonne droite (notes et compte-rendus, scrollable)** :
- **Système de notes par stage** : Pour chaque stage, possibilité d'ajouter :
  - **Compte-rendu** : Texte libre pour décrire l'entretien ou l'évaluation
  - **Note sur 4** : Système de notation de 1 à 4 avec code couleur :
    - 🟢 Vert pour les notes 3 et 4 (positif)
    - 🔴 Rouge pour les notes 1 et 2 (négatif)
  - **Nom de l'interviewer** : Enregistrement de la personne qui a mené l'entretien
- **Historique des notes** : Affichage chronologique de toutes les notes ajoutées pour chaque stage avec :
  - Date et heure
  - Note sur 4 (avec code couleur)
  - Compte-rendu complet
  - Nom de l'interviewer
- **Validation** : Bouton de soumission clair pour enregistrer les notes avec indicateur de succès

#### Affichage des notes dans le Kanban
- **Résumé visuel** : Les notes sont affichées directement sur les cartes du Kanban
- **Badges colorés** : Chaque note apparaît comme un badge avec sa note sur 4 (vert pour 3-4, rouge pour 1-2)
- **Note moyenne** : Calcul et affichage automatique de la note moyenne de toutes les évaluations
- **Limite d'affichage** : Affichage des 4 notes les plus récentes avec un compteur "+X" pour les notes supplémentaires

---

## 🎨 Design et Expérience Utilisateur

### Interface moderne et épurée
- **Style "Revolut-like"** : Design minimaliste et professionnel inspiré des meilleures pratiques UX
- **Typographie claire** : Hiérarchie visuelle bien définie pour une lecture facile
- **Couleurs cohérentes** : Palette de couleurs primaires harmonieuse
- **Responsive** : Interface adaptée à tous les écrans (mobile, tablette, desktop)

### Navigation intuitive
- **Barre de navigation** : Boutons "Candidat" et "Admin" en haut de l'écran pour basculer facilement entre les espaces
- **Breadcrumbs** : Liens de retour pour une navigation fluide
- **Feedback visuel** : Animations et transitions pour une expérience utilisateur agréable

---

## 🔧 Fonctionnalités techniques

### Backend (FastAPI)
- **API RESTful** : Architecture moderne avec endpoints bien structurés
- **Base de données PostgreSQL/Supabase** : Stockage sécurisé et performant
- **Authentification admin** : Système de clé API pour protéger les routes d'administration
- **Gestion des UUIDs** : Identifiants uniques pour toutes les entités
- **Validation des données** : Modèles Pydantic pour garantir l'intégrité des données

### Frontend (Nuxt 3)
- **Server-side rendering** : Performance optimale et SEO-friendly
- **Routes sécurisées** : Les routes admin passent par des server routes Nuxt pour protéger les clés API
- **TypeScript** : Code type-safe pour une meilleure maintenabilité
- **Tailwind CSS** : Styling moderne et responsive

### Sécurité
- **Séparation des espaces** : Routes publiques et admin clairement séparées
- **Protection des clés API** : Les clés admin ne sont jamais exposées au client
- **Validation côté serveur** : Toutes les données sont validées avant traitement

---

## 📊 Résumé des fonctionnalités principales

### Pour les candidats
✅ Consultation des offres d'emploi ouvertes  
✅ Visualisation détaillée d'une offre  
✅ Candidature en ligne simple et rapide  
✅ Confirmation de candidature  

### Pour les recruteurs
✅ Création et gestion des offres d'emploi  
✅ Vue Kanban pour le suivi des candidatures  
✅ 6 stages de recrutement configurables  
✅ Système de notes et évaluations par stage  
✅ Historique complet des entretiens  
✅ Affichage des notes directement dans le Kanban  
✅ Calcul automatique des notes moyennes  
✅ Gestion des interviewers  
✅ Interface intuitive pour changer les stages  

---

## 🚀 Technologies utilisées

- **Backend** : FastAPI (Python)
- **Frontend** : Nuxt 3 (Vue.js)
- **Base de données** : PostgreSQL (via Supabase)
- **Styling** : Tailwind CSS
- **Langage** : TypeScript / Python

---

Netter ATS offre une solution complète et moderne pour gérer efficacement le processus de recrutement, de la publication des offres à l'évaluation des candidats, en passant par le suivi des différentes étapes du processus de recrutement.

