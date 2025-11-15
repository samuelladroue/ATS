-- Templates d'email d'exemple à insérer dans la table email_templates
-- Exécutez ces INSERT après avoir créé la table avec migration_add_email_tables.sql

-- Template 1: Invitation à un entretien de présélection
INSERT INTO email_templates (name, subject, body) VALUES (
  'Invitation entretien présélection',
  'Invitation à un entretien de présélection - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Nous avons bien reçu votre candidature et nous sommes ravis de vous informer que votre profil a retenu notre attention.

Nous aimerions vous rencontrer pour un entretien de présélection afin d''en apprendre davantage sur votre parcours et vos motivations.

Nous vous proposons de planifier cet entretien dans les prochains jours. Pouvez-vous nous indiquer vos disponibilités ?

En attendant, n''hésitez pas si vous avez des questions.

Cordialement,
L''équipe Netter'
);

-- Template 2: Invitation à un entretien technique
INSERT INTO email_templates (name, subject, body) VALUES (
  'Invitation entretien technique',
  'Invitation à un entretien technique - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Suite à notre premier échange, nous sommes convaincus que votre profil correspond à nos attentes.

Nous aimerions vous inviter à un entretien technique pour approfondir vos compétences techniques et discuter du poste en détail.

Cet entretien durera environ 1 heure et portera sur vos expériences techniques ainsi que sur des questions pratiques liées au rôle.

Pouvez-vous nous indiquer vos disponibilités pour la semaine prochaine ?

Cordialement,
L''équipe Netter'
);

-- Template 3: Offre d'emploi
INSERT INTO email_templates (name, subject, body) VALUES (
  'Offre d''emploi',
  'Offre d''emploi - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Nous avons le plaisir de vous faire une proposition d''embauche !

Après nos différents échanges, nous sommes convaincus que vous seriez un excellent ajout à notre équipe.

Vous trouverez ci-joint les détails de notre offre. Nous restons à votre disposition pour toute question ou clarification.

Nous espérons avoir de vos nouvelles rapidement.

Cordialement,
L''équipe Netter'
);

-- Template 4: Refus de candidature
INSERT INTO email_templates (name, subject, body) VALUES (
  'Refus candidature',
  'Réponse à votre candidature - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Nous vous remercions pour l''intérêt que vous avez porté à notre entreprise et pour le temps que vous avez consacré à votre candidature.

Après avoir examiné attentivement votre profil, nous avons pris la décision de ne pas retenir votre candidature pour ce poste.

Cette décision ne remet pas en question vos compétences, et nous vous souhaitons beaucoup de succès dans vos recherches.

Nous conservons votre candidature dans nos fichiers et ne manquerons pas de vous recontacter si une opportunité correspondant à votre profil se présente.

Cordialement,
L''équipe Netter'
);

-- Template 5: Confirmation de candidature
INSERT INTO email_templates (name, subject, body) VALUES (
  'Confirmation candidature',
  'Confirmation de réception de votre candidature - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Nous accusons réception de votre candidature et vous en remercions.

Votre dossier a bien été enregistré et sera examiné par notre équipe de recrutement dans les plus brefs délais.

Nous vous tiendrons informé(e) de l''évolution de votre candidature.

En attendant, n''hésitez pas si vous avez des questions.

Cordialement,
L''équipe Netter'
);

-- Template 6: Remerciement après entretien
INSERT INTO email_templates (name, subject, body) VALUES (
  'Remerciement après entretien',
  'Merci pour votre entretien - {{candidate_name}}',
  'Bonjour {{candidate_name}},

Nous tenons à vous remercier pour le temps que vous avez consacré à cet entretien.

Vos réponses et votre présentation nous ont permis de mieux comprendre votre profil et vos motivations.

Notre équipe va maintenant examiner votre candidature et nous vous reviendrons très prochainement avec une réponse.

Encore merci pour votre intérêt et votre disponibilité.

Cordialement,
L''équipe Netter'
);

