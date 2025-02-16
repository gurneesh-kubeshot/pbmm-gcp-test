# Document de conception technique

In English: [Technical  Design Document](./technical-design-document.md)

## Zone d'accueil PBMM (Protégé B, Intégrité moyenne/Disponibilité moyenne)

#### Contenu

* [Présentation de la documentation](#présentation-de-la-documentation)
  * [Public visé](#public-visé)
  * [Avis de non-responsabilité concernant la conformité ITSG-33/PBMM](#itsg-33)
* [1\. Aperçu de la zone d'accueil](#aperçu-de-la-zone-d'accueil)
* [2\. Condition préalable au déploiement](#condition-préalable-au-déploiement)
  * [2.1 Configurer votre organisation](#configurer-votre-organisation)
  * [2.2 Authentification et autorisation](#authentification-et-autorisation)
  * [2.3 Facturation](#facturation)
  * [2.4 Autres considérations](#autres-considérations)
* [3\. Étapes de déploiement de la zone d'accueil](#étapes-de-déploiement-de-la-zone-d'accueil)
  * [Le bootstrap de l'environnement (0-bootstrap)](#le-bootstrap-de-l'environnement)
  * [Organisation (1 organisation)](#organisation)
  * [Environnements (2-environnements)](#environnements)
  * [Réseaux (3 réseaux en étoile)](#réseaux)
  * [Projets (4-projets)](#projets)
  * [Politiques organisationnelles (polices à 6 organisations)](#politiques-organisationnelles)
  * [Appliance virtuelle réseau (7-fortigate)](#appliance-virtuelle-réseau)
* [4\. Caractéristiques de la zone d'accueil](#caractéristiques-de-la-zone-d'accueil)
  * [4.1 Gestion des identités et des accès (IAM)](#gestion-des-identités-et-des-accès)
  * [4.3 Réseaux Hub et Spoke](#réseaux-hub-et-spoke)
  * [4.4DNS](#dns)
  * [4.5 Pare-feu Politiques](#pare-feu-politiques)
  * [4.6 Pare-feu Fortigate : 2 appliances](#pare-feu-fortigate)
  * [4.7 Contrôles des services VPC](#contrôles-des-services-vpc)
  * [4.8 Journalisation centralisée](#journalisation-centralisée)
  * [4.9 Security Commande Center](#security-commande-center)
  * [4.10 Gestion des secrets](#gestion-des-secrets)
* [5\. Options de déploiement de la zone d'accueil](#options-de-déploiement-de-la-zone-daccueil)
  * [5.1 Création du cloud](#création-du-cloud)
  * [5.2 Déploiement manuel](#déploiement-manuel)
  * [5.3 Pipeline Devops Azure](#pipeline-devops-azure)
* [Tâches du jour 2 et meilleures pratiques opérationnelles	34](#tâches-du-jour-2-et-meilleures-pratiques-opérationnelles)
  * [Après le déploiement d'IAC](#après-le-déploiement-diac)
  * [Meilleures pratiques opérationnelles](#meilleures-pratiques-opérationnelles)
* [Annexe 1 : Nomenclature](#annexe-1)
* [Annexe 2 : Mappage des contrôles au code](#annexe-2)
* [Annexe 3 : Documents de référence](#annexe-3)

# Présentation de la documentation <a name="présentation-de-la-documentation"></a>

Ce document aide les clients Google Cloud à mettre en œuvre et à formaliser les contrôles de sécurité Protégé B, Intégrité moyenne, Disponibilité moyenne (PBMM) pour les systèmes d'information déployés sur Google Cloud Platform (GCP). Les clients peuvent utiliser ce document et le référentiel de code associé pour accélérer la création d'une base infonuagique répondant aux exigences de sécurité du gouvernement canadien. La base de code constitue un point de départ pour construire vos propres fondations avec des valeurs par défaut pragmatiques que vous pouvez personnaliser pour répondre à vos besoins spécifiques. 

Le Centre de la sécurité des télécommunications (CST) a fourni aux ministères et organismes du gouvernement du Canada (GC) un cadre de gestion des risques liés à la sécurité de l'information publié sous le nom de Ligne directrice sur la sécurité des technologies de l'information (ITSG-33).  [Annexe 3A des documents ITSG-33](https://www.cyber.gc.ca/fr/orientation/annexe-3a-catalogue-des-controles-de-securite-itsg-33) suggère des contrôles de sécurité et des améliorations des contrôles. ITSG-33 est aligné sur [version 4 du NIST 800-53](https://csrc.nist.gov/pubs/sp/800/53/r4/upd3/final). Le Centre canadien pour la cybersécurité (CCS) a publié divers profils sous forme d'un ensemble de contrôles de sécurité cloud pour différents niveaux de classification des données.  [Profil 1 (Protégé B / Intégrité moyenne / Disponibilité moyenne)](https://www.cyber.gc.ca/fr/orientation/annexe-4a-profil-1-protege-b-integrite-moyenne-disponibilite-moyenne-itsg-33) et [Profil 3 (SECRET / Intégrité moyenne / Disponibilité moyenne)](https://www.cyber.gc.ca/fr/orientation/annexe-4a-profil-3-secret-integrite-moyenne-disponibilite-moyenne-itsg-33). Pour les environnements contenant des informations appartenant à la catégorie de sécurité PBMM, ce document capture les détails d'un système d'information hébergé dans le cloud, y compris les spécifications de l'architecture du système et la mise en œuvre des contrôles de sécurité. 

Google fournit deux artefacts principaux pour aider les ministères et organismes du GC dans leur posture PBMM : un référentiel de codes de zone d'accueil (ZA) et ce document de conception technique (TDD) comprenant une annexe pour aider à cartographier les contrôles PBMM et les méthodes par lesquelles la zone d'accueil répond eux:

* **La zone d'accueil,** ce qui est un Google Cloud Landing Zone hébergée sur GitHub, basée sur Terraform et conforme à PBMM, que GC peut cloner dans son propre référentiel, définir des variables et déployer.   
* **Le TDD** (ce document) détaille les spécifications de l'architecture du système. Le PBMM inclus sécurité la cartographie des contrôles décrit la mise en œuvre des contrôles de sécurité, ainsi que les documents qui contrôlent l'environnement de la Landing Zone hérité de Google et ceux que le département ou l'agence a mis en œuvre.  

Les ministères et organismes du GC peuvent utiliser ces deux artefacts pour fournir des détails ITSG-33/PBMM à toute partie intéressée pour leur système d'information hébergé par GCP. 

Le PBMM ZA est construit en utilisant le [Plan de fondation d’entreprise](https://cloud.google.com/architecture/security-foundations?hl=fr) et [Exemple de fondation Terraform](https://github.com/terraform-google-modules/terraform-example-foundation) v4 dépôt.

## Public visé <a name="public-visé"></a>

Ce document, ainsi que le mappage PBMM inclus, sont destinés à être utilisés par le personnel suivant au sein de l’organisation d’un client :

* Propriétaire du système d'information \- *Principale partie prenante de Google*  
* Évaluateur indépendant du ministère ou de l’agence ou organisme d’évaluation tiers  
* Administrateurs GCP pour le système d'information  
* Personnel de sécurité d'un département, d'un ministère ou d'une agence : CIO, CTO, ISSM, ISSO, etc.

# 

## Avis de non-responsabilité concernant la conformité ITSG-33/PBMM <a name="itsg-33"></a>

Google maintient l'alignement sur les normes de conformité sur de nombreux services cloud permettre aux clients de créer des applications et des systèmes de support généraux conformes ; toutefois, ce sont les ministères et organismes qui sont responsables en fin de compte de assurer que leurs systèmes informatiques sont conformes à l'ITSG-33/PBMM lorsque cela est nécessaire.

Ce document de conception technique (TDD) décrit les composants de mise en œuvre et de configuration de la zone d'accueil alignés sur l'ITSG-33/PBMM.

# 

# 1\. Aperçu de la zone d'accueil <a name="aperçu-de-la-zone-d'accueil"></a>

Une fondation cloud est le point de départ essentiel pour les organisations du secteur public canadien qui adoptent Google Cloud. Il englobe les ressources de base, les configurations standardisées et les fonctionnalités qui permettent aux agences d'exploiter Google Cloud de manière sécurisée et efficace. Les zones d'atterrissage sont composées de plusieurs composants, notamment la politique de sécurité, la gestion des identités et des accès (IAM), les pipelines d'automatisation, la politique organisationnelle, la mise en réseau, la journalisation et la surveillance. Une représentation visuelle peut être trouvée ci-dessous avec plus de détails offerts plus loin dans ce document et dans la documentation à l'appui.

![][image1]

Pour séparer les équipes et les piles technologiques responsables de la gestion des différentes couches de votre environnement, le code de déploiement a été séparé en différentes couches destinées à correspondre aux différents personnages responsables de votre environnement ([Lien vers la méthodologie de déploiement](https://cloud.google.com/architecture/security-foundations/deployment-methodology?hl=fr)). 

La zone d'accueil PBMM se compose de 7 étapes comme suit :

| Scène | Description |
| :---- | :---- |
| 0-bootstrap | Bootstrap prépare votre organisation Google Cloud aux étapes de déploiement suivantes. Cette étape configure également un pipeline CI/CD pour le code Blueprint dans les étapes suivantes. Configuration des comptes de service et des autorisations appropriés Le projet CICD contient le pipeline de base Cloud Build pour le déploiement de ressources. Le projet de départ inclut les buckets Cloud Storage qui contiennent l'état Terraform de l'infrastructure de base et inclut les comptes de service hautement privilégiés qui sont utilisés par le pipeline de base pour créer des ressources. L'état Terraform est protégé par le contrôle de version des objets de stockage. Lorsque le pipeline CI/CD s'exécute, il fait office de comptes de service gérés dans le projet initial. |
| 1-org | Configure les dossiers partagés de niveau supérieur, les projets pour les services partagés, la journalisation au niveau de l'organisation et les paramètres de sécurité de base via les stratégies d'organisation. |
| 2-environments | Configure les environnements de développement, de non-production et de production au sein de l'organisation Google Cloud que vous avez créée. |
| 3-networks | Configure les VPC partagés dans la topologie choisie et les ressources réseau associées. |
| 4-projects | Met en place une structure de dossiers pour les différentes unités commerciales, les projets de service dans chacun des environnements. Il existe des exemples de projets prêts à l'emploi et peuvent être ajustés pour répondre aux besoins de votre organisation.  |
| 5-app-infra | Déploie des projets de charge de travail avec une instance Compute Engine en utilisant le pipeline d'infrastructure comme exemple. |
| 6-org-policies | Une fois les politiques mises en œuvre au niveau d'une organisation, les développeurs peuvent utiliser le package « 6-org-policies » pour personnaliser les politiques, qu'elles soient nécessaires ou qu'elles doivent être remplacées au niveau spécifique de l'environnement. C’est là que de nombreuses politiques spécifiques Protégé B sont mises en place. |
| 7-fortifier | Installe une paire redondante d'appliances de sécurité Fortigate dans prj-net-hub-base, le VPC de transit de la zone d'accueil. |

#### *Exemple d'architecture avec les appliances Fortigate*

![][image2]

[Ressources Google Cloud](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=fr) sont organisés hiérarchiquement. Au niveau le plus bas, les ressources sont les composants fondamentaux qui composent tous les services Google Cloud. Des exemples de ressources incluent les machines virtuelles (VM) Compute Engine, les sujets Pub/Sub, les buckets Cloud Storage et les instances App Engine. Toutes ces ressources de niveau inférieur ne peuvent exister qu'au sein d'un projet. Un projet est le premier mécanisme de regroupement de la hiérarchie des ressources Google Cloud.

**Les dossiers sont un mécanisme de regroupement supplémentaire pour organiser les projets**. Vous devez disposer d’une ressource Organisation comme condition préalable pour utiliser les dossiers. Les dossiers et les projets sont tous mappés sous la ressource Organisation.

**La ressource Organisation est le nœud de niveau supérieur** de la hiérarchie des ressources Google Cloud et toutes les ressources appartenant à une organisation sont regroupées sous le nœud d'organisation. Cela offre une visibilité et un contrôle centralisés sur chaque ressource appartenant à une organisation. Le diagramme suivant montre les dossiers et les projets déployés dans le cadre du code de déploiement de la zone d'accueil PBMM.

![][image3]

# 2\. Condition préalable au déploiement <a name="condition-préalable-au-déploiement"></a>

Bien qu'une grande partie du déploiement de la zone d'accueil soit automatisée via des pipelines et du code Terraform, un certain nombre de conditions préalables sont requises pour réussir le déploiement et pour s'aligner sur les exigences de sécurité de Protégé B.

## 2.1 Configurer votre organisation  <a name="configurer-votre-organisation"></a>

Une ressource d'organisation dans Google Cloud représente votre entreprise et constitue le nœud de niveau supérieur de votre hiérarchie. Pour créer votre organisation, vous configurez un service d'identité Google et l'associez à votre domaine. Une fois ce processus terminé, une ressource d'organisation est automatiquement créée.  Des informations détaillées sur la création de votre organisation sortent du cadre de ce document et peuvent être trouvées [ici](https://cloud.google.com/resource-manager/docs/creating-managing-organization?hl=fr).

## 2.2 Authentification et autorisation <a name="authentification-et-autorisation"></a>

Google Cloud nécessite l'utilisation de Cloud Identity ou de Google Workspace afin de contrôler la gestion des identités et des accès au sein de la plate-forme cloud. À titre de bonne pratique, nous vous recommandons de fédérer votre compte Cloud Identity avec votre fournisseur d'identité existant. La fédération vous aide à garantir que vos processus de gestion de compte existants s'appliquent à Google Cloud et aux autres services Google. Si vous utilisez déjà Google Workspace, Cloud Identity utilise la même console, les mêmes contrôles d'administration et les mêmes comptes d'utilisateur que votre compte Google Workspace.

Le processus de fédération de l'identité n'est PAS couvert dans la base de code Terraform de la zone d'accueil PBMM, car il dépendra des besoins, des politiques et des pratiques d'approvisionnement spécifiques de chaque organisation. Il est fortement recommandé de terminer la fédération avant de procéder au déploiement d'une zone d'accueil. 

Le diagramme suivant présente une vue générale de la fédération d'identité et de l'authentification unique (SSO). Il utilise Microsoft Active Directory, situé dans l'environnement sur site, comme exemple de fournisseur d'identité.  
![][image4]

Le tableau suivant fournit des liens vers des conseils de configuration pour les fournisseurs d'identité.

| Fournisseur d'identité | Conseils |
| :---- | :---- |
| Identifiant de connexion Microsoft  (anciennement Azure AD) | [Fédérer Google Cloud avec Microsoft Entra ID](https://cloud.google.com/architecture/identity/federating-gcp-with-azure-active-directory?hl=fr) |
| Annuaire actif | [Provisionnement des comptes d'utilisateurs Active Directory](https://cloud.google.com/architecture/identity/federating-gcp-with-active-directory-synchronizing-user-accounts?hl=fr) [Authentification unique Active Directory](https://cloud.google.com/architecture/identity/federating-gcp-with-active-directory-configuring-single-sign-on?hl=fr) |
| Autres fournisseurs d'identité externes (par exemple, Ping ou Okta) | [Intégration des solutions d'identité Ping aux services d'identité Google](https://www.pingidentity.com/en/resources/content-library/white-papers/3034-integrate-ping-identity-solutions-google-identity-services.html) [Utiliser Okta avec les fournisseurs Google Cloud](https://www.okta.com/sites/default/files/UsingOktaWithGCP.pdf) [Bonnes pratiques pour fédérer Google Cloud avec un fournisseur d'identité externe](https://cloud.google.com/architecture/identity/best-practices-for-federating?hl=fr) |

Nous vous recommandons fortement d'appliquer l'authentification multifacteur auprès de votre fournisseur d'identité avec un mécanisme résistant au phishing tel qu'une [Clé de sécurité Titan](https://cloud.google.com/titan-security-key?hl=fr). 

Les paramètres recommandés pour Cloud Identity ne sont pas automatisés via le code Terraform dans ce plan. Voir [contrôles administratifs pour Cloud Identity](https://cloud.google.com/architecture/security-foundations/printable#administrative-controls-for-cloud-identity?hl=fr) pour les paramètres de sécurité recommandés que vous devez configurer en plus du déploiement du code Terraform.

## 2.3 Facturation <a name="facturation"></a>

De nombreuses agences et organisations gouvernementales ont déjà mis en place des relations d'approvisionnement avec Google Cloud, généralement sous la forme d'un compte de facturation.  En cas de doute, nous vous suggérons de commencer par votre service des achats ou des achats pour utiliser tous les véhicules existants.  Alternativement, vous pouvez [Demander un compte de facturation facturé](https://cloud.google.com/billing/docs/how-to/invoiced-billing?hl=fr) avec votre équipe commerciale Google Cloud ou créez un [compte de facturation en libre-service](https://cloud.google.com/billing/docs/how-to/create-billing-account?hl=fr) en utilisant une carte de crédit.

## 2.4 Autres considérations <a name="autres-considérations"></a>

Les éléments suivants sont recommandés à la fois comme meilleure pratique et pour garantir l’alignement avec toute exigence de contrôle de sécurité.

* Si vous utilisez un compte de facturation en libre-service, vous devez [demander un quota de projet supplémentaire](https://github.com/terraform-google-modules/terraform-example-foundation/blob/4d7e822b85d6c21c28389e82b3794b9e1554ebc6/docs/FAQ.md?plain=1#L9) avant de passer à l'étape suivante.  
* Imposer [bonnes pratiques de sécurité](https://support.google.com/a/answer/9011373?hl=fr) pour les comptes administrateur.  
* Vérifier et rapprocher [problèmes avec les comptes d'utilisateurs grand public](https://cloud.google.com/architecture/security-foundations/authentication-authorization#issues_with_consumer_user_accounts?hl=fr).

Pour vous connecter à un environnement sur site existant, préparez les éléments suivants :

* Planifiez votre [Attribution d'adresse IP](https://cloud.google.com/architecture/security-foundations/networking#ip-address-allocation?hl=fr) en fonction du nombre et de la taille des plages requises par le plan.  
* Commandez votre [Interconnexion dédiée](https://cloud.google.com/interconnect/docs/concepts/dedicated-overview?hl=fr) relations.

# 

# 3\. Étapes de déploiement de la zone d'accueil <a name="étapes-de-déploiement-de-la-zone-d'accueil"></a>

## Le bootstrap de l'environnement (0-bootstrap) <a name="le-bootstrap-de-l'environnement-"></a>

Le bootstrapping est le processus de configuration des ressources initiales pour un déploiement ultérieur dans le cloud. Le but de cette étape est de démarrer une organisation Google Cloud, en créant toutes les ressources et autorisations requises pour commencer à utiliser le code de la zone d'accueil PBMM. Cette étape peut également configurer un [Pipeline CI/CD](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/tef_0724_merged/docs/GLOSSARY.md#foundation-cicd-pipeline) pour les étapes ultérieures.  
Ce module configure la structure d'autorisations initiale sur le nœud d'organisation et active les services GCP de base tels que Google Cloud Storage afin qu'un référentiel puisse être instancié pour que Terraform valide et exécute le plan. 

Ceci est hébergé dans le sous-répertoire :   
../0-bootstrap/  
../automation-scripts/0-bootstrap/

## Organisation (1-org) <a name="organisation"></a>

Le but de cette étape est de configurer les dossiers partagés de niveau supérieur, les projets de surveillance et de mise en réseau, la journalisation au niveau de l'organisation et les paramètres de sécurité de base via les politiques de l'organisation.

Ceci est hébergé dans le sous-répertoire :   
../1-org/

## Environnements (2-environments) <a name="environnements"></a>

Le but de cette étape est de configurer des environnements de développement, de non-production et de production au sein de l'organisation Google Cloud que vous avez créée.

Ceci est hébergé dans le sous-répertoire :   
../2-environments/

## Réseaux (3-networks) <a name="réseaux"></a>

Le but de cette étape est de mettre en place le système global [Centre DNS](https://cloud.google.com/blog/products/networking/cloud-forwarding-peering-and-zones?hl=fr), par environnement Hubs et leurs rayons correspondants. Avec DNS par défaut, NAT (facultatif), mise en réseau de service privé, contrôles de service VPC, interconnexion dédiée ou partenaire sur site et règles de pare-feu de base pour chaque environnement.  
	  
Ceci est hébergé dans le sous-répertoire :   
../3-réseaux-hub-and-spoke/

## Projets (4-projects) <a name="projets"></a>

Le but de cette étape est de configurer la structure des dossiers, les projets et les pipelines d'infrastructure pour les applications connectées en tant que projets de service au VPC partagé créé à l'étape précédente.

Pour chaque unité commerciale, un projet d'infra-pipeline partagé est créé avec des déclencheurs Cloud Build, des référentiels sources cloud (CSR) pour le code d'infrastructure d'application et des buckets Google Cloud Storage pour le stockage d'état.

Cette étape suit la même [conventions](https://github.com/terraform-google-modules/terraform-example-foundation#branching-strategy) comme le pipeline Foundation déployé dans [0-bootstrap](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/0-bootstrap/README.md). Une coutume [espace de travail](https://github.com/terraform-google-modules/terraform-google-bootstrap/blob/master/modules/tf_cloudbuild_workspace/README.md) (bu1-example-app) est créé par ce pipeline et les rôles nécessaires sont accordés au compte de service Terraform de cet espace de travail en activant la variable sa\_roles comme indiqué dans ceci [exemple](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/4-projects/modules/base_env/example_base_shared_vpc_project.tf).

Ce pipeline est utilisé pour déployer des ressources dans des projets à travers les environnements, étape par étape [5-app-infra](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/tef_0724_merged/5-app-infra/README.md). Autre Espaces de travail peut également être créé pour isoler les déploiements si nécessaire.  
	  
Ceci est hébergé dans le sous-répertoire :   
../4-networks-hub-and-spoke/

## 

## Politiques organisationnelles (polices à 6 organisations) <a name="politiques-organisationnelles"></a>

[Contraintes de stratégie d'organisation](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints?hl=fr) appliquer la conformité au niveau de l'organisation, du dossier ou du projet GCP. Il s'agit d'un ensemble de règles prédéfinies qui empêchent certaines actions de se produire. Ces politiques intégrées sont définies par Google et activées par l'organisation qui utilise GCP. Ces politiques aident à protéger la limite de sécurité de la plateforme.

Au total, 26 politiques organisationnelles ont été mises en œuvre et les détails peuvent être trouvés dans le tableau ci-dessous.  

| Nom de la contrainte | Description de la contrainte | Références de contrôle |
| :---- | :---- | :---- |
| essentialcontacts.allowedContactDomains | Cette stratégie limite les contacts essentiels pour autoriser uniquement les identités d'utilisateurs gérés dans les domaines sélectionnés à recevoir des notifications de plateforme. | AC-2(4) |
| calculate.disableNestedVirtualization | Cette stratégie désactive la virtualisation imbriquée pour réduire les risques de sécurité dus aux instances imbriquées non surveillées. | AC-3, AC-6(9), AC-6(10) |
| calculate.disableSerialPortAccess | Cette stratégie empêche les utilisateurs d'accéder au port série de la VM qui peut être utilisé pour un accès par porte dérobée à partir du plan de contrôle de l'API Compute Engine. | AC-3, AC-6(9), AC-6(10) |
| calculate.requireOsLogin | Cette stratégie nécessite une connexion au système d'exploitation sur les machines virtuelles nouvellement créées pour gérer plus facilement les clés SSH, fournir une autorisation au niveau des ressources avec les stratégies IAM et enregistrer l'accès des utilisateurs. | AC-3, HE-12 |
| calculate.restrictVpcPeering | Vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP. | SC-7, SC-7(5), SC-7(7), SC-7(8), SC-7(18) |
| calculate.vmCanIpForward | Cette autorisation contrôle si une instance de VM peut agir comme un routeur réseau, transmettant des paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité.  | SC-7, SC-7(5), SC-7 (7), SC-7(8), SC-7(18), SC-8, SC-8(1) |
| calculate.restrictLoadBalancerCreationForTypes |  Cette autorisation vous permet de restreindre les types d'équilibreurs de charge pouvant être créés dans votre projet. Cela permet d'éviter la création non autorisée ou accidentelle d'équilibreurs de charge qui pourraient exposer vos services à des risques ou à des attaques inutiles. | SC-8, SC-8(1) |
| calculate.requireTlsForLoadBalancers | Cette contrainte impose l'utilisation de Transport Layer Security (TLS) pour la communication avec les équilibreurs de charge dans GCP. Il s'aligne sur plusieurs principes et contrôles clés décrits dans le NIST. | SC-8, SC-8(1) |
| calculate.skipDefaultNetworkCreation | Cette stratégie désactive la création automatique d'un réseau VPC par défaut et de règles de pare-feu par défaut dans chaque nouveau projet, garantissant ainsi que les règles de réseau et de pare-feu sont créées intentionnellement. | AC-3, AC-6(9), AC-6(10) |
| calculate.restrictXpnProjectLienRemoval | Cette stratégie empêche la suppression accidentelle des projets hôtes de VPC partagé en limitant la suppression des privilèges du projet. | AC-3, AC-6(9), AC-6(10) |
| calculate.disableVpcExternalIpv6 | Cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant. | AC-3, AC-6(9), AC-6(10) |
| calculate.setNewProjectDefaultToZonalDNSOly | Cette stratégie empêche les développeurs d'applications de choisir d'anciens paramètres DNS pour les instances Compute Engine dont la fiabilité du service est inférieure à celle des paramètres DNS modernes. | AC-3, AC-6(9), AC-6(10) |
| calculate.vmExternalIpAccess | Cette stratégie empêche la création d'instances Compute Engine avec une adresse IP publique, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant. | AC-3, AC-6(9), AC-6(10) |
| sql.restrictPublicIp | Cette stratégie empêche la création d'instances Cloud SQL avec des adresses IP publiques, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant. | AC-3, AC-6(9), AC-6(10) |
| sql.restrictAuthorizedNetworks | Cette stratégie empêche les plages de réseaux publics ou non RFC 1918 d'accéder aux bases de données Cloud SQL. | AC-3, AC-6(9), AC-6(10) |
| stockage.uniformBucketLevelAccess | Cette stratégie empêche les buckets Cloud Storage d'utiliser l'ACL par objet (un système distinct des stratégies IAM) pour fournir l'accès, garantissant ainsi la cohérence de la gestion des accès et de l'audit. | AC-3, AC-6(9), AC-6(10) |
| stockage.publicAccessPrevention | Cette stratégie empêche les buckets Cloud Storage d'être ouverts à un accès public non authentifié. | AC-3, AC-6(9), AC-6(10) |
| iam.disableServiceAccountKeyCreation | Cette contrainte empêche les utilisateurs de créer des clés persistantes pour les comptes de service afin de réduire le risque d'exposition des informations d'identification du compte de service. | AC-2(4) |
| iam.disableServiceAccountKeyUpload | Cette contrainte évite le risque de fuite et de réutilisation des éléments de clé personnalisés dans les clés de compte de service. | AC-6(9), AC-6(10) |
| iam.allowedPolicyMemberDomains | Cette stratégie limite les stratégies IAM pour autoriser uniquement les identités d'utilisateurs gérés dans les domaines sélectionnés à accéder aux ressources au sein de cette organisation. | AC-2(4) |
| computing.disableGuestAttributesAccess | Cette autorisation contrôle si un utilisateur ou un compte de service peut modifier les attributs d'invité sur une instance de machine virtuelle (VM). Les attributs d'invité peuvent contenir des métadonnées ou des données de configuration susceptibles d'avoir un impact sur la sécurité ou le fonctionnement de la VM. | AC-2(4) |
| iam.automaticIamGrantsForDefaultServiceAccounts | Cette contrainte empêche les comptes de service par défaut de recevoir le rôle d'éditeur de gestion des identités et des accès (IAM) trop permissif lors de la création. | AC-3 |
| calculate.trustedImageProjects | Cette contrainte permet de renforcer l’intégrité des logiciels et des micrologiciels ainsi que la gestion de la configuration. Cette autorisation contrôle quels projets peuvent être utilisés comme sources fiables pour les images de VM. En limitant cela à un ensemble sélectionné de projets, vous réduisez le risque de déployer des machines virtuelles à partir de sources non fiables ou potentiellement compromises. | SI-3 (2), SI-3 (7) |

Ceci est hébergé dans le sous-répertoire :   
../6-org-policies/

## Appliance virtuelle réseau (7-fortigate) <a name="appliance-virtuelle-réseau"></a>

Ce module peut être personnalisé pour prendre en charge les fournisseurs NGFW tiers ou [Le Cloud NGFW de Google](https://cloud.google.com/firewall/docs/about-firewalls?hl=fr). Cette implémentation est actuellement conçue et testée pour installer une paire redondante d'appliances de sécurité Fortigate dans prj-net-hub-base, le VPC de transit de la zone d'accueil, comme le montre le diagramme suivant.  
![][image5]  
Pour plus d'informations, consultez le document suivant pour un aperçu de l'architecture de [Renforcez les appliances sur GCP.](https://cloud.google.com/architecture/partners/fortigate-architecture-in-cloud?hl=fr)

Ceci est hébergé dans le sous-répertoire :   
../7-fortigate/

# 4\. Caractéristiques de la zone d'accueil <a name="caractéristiques-de-la-zone-d'accueil"></a>

La section se concentre en grande partie sur les fonctionnalités et les outils utilisés dans le cadre de la zone d'accueil et aborde certains des contrôles de sécurité mis en place dans le cadre d'un déploiement. 

La zone d'accueil utilise [projets](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects) pour regrouper des ressources individuelles en fonction de leurs fonctionnalités et des limites prévues pour le contrôle d'accès. Le tableau suivant décrit les projets inclus dans le plan.

| Dossier | Projet | Description |
| :---- | :---- | :---- |
| `bootstrap` | `prj-b-cicd` | Contient le pipeline de déploiement utilisé pour créer les composants de base de l’organisation. Pour plus d'informations, voir [méthodologie de déploiement](https://cloud.google.com/architecture/security-foundations/deployment-methodology?hl=fr). |
|  | `prj-b-seed` | Contient l'état Terraform de votre infrastructure et le compte de service Terraform requis pour exécuter le pipeline. Pour plus d'informations, voir [méthodologie de déploiement](https://cloud.google.com/architecture/security-foundations/deployment-methodology?hl=fr). |
| `common` | `prj-c-secrets` | Contient des secrets au niveau de l’organisation. Pour plus d'informations, voir [stocker les informations d'identification de l'application avec Secret Manager](https://cloud.google.com/architecture/security-foundations/operation-best-practices#store-and?hl=fr). |
|  | `prj-c-logging` | Contient les sources de journaux agrégées pour les journaux d’audit. Pour plus d'informations, voir [journalisation centralisée pour la sécurité et l'audit](https://cloud.google.com/architecture/security-foundations/detective-controls#centralized-logging?hl=fr). |
|  | `prj-c-scc` | Contient des ressources pour aider à configurer les alertes Security Command Center et d’autres surveillances de sécurité personnalisées. Pour plus d'informations, voir [surveillance des menaces avec Security Command Center](https://cloud.google.com/architecture/security-foundations/detective-controls#threat-monitoring?hl=fr). |
|  | `prj-c-billing-export` | Contient un ensemble de données BigQuery avec l'identité de l'organisation [facturation des exportations](https://cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=fr). Pour plus d'informations, voir [répartir les coûts entre les centres de coûts internes](https://cloud.google.com/architecture/security-foundations/operation-best-practices#allocate-costs?hl=fr). |
|  | `prj-c-infra-pipeline` | Contient un pipeline d'infrastructure pour déployer des ressources telles que des machines virtuelles et des bases de données à utiliser par les charges de travail. Pour plus d'informations, voir [couches de pipelines](https://cloud.google.com/architecture/security-foundations/deployment-methodology#pipeline-layers?hl=fr). |
|  | `prj-c-kms` | Contient les clés de chiffrement au niveau de l’organisation. Pour plus d'informations, voir [gérer les clés de chiffrement](https://cloud.google.com/architecture/security-foundations/operation-best-practices#manage-encryption?hl=fr). |
| `prj-networks` | `prj-net-hub-base` | Contient le projet hôte d'un réseau VPC partagé pour les charges de travail qui ne nécessitent pas VPC Service Controls. Pour plus d'informations, voir [topologie du réseau](https://cloud.google.com/architecture/security-foundations/networking#network_topology?hl=fr). |
|  | `prj-net-hub-restricted` | Contient le projet hôte d'un réseau VPC partagé pour les charges de travail qui nécessitent VPC Service Controls. Pour plus d'informations, voir [topologie du réseau](https://cloud.google.com/architecture/security-foundations/networking#network_topology?hl=fr). |
|  | `prj-net-interconnect` | Contient les connexions Cloud Interconnect qui assurent la connectivité entre votre environnement sur site et Google Cloud. Pour plus d'informations, voir [connectivité hybride](https://cloud.google.com/architecture/security-foundations/networking#hybrid-connectivity?hl=fr). |
|  | `prj-net-dns` | Contient des ressources pour un point central de communication entre votre système DNS sur site et Cloud DNS. Pour plus d'informations, voir [configuration DNS centralisée](https://cloud.google.com/architecture/security-foundations/networking#dns-setup?hl=fr). |
| `prj-{env}-secrets` | Contient des secrets au niveau du dossier. Pour plus d'informations, voir stocker et auditer les informations d'identification des applications avec Secret Manager. |  |
| `prj-{env}-kms` | Contient les clés de chiffrement au niveau du dossier. Pour plus d'informations, voir [gérer les clés de chiffrement](https://cloud.google.com/architecture/security-foundations/operation-best-practices?hl=fr#manage-encryption). |  |
| projets d'application | Contient divers projets dans lesquels vous créez des ressources pour les applications. Pour plus d'informations, voir [modèles de déploiement de projet](https://cloud.google.com/architecture/security-foundations/networking?hl=fr#project_deployment_patterns) et [couches de pipelines](https://cloud.google.com/architecture/security-foundations/deployment-methodology?hl=fr#pipeline-layers). |  |

## 4.1 Gestion des identités et des accès (IAM) <a name="gestion-des-identités-et-des-accès"></a>

Google Cloud Identity est le produit utilisé pour gérer les utilisateurs, les groupes et les paramètres de sécurité à l'échelle du domaine pour Workspace et Google Cloud Platform. Cloud Identity est lié à un domaine DNS unique qui doit être activé pour la réception d'e-mails (par exemple, un MX approprié est configuré) afin que les utilisateurs et les groupes configurés avec des responsabilités dans GCP puissent recevoir les notifications générées.

Les configurations Cloud Identity sont effectuées dans la console d'administration. Les clients Workspace existants peuvent utiliser leur console d'administration Workspace pour Cloud Identity. Les clients sans compte Workspace existant peuvent créer une Cloud Identity dans la section "IAM" de GCP Cloud Console.

Les stratégies IAM peuvent être configurées dans Google Cloud Console. Les rôles IAM sont disponibles pour les utilisateurs, les groupes d'utilisateurs et les comptes de service qui permettent un contrôle granulaire des autorisations d'accès aux ressources. La ressource d'organisation permet d'unifier tous les projets sous une seule organisation avec héritage des autorisations dans toute l'organisation. 

Identity Aware Proxy (IAP) fournit un proxy authentifié qui vérifie toutes les connexions par rapport à une politique de contrôle d'accès (voir [Référence : Proxy prenant en compte l'identité](https://cloud.google.com/iap/docs/concepts-overview?hl=fr)). Il peut être utilisé pour accéder aux ressources d'un VPC où le système source n'a pas de route vers le système de destination, ou où une règle de pare-feu bloque l'accès direct. Toutes les connexions via IAP doivent s'authentifier et, une fois authentifiées, seront acheminées vers le service de destination où elles pourront interagir avec lui. Cette interaction peut être un simple trafic TCP tel qu'un service Web, ou plus complexe comme une session RDP ou SSH où un identifiant pour accéder au système serait également requis. Tout le trafic IAP est crypté via TLS.

L'accès est contrôlé via les rôles IAM et est attribué directement aux groupes, utilisateurs ou comptes de service. Cela permet une granularité dans le contrôle de l'accès aux systèmes et garantit que le principe du moindre privilège est respecté. Ainsi, au lieu de gérer les hôtes bastions, les clés SSH et d’autres composants pouvant entraîner une charge opérationnelle, la Landing Zone tirera parti des capacités IAP.

## 4.3 Réseaux Hub et Spoke <a name="réseaux-hub-et-spoke"></a>

L’infrastructure mondiale de Google se compose de régions et, au sein de ces régions, de zones. Google propose plusieurs options de connectivité pour la connectivité physique via le peering direct ou Google Carrier Interconnect dans plusieurs zones géographiques. Des réseaux privés virtuels peuvent être construits au-dessus de cette couche physique et le Cloud Router est disponible pour gérer les routes dynamiques à l'aide de BGP une fois cette connexion configurée. L'utilisation de VPC partagés vous permet de centraliser l'infrastructure réseau dans un seul projet hôte et de permettre à d'autres projets de service de consommer les ressources réseau du projet hôte. 

La conception de la zone d'accueil PBMM utilise une topologie de réseau en étoile.

![][image6]

* Ce modèle ajoute un réseau hub, et chacun des réseaux de développement, de non-production et de production (rayons) est connecté au réseau hub via l'appairage de réseaux VPC. Alternativement, si vous prévoyez de dépasser la limite de quota d'appairage VPC (25), vous pouvez utiliser une passerelle VPN HA à la place.  
* La connectivité aux réseaux sur site est autorisée uniquement via le réseau hub. Tous les réseaux satellites peuvent communiquer avec les ressources partagées du réseau hub et utiliser ce chemin pour se connecter aux réseaux sur site.  
* Les réseaux hub incluent une appliance virtuelle réseau (NVA) pour chaque région, déployée de manière redondante derrière les instances internes de Network Load Balancer. Cette NVA sert de passerelle pour autoriser ou refuser la communication du trafic entre les réseaux satellites.  
* Le réseau hub héberge également des outils qui nécessitent une connectivité à tous les autres réseaux. Par exemple, vous pouvez déployer des outils sur des instances de VM pour la gestion de la configuration dans l'environnement commun.  
* Le modèle en étoile est dupliqué pour une version de base et une version restreinte de chaque réseau.

Pour activer le trafic de rayon à rayon, le plan déploie des NVA sur le réseau hub Shared VPC qui agissent comme des passerelles entre les réseaux. Les routes sont échangées à partir des réseaux VPC hub-to-spoke via un échange de routes personnalisées. Dans ce scénario, la connectivité entre les satellites doit être acheminée via la NVA, car l'appairage de réseaux VPC n'est pas transitif et, par conséquent, les réseaux VPC satellite ne peuvent pas échanger de données directement entre eux. Vous devez configurer les appareils virtuels pour autoriser de manière sélective le trafic entre les rayons.

## 

## 4.4DNS <a name="dns"></a>

Cloud DNS prend en charge les zones publiques (résolvables sur Internet) et privées (voir [Référence : Présentation du DNS](https://cloud.google.com/dns/docs/overview?hl=fr)). Pour la résolution DNS entre Google Cloud et les environnements sur site, nous vous recommandons d'utiliser une approche hybride avec deux systèmes DNS faisant autorité. Dans cette approche, Cloud DNS gère la résolution DNS faisant autorité pour votre environnement Google Cloud et vos serveurs DNS sur site existants gèrent la résolution DNS faisant autorité pour les ressources sur site. Votre environnement sur site et votre environnement Google Cloud effectuent des recherches DNS entre les environnements via des requêtes de transfert.

Le diagramme suivant illustre la topologie DNS sur les multiples réseaux VPC utilisés dans la zone d'accueil.

![][image7]

* Le projet de hub DNS dans le dossier commun est le point central de l'échange DNS entre l'environnement sur site et l'environnement Google Cloud. Le transfert DNS utilise les mêmes instances d'interconnexion dédiées et les mêmes routeurs cloud que ceux déjà configurés dans la topologie de votre réseau.  
  * Dans la topologie VPC partagé double, le hub DNS utilise le réseau VPC partagé de production de base.  
  * Dans la topologie hub-and-spoke, le hub DNS utilise le réseau VPC partagé du hub de base.  
* Les serveurs de chaque réseau VPC partagé peuvent résoudre les enregistrements DNS d'autres réseaux VPC partagés via [Redirection DNS](https://cloud.google.com/dns/docs/overview#dns-forwarding-methods?hl=fr), qui est configuré entre Cloud DNS dans chaque projet hôte de VPC partagé et le hub DNS.  
* Les serveurs sur site peuvent résoudre les enregistrements DNS dans les environnements Google Cloud à l'aide [Politiques du serveur DNS](https://cloud.google.com/dns/docs/best-practices?hl=fr#use_dns_server_policies_to_allow_queries_from_on-premises) qui autorisent les requêtes à partir de serveurs sur site. Le modèle configure une stratégie de serveur entrant dans le hub DNS pour allouer des adresses IP, et les serveurs DNS sur site transmettent les demandes à ces adresses. Toutes les requêtes DNS adressées à Google Cloud atteignent d'abord le hub DNS, qui résout ensuite les enregistrements des homologues DNS.  
* Les serveurs de Google Cloud peuvent résoudre les enregistrements DNS dans l'environnement sur site à l'aide [zones de transfert](https://cloud.google.com/dns/docs/best-practices?hl=fr#use_forwarding_zones_to_query_on-premises_servers) qui interrogent les serveurs sur site. Toutes les requêtes DNS adressées à l'environnement sur site proviennent du hub DNS. La source de la requête DNS est 35.199.192.0/19.

## 4.5 Pare-feu Politiques <a name="pare-feu-politiques"></a>

Google Cloud propose plusieurs [politique de pare-feu](https://cloud.google.com/firewall/docs/firewall-policies-overview?hl=fr). Les stratégies de pare-feu hiérarchiques sont appliquées au niveau de l'organisation ou du dossier pour hériter des règles de stratégie de pare-feu de manière cohérente sur toutes les ressources de la hiérarchie. De plus, vous pouvez configurer des stratégies de pare-feu réseau pour chaque réseau VPC. La zone d'accueil combine ces stratégies de pare-feu pour appliquer des configurations communes dans tous les environnements à l'aide de stratégies de pare-feu hiérarchiques et pour appliquer des configurations plus spécifiques sur chaque réseau VPC individuel à l'aide de stratégies de pare-feu réseau.

### Politiques de pare-feu hiérarchiques

Le plan définit une seule [politique de pare-feu hiérarchique](https://cloud.google.com/firewall/docs/firewall-policies?hl=fr) et attache la stratégie à chacun des dossiers de production, de non-production, de développement, d'amorçage et commun. Cette stratégie de pare-feu hiérarchique contient les règles qui doivent être appliquées largement dans tous les environnements et délègue l'évaluation de règles plus granulaires à la stratégie de pare-feu réseau pour chaque environnement individuel.

Le tableau suivant décrit les règles de stratégie de pare-feu hiérarchique déployées par la zone d'accueil.

| Description de la règle | Sens de circulation | Filtre (plage IPv4) | Protocoles et ports | Action |
| :---- | :---- | :---- | :---- | :---- |
| Déléguez l’évaluation du trafic entrant de la RFC 1918 aux niveaux inférieurs de la hiérarchie. | Ingress | 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 | tous | Aller au suivant |
| Déléguez l’évaluation du trafic sortant à la RFC 1918 aux niveaux inférieurs de la hiérarchie. | Egress | 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 | tous | Aller au suivant |
| [IAP pour le transfert TCP](https://cloud.google.com/iap/docs/using-tcp-forwarding?hl=fr) | Ingress | 35.235.240.0/20 | TCP : 22,3390 | Permettre |
| [Activation du serveur Windows](https://cloud.google.com/compute/docs/instances/windows/creating-managing-windows-instances?hl=fr) | Egress | 35.190.247.13/32 | TCP : 1688 | Permettre |
| [Bilans de santé](https://cloud.google.com/load-balancing/docs/health-checks?hl=fr#fw-rule) pour l'équilibrage de charge cloud | Ingress | 130.211.0.0/22, 35.191.0.0/16, 209.85.152.0/22, 209.85.204.0/22 | TCP : 80 443 | Permettre |

### Politiques de pare-feu réseau

La zone d'accueil configure une politique [de pare-feu réseau](https://cloud.google.com/vpc/docs/network-firewall-policies?hl=fr) pour chaque réseau. Chaque stratégie de pare-feu réseau commence par un ensemble minimum de règles qui autorisent l'accès aux services Google Cloud et refusent la sortie vers toutes les autres adresses IP.

Dans le modèle hub-and-spoke, les politiques de pare-feu réseau contiennent des règles supplémentaires pour permettre la communication entre les rayons. La stratégie de pare-feu réseau autorise le trafic sortant de l'un vers le hub ou un autre rayon, et autorise le trafic entrant depuis la NVA dans le réseau hub.

Le tableau suivant décrit les règles de la stratégie de pare-feu réseau globale déployée pour chaque réseau VPC dans la zone d'accueil.

| Description de la règle | Sens de circulation | Filtre | Protocoles et ports |
| :---- | :---- | :---- | :---- |
| Autorisez le trafic sortant vers les API Google Cloud. | Egress | Point de terminaison Private Service Connect configuré pour chaque réseau individuel. Voir [Accès privé aux API Google](https://cloud.google.com/architecture/security-foundations/networking#private-access-to-google-cloud-apis?hl=fr). | TCP : 443 |
| Refuser le trafic sortant qui ne correspond pas à d’autres règles. | Egress | tous | tous |
| Autorisez le trafic sortant d’un rayon à un autre (pour le modèle hub-and-spoke uniquement). | Egress | Regroupement de toutes les adresses IP utilisées dans la topologie hub-and-spoke. Le trafic qui quitte un VPC satellite est d'abord acheminé vers la NVA dans le réseau hub. | tous |
| Autorisez le trafic entrant vers un rayon depuis la NVA dans le réseau hub (pour le modèle hub-and-spoke uniquement). | Ingress | Trafic provenant des NVA du réseau hub. | tous |

Lorsque vous déployez le plan pour la première fois, une instance de VM dans un réseau VPC peut communiquer avec les services Google Cloud, mais pas avec d'autres ressources d'infrastructure dans le même réseau VPC. Pour permettre aux instances de VM de communiquer, vous devez ajouter des règles supplémentaires à votre stratégie de pare-feu réseau et [balises](https://cloud.google.com/resource-manager/docs/tags/tags-overview?hl=fr) qui permettent explicitement aux instances de VM de communiquer. Les balises sont ajoutées aux instances de VM et le trafic est évalué par rapport à ces balises. Les balises disposent en outre de contrôles IAM afin que vous puissiez les définir de manière centralisée et déléguer leur utilisation à d'autres équipes.

## 4.6 Pare-feu Fortigate : 2 appliances <a name="pare-feu-fortigate"></a>

Ce module optionnel est disponible si un dispositif de pare-feu Fortigate est souhaité. Ce type de pare-feu NVA fournira des fonctionnalités comprenant, sans s'y limiter :

* Inspection approfondie des paquets  
* Capacités IDS  
* Capacités WAF  
* Filtrage du nom de domaine complet

S’il est utilisé, tout le trafic passera d’abord par l’appliance virtuelle, avant de sortir vers l’Internet public. Le trafic destiné à l'environnement sur site transitera également par la NVA avant de sortir vers l'environnement sur site. Pour faciliter cela, la zone d'accueil utilise [Routage basé sur des politiques](https://cloud.google.com/vpc/docs/policy-based-routes?hl=fr) afin de diriger le trafic à travers les VM du pare-feu. 

## 4.7 Contrôles des services VPC <a name="contrôles-des-services-vpc"></a>

Cette zone d'accueil aide à préparer votre environnement pour VPC Service Controls en séparant les réseaux de base et restreints. Cependant, par défaut, le code Terraform n'active pas VPC Service Controls, car cette activation peut constituer un processus perturbateur. Pour activer les réseaux restreints, il y a un indicateur dans les variables du dossier *3-networks*.

Un périmètre refuse l'accès aux services Google Cloud restreints au trafic provenant de l'extérieur du périmètre, qui comprend la console, les postes de travail des développeurs et le pipeline de base utilisé pour déployer les ressources. Si vous utilisez VPC Service Controls, vous devez concevoir des exceptions au périmètre qui autorisent les chemins d'accès souhaités.

Un périmètre VPC Service Controls est destiné aux contrôles d'exfiltration entre votre organisation Google Cloud et des sources externes. Le périmètre n’est pas destiné à remplacer ou à dupliquer les politiques d’autorisation pour un contrôle d’accès granulaire à des projets ou des ressources individuels. Pour [concevoir  un périmètre](https://cloud.google.com/vpc-service-controls/docs/architect-perimeters?hl=fr), nous vous recommandons d'utiliser un périmètre unifié commun pour réduire les frais de gestion.

## 4.8 Journalisation centralisée <a name="journalisation-centralisée"></a>

La surveillance et la journalisation dans GCP sont assurées par deux produits différents, Cloud Monitoring (voir [Référence : Surveillance du cloud](https://cloud.google.com/monitoring/docs/monitoring-overview?hl=fr)) et Cloud Logging (voir [Référence : Cloud Logging](https://cloud.google.com/logging/docs?hl=fr)). Ces services GCP, en conjonction avec Security Command Center, permettent une vue globale de l'état des ressources dans tous les projets GCP. 

La zone d'accueil configure les fonctionnalités de journalisation pour suivre et analyser les modifications apportées à vos ressources Google Cloud avec des journaux regroupés dans un seul projet.

Le diagramme suivant montre comment le plan regroupe les journaux provenant de plusieurs sources dans plusieurs projets dans un récepteur de journaux centralisé.

![][image8]

* Les récepteurs de journaux sont configurés au niveau du nœud d'organisation pour regrouper les journaux de tous les projets de la hiérarchie des ressources.  
* Plusieurs récepteurs de journaux sont configurés pour envoyer les journaux correspondant à un filtre vers différentes destinations à des fins de stockage et d'analyse.  
* Le projet prj-c-logging contient toutes les ressources pour le stockage et l'analyse des journaux.  
* En option, vous pouvez configurer des outils supplémentaires pour exporter les journaux vers un SIEM.

## 4.9 Security Commande Center <a name="security-commande-center"></a>

Nous vous recommandons fortement d'activer [Security Command Center Premium](https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview?hl=fr) pour votre organisation, car il joue un rôle essentiel dans la conformité en détectant les menaces, les vulnérabilités et les erreurs de configuration dans vos ressources Google Cloud. Security Command Center crée des résultats de sécurité à partir de plusieurs sources, notamment :

* [Analyse de l'état de la sécurité](https://cloud.google.com/security-command-center/docs/how-to-use-security-health-analytics?hl=fr) : détecte les vulnérabilités courantes et les erreurs de configuration dans les ressources Google Cloud.

* [Exposition au chemin d'attaque](https://cloud.google.com/security-command-center/docs/attack-exposure-learn?hl=fr): montre un chemin simulé de la manière dont un attaquant pourrait exploiter vos ressources de grande valeur, en fonction des vulnérabilités et des erreurs de configuration détectées par d'autres sources de Security Command Center.

* [Détection des menaces d'événements](https://cloud.google.com/security-command-center/docs/how-to-use-event-threat-detection?hl=fr): applique une logique de détection et des renseignements exclusifs sur les menaces à vos journaux pour identifier les menaces en temps quasi réel.

* [Détection des menaces liées aux conteneurs](https://cloud.google.com/security-command-center/docs/how-to-use-container-threat-detection?hl=fr): détecte les attaques courantes d'exécution de conteneur.

* [Détection des menaces des machines virtuelles](https://cloud.google.com/security-command-center/docs/how-to-use-vm-threat-detection?hl=fr): détecte les applications potentiellement malveillantes qui s'exécutent sur les machines virtuelles.

* [Scanner de sécurité Web](https://cloud.google.com/security-command-center/docs/how-to-use-web-security-scanner?hl=fr): recherche les dix principales vulnérabilités OWASP dans vos applications Web sur Compute Engine, App Engine ou Google Kubernetes Engine.

Pour plus d'informations sur les vulnérabilités et les menaces traitées par Security Command Center, voir [Sources du centre de commande de sécurité](https://cloud.google.com/security-command-center/docs/concepts-security-sources?hl=fr).

Vous devez activer Security Command Center après avoir déployé la zone d'accueil. Pour les instructions, voir [Activer Security Command Center pour une organisation](https://cloud.google.com/security-command-center/docs/activate-scc-for-an-organization?hl=fr).

Après avoir activé Security Command Center, nous vous recommandons d'exporter les résultats produits par Security Command Center vers vos outils ou processus existants pour trier et répondre aux menaces. Le plan crée le projet prj-c-scc avec un sujet Pub/Sub à utiliser pour cette intégration. En fonction de vos outils existants, utilisez l'une des méthodes suivantes pour exporter les résultats :

* Si vous utilisez la console pour gérer les résultats de sécurité directement dans Security Command Center, configurez [rôles au niveau du dossier et du projet](https://cloud.google.com/security-command-center/docs/access-control-org#folder-level_and_project-level_roles?hl=fr) pour Security Command Center afin de permettre aux équipes de visualiser et de gérer les résultats de sécurité uniquement pour les projets dont elles sont responsables.

* Si vous utilisez Google SecOps comme SIEM, suivez cet article : [ingérer des données Google Cloud dans Google SecOps](https://cloud.google.com/chronicle/docs/ingestion/cloud/ingest-gcp-logs?hl=fr).

* Si vous utilisez un outil SIEM ou SOAR avec des intégrations à Security Command Center, lisez les articles pertinents suivants : [Cortex XSOAR](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-cortex-xsoar?hl=fr), [Pile élastique](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-elastic-stack-docker?hl=fr), [Service Mandiant](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-servicenow?hl=fr), [Splunk](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-splunk?hl=fr), ou [QRadar](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-qradar?hl=fr).

* Si vous utilisez un outil externe capable d'ingérer les résultats de Pub/Sub, configurez [exportations continues](https://cloud.google.com/security-command-center/docs/how-to-export-data?hl=fr#continuous_exports) vers Pub/Sub et configurez vos outils existants pour ingérer les résultats du sujet Pub/Sub.

## 4.10 Gestion des secrets <a name="gestion-des-secrets"></a>

Nous vous recommandons de ne jamais confier de secrets sensibles tels que des clés API, des mots de passe et des certificats privés aux référentiels de code source. Confier le secret à [Gestionnaire de secrets](https://cloud.google.com/secret-manager/docs/overview?hl=fr) et accorder le [Accesseur secret Secret Manager](https://cloud.google.com/secret-manager/docs/access-control?hl=fr#secretmanager.secretAccessor) Rôle IAM pour l'utilisateur ou le compte de service qui doit accéder au secret. Nous vous recommandons d'accorder le rôle IAM à un secret individuel, et non à tous les secrets du projet.

Lorsque cela est possible, vous devez générer automatiquement des secrets de production dans les pipelines CI/CD et les garder inaccessibles aux utilisateurs humains, sauf en cas de bris de glace. Dans ce scénario, assurez-vous de ne pas accorder de rôles IAM pour afficher ces secrets à des utilisateurs ou à des groupes.

La zone d'accueil offre un seul *prj-c-secrets* projet dans le dossier commun et un *prj-{env}-secrets* projet dans chaque dossier d’environnement pour gérer les secrets de manière centralisée. Cette approche permet à une équipe centrale d'auditer et de gérer les secrets utilisés par les applications afin de répondre aux exigences réglementaires et de conformité.

En fonction de votre modèle opérationnel, vous préférez peut-être une seule instance centralisée de Secret Manager sous le contrôle d'une seule équipe, ou vous préférez peut-être gérer les secrets séparément dans chaque environnement, ou vous préférez peut-être plusieurs instances distribuées de Secret Manager afin que chaque charge de travail l'équipe peut gérer ses propres secrets. Modifiez l'exemple de code Terraform si nécessaire pour l'adapter à votre modèle opérationnel.

Les opérateurs de plateforme doivent avoir accès aux secrets au niveau du projet dans les projets gérés par l’équipe de plateforme, mais ils ne doivent pas avoir accès aux secrets d’application. Les opérateurs d'applications auront accès à la gestion des secrets d'application, ce qui inclut la création, la mise à jour ou la mise hors service de secrets dans Secrets Manager. En plus de cela, les propres comptes de service de l’application auront accès aux versions individuelles de secret/secret, mais ces comptes de service ne pourront lire aucun autre secret.

Secrets Manager dispose d'un chiffrement au repos par défaut à l'aide des clés de chiffrement gérées par Google. L'option permettant d'utiliser des clés de chiffrement gérées par le client est également disponible et recommandée (voir [Référence : Secrets Manager \- Clés de chiffrement gérées par le client](https://cloud.google.com/secret-manager/docs/cmek?hl=fr)).

# 

# 5\. Options de déploiement de la zone d'accueil <a name="options-de-déploiement-de-la-zone-d'accueil"></a>

Il existe quelques options pour déployer la zone d'accueil Protégée B qui peuvent être envisagées en fonction du futur modèle opérationnel souhaité et des préférences technologiques d’une organisation. Nous vous recommandons d'utiliser une infrastructure déclarative pour déployer votre fondation de manière cohérente et contrôlable. Cette approche permet de permettre une gouvernance cohérente en appliquant des contrôles de stratégie sur les configurations de ressources acceptables dans vos pipelines. 

## 5.1 Création du cloud <a name="création-du-cloud"></a>

Dans ce modèle, la zone d'accueil est déployée à l'aide d'un flux GitOps avec Terraform utilisé pour définir l'infrastructure en tant que code (IaC), un référentiel Git pour le contrôle de version et l'approbation du code, et Cloud Build pour l'automatisation CI/CD dans le pipeline de déploiement. Les commits Terraform sont récupérés par Cloud Build et une opération de « planification » Terraform est effectuée pour planifier l'impact sur l'environnement. Les modifications Terraform fusionnées dans la branche principale du référentiel d'amorçage sont récupérées par Cloud Build et une opération « appliquer » Terraform est effectuée.

## 5.2 Déploiement manuel <a name="déploiement-manuel"></a>

Ce mode de déploiement, vous devrez déployer chacune des 7 étapes individuelles à la main.  Vous utiliserez toujours Terraform comme infrastructure en tant que moteur de code, mais les étapes de planification et d'application de Terraform devront être exécutées dans les différents répertoires liés aux différentes étapes de 1 à 7\.

Un lien vers les instructions de déploiement spécifiques peut être trouvé ci-dessous.  
[Manual PBMM Installation](https://docs.google.com/document/d/1iF-y9kQwVk4xs0bNhdX6kogHU-b8b1BbWl6AdbCJAUY/edit?usp=sharing)

## 5.3 Pipeline Devops Azure <a name="5.3-pipeline-devops-azure"></a>

Approche similaire au modèle Cloud Build décrit ci-dessus, mais cette méthode est destinée aux organisations qui préfèrent utiliser Azure DevOps comme déploiement préféré.

Un lien vers les instructions de déploiement spécifiques peut être trouvé ci-dessous :  
[ADO Pipeline Documentation](https://docs.google.com/document/d/1gnbcEDA070Cqey-0-bO7KxMvOTcxTuZd-QNmBrceEmA/edit?usp=sharing&resourcekey=0-c_rRkhdtnYWl8P8683zPIw)

# Tâches du jour 2 et meilleures pratiques opérationnelles <a name="tâches-du-jour-2-et-meilleures-pratiques-opérationnelles"></a>

## Après le déploiement d'IAC <a name="après-le-déploiement-d'iac"></a>

Une fois votre code Terraform terminé, vous devez effectuer les étapes supplémentaires suivantes afin de terminer votre configuration et garantir le plus haut niveau de conformité.

* Complétez les [modifications de la configuration sur site](https://cloud.google.com/architecture/security-foundations/networking?hl=fr#on-premises_configuration_changes).  
* [Activer Security Command Center Premium](https://cloud.google.com/security-command-center/docs/activate-scc-overview?hl=fr).  
* [Exporter les données de facturation Cloud vers BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=fr).  
* Inscrivez-vous à un [Plan de service client cloud](https://cloud.google.com/support?hl=fr).  
* [Activer la transparence des accès](https://cloud.google.com/assured-workloads/access-transparency/docs/enable?hl=fr) journaux.  
* [Partager des données de Cloud Identity avec Google Cloud](https://support.google.com/a/answer/9320190?hl=fr).

 

## Meilleures pratiques opérationnelles <a name="meilleures-pratiques-opérationnelles"></a>

### Stratégie de branchement pour vos dépôts IAC

Après le déploiement, vous disposerez de 7 dépôts correspondant aux étapes ci-dessus. Les modifications et ajouts à votre infrastructure doivent être effectués via du code. Nous recommandons une maintenance continue de votre infrastructure, car le code doit suivre les meilleures pratiques décrites ci-dessous. 

Nous recommandons une stratégie de [branche persistante](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)  pour soumettre du code à votre système Git et déployer des ressources via le pipeline de fondation. Le diagramme suivant décrit la stratégie de branche persistante.

Le diagramme ci-dessous montre trois branches persistantes dans Git (développement, non-production et production) qui reflètent les environnements Google Cloud correspondants. Il existe également plusieurs branches de fonctionnalités éphémères qui ne correspondent pas aux ressources déployées dans vos environnements Google Cloud.

![][image9]

Nous vous recommandons d'appliquer un processus de [demande de tirage (PR)](https://git-scm.com/docs/git-request-pull) dans votre système Git afin que tout code fusionné dans une branche persistante ait un PR approuvé.

Pour développer du code avec cette stratégie de branche persistante, suivez ces étapes générales :

1. Lorsque vous développez de nouvelles fonctionnalités ou travaillez sur une correction de bug, créez une nouvelle branche basée sur la branche de développement. Utilisez une convention de dénomination pour votre succursale qui inclut le type de changement, un numéro de ticket ou un autre identifiant, ainsi qu'une description lisible par l'homme, comme feature/123456-org-policies.

2. Lorsque vous avez terminé le travail dans la branche des fonctionnalités, ouvrez un PR qui cible la branche de développement.

3. Lorsque vous soumettez le PR, le PR déclenche le pipeline de fondation pour exécuter un plan Terraform et une validation Terraform pour organiser et vérifier les modifications.

4. Après avoir validé les modifications apportées au code, fusionnez la fonctionnalité ou le correctif de bogue dans la branche de développement.

5. Le processus de fusion déclenche l'exécution de Terraform Apply par le pipeline de base pour déployer les dernières modifications de la branche de développement dans l'environnement de développement.

6. Examinez les modifications apportées à l'environnement de développement à l'aide de révisions manuelles, de tests fonctionnels ou de tests de bout en bout pertinents pour votre cas d'utilisation. Promouvez ensuite les modifications apportées à l'environnement de non-production en ouvrant un PR qui cible la branche de non-production et fusionnez vos modifications.

7. Pour déployer des ressources dans l'environnement de production, répétez le même processus qu'à l'étape 6 : examinez et validez les ressources déployées, ouvrez un PR vers la branche de production et fusionnez.

### Utilisez le portefeuille Active Assist

En plus de l'outil de recommandation IAM, Google Cloud fournit l' Assistance [active](https://cloud.google.com/solutions/active-assist?hl=fr) de portefeuille de services pour formuler des recommandations sur la manière d'optimiser votre environnement. Par exemple, [informations sur le pare-feu](https://cloud.google.com/network-intelligence-center/docs/firewall-insights/how-to/using-firewall-insights?hl=fr) ou le [recommandeur de projet sans surveillance](https://cloud.google.com/recommender/docs/unattended-project-recommender?hl=fr) fournissent des recommandations concrètes qui peuvent vous aider à renforcer votre posture de sécurité.

Concevez un processus pour examiner périodiquement les recommandations ou appliquer automatiquement les recommandations dans vos pipelines de déploiement. Décidez quelles recommandations doivent être gérées par une équipe centrale et lesquelles doivent relever de la responsabilité des propriétaires de charges de travail, et appliquez des rôles IAM pour accéder aux recommandations en conséquence.

### Accorder des exceptions aux règles de l'organisation

Le modèle applique un ensemble de contraintes de stratégie d'organisation qui sont recommandées à la plupart des clients dans la plupart des scénarios, mais vous pouvez avoir des cas d'utilisation légitimes qui nécessitent des exceptions limitées aux stratégies d'organisation que vous appliquez de manière générale.

Par exemple, le plan applique le [iam.disableServiceAccountKeyCreation](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts?hl=fr#disable_service_account_key_creation) contrainte. Cette contrainte constitue un contrôle de sécurité important, car une fuite de clé de compte de service peut avoir un impact négatif important, et la plupart des scénarios devraient utiliser [des alternatives plus sécurisées aux clés de compte de service](https://cloud.google.com/docs/authentication?hl=fr#auth-decision-tree) pour authentifier. Cependant, il peut y avoir des cas d'utilisation qui ne peuvent s'authentifier qu'avec une clé de compte de service, comme un serveur sur site qui nécessite un accès aux services Google Cloud et ne peut pas utiliser la fédération d'identité de charge de travail. Dans ce scénario, vous pouvez décider d'autoriser une exception à la politique, à condition que des contrôles compensatoires supplémentaires tels que [bonnes pratiques pour la gestion des clés de compte de service](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys?hl=fr) sont appliquées.

Par conséquent, vous devez concevoir un processus permettant aux charges de travail de demander une exception aux politiques et vous assurer que les décideurs chargés d'accorder les exceptions disposent des connaissances techniques nécessaires pour valider le cas d'utilisation et se consulter pour savoir si des contrôles supplémentaires doivent être mis en place pour compenser. Lorsque vous accordez une exception à une charge de travail, modifiez la contrainte de stratégie d'organisation aussi étroitement que possible. Vous pouvez également [ajouter conditionnellement des contraintes à une stratégie d'organisation](https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy?hl=fr#conditionally_add_constraints_to_organization_policy) en définissant une balise qui accorde une exception ou une application de la stratégie, puis en appliquant la balise aux projets et aux dossiers.

# Annexe 1 : Nomenclature <a name="annexe-1"></a>

Nous vous recommandons d'avoir une convention de dénomination standardisée pour vos ressources Google Cloud. Le tableau suivant décrit les conventions recommandées pour les noms de ressources dans le Blueprint.

| Type de ressource | Convention de dénomination |
| :---- | :---- |
| Dossier | `fldr-environment` environment est une description des ressources au niveau du dossier au sein de l'organisation Google Cloud. Par exemple, bootstrap, commun, production, non-production, développement, ou réseau. Par exemple: `fldr-production` |
| ID du projet | `prj-environmentcode-description-randomid` environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet). Les projets hôtes de VPC partagé utilisent le code d'environnement de l’environnement associé. Projets de mise en réseau de ressources partagées entre environnements, comme le interconnexion projet, utilisez le filet code de l'environnement. description contient des informations supplémentaires sur le projet. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. randomid est un suffixe aléatoire pour éviter les collisions pour les noms de ressources qui doivent être globalement uniques et pour empêcher les attaquants de deviner les noms de ressources. Le plan ajoute automatiquement un identifiant alphanumérique aléatoire à quatre caractères. Par exemple: `prj-c-logging-a1b2` |
| Réseau VPC | `vpc-environmentcode-vpctype-vpcconfig` environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet). vpctype est l'un des commun, flotter, ou pair. vpcconfig est soit base ou limité pour indiquer si le réseau est destiné à être utilisé avec VPC Service Controls ou non. Par exemple: `vpc-p-base-partagée` |
| Sous-réseau | `sn-environmentcode-vpctype-vpcconfig-region{-description}` environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet). vpctype est l'un des commun, flotter, ou pair. vpcconfig est soit base ou limité pour indiquer si le réseau est destiné à être utilisé avec VPC Service Controls ou non. region est-ce que quelque chose est valide [Région Google Cloud](https://cloud.google.com/compute/docs/regions-zones) dans lequel se trouve la ressource. Nous vous recommandons de supprimer les traits d’union et d’utiliser une forme abrégée de certaines régions et directions pour éviter d’atteindre les limites de caractères. Par exemple, au (Australie), déjà (Amérique du Nord), sur (Amérique du Sud), UE (Europe), avec (sud-est), ou c'est (nord-est). description contient des informations supplémentaires sur le sous-réseau. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: sn-p-shared-restricted-uswest1 |
| Politiques de pare-feu | fw-firewalltype-scope-environmentcode{-description} firewalltype est hiérarchique ou réseau. scope est mondial ou la région Google Cloud dans laquelle se trouve la ressource. Nous vous recommandons de supprimer les traits d'union et d'utiliser une forme abrégée de certaines régions et directions pour éviter d'atteindre les limites de caractères. Par exemple, au (Australie), déjà (Amérique du Nord), sur (Amérique du Sud), UE (Europe), avec (sud-est), ou c'est (nord-est). environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet) qui possède la ressource de stratégie. description contient des informations supplémentaires sur la stratégie de pare-feu hiérarchique. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `fw-hiérarchique-global-c-01 fw-network-uswest1-p-base-partagée` |
| Routeur cloud | `cr-environmentcode-vpctype-vpcconfig-region{-description}` environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet). vpctype est l'un des commun, flotter, ou pair. vpcconfig est soit base ou limité pour indiquer si le réseau est destiné à être utilisé avec VPC Service Controls ou non. region est une région Google Cloud valide dans laquelle se trouve la ressource. Nous vous recommandons de supprimer les traits d'union et d'utiliser une forme abrégée de certaines régions et directions pour éviter d'atteindre les limites de caractères. Par exemple, au (Australie), déjà (Amérique du Nord), sur (Amérique du Sud), UE (Europe), avec (sud-est), ou c'est (nord-est). description contient des informations supplémentaires sur le Cloud Router. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `cr-p-base-partagée-useast1-cr1` |
| Connexion Cloud Interconnect | `ic-dc-colo` dc est le nom de votre centre de données auquel un Cloud Interconnect est connecté. colo est le [nom de l'installation de colocation](https://cloud.google.com/interconnect/docs/concepts/colocation-facilities#locations-table) avec lequel Cloud Interconnect du centre de données sur site est appairé. Par exemple: `ic-mydatacenter-lgazone1` |
| Rattachement de VLAN Cloud Interconnect | `vl-dc-colo-environmentcode-vpctype-vpcconfig-region{-description}` dc est le nom de votre centre de données auquel un Cloud Interconnect est connecté. colo est le nom de l'installation de colocation avec lequel Cloud Interconnect du centre de données sur site est appairé. environmentcode est une forme abrégée du domaine de l'environnement (l'un des b, c, p, n, d, ou filet). vpctype est l'un des commun, flotter, ou pair. vpcconfig est soit base ou limité pour indiquer si le réseau est destiné à être utilisé avec VPC Service Controls ou non. region est une région Google Cloud valide dans laquelle se trouve la ressource. Nous vous recommandons de supprimer les traits d'union et d'utiliser une forme abrégée de certaines régions et directions pour éviter d'atteindre les limites de caractères. Par exemple, au (Australie), déjà (Amérique du Nord), sur (Amérique du Sud), UE (Europe), avec (sud-est), ou c'est (nord-est). description contient des informations supplémentaires sur le VLAN. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `vl-mydatacenter-lgazone1-p-shared-base-useast1-cr1` |
| Groupe | `grp-gcp-description@exemple.com` Où description contient des informations supplémentaires sur le groupe. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `grp-gcp-billingadmin@example.com` |
| Rôle personnalisé | `rl-description` Où description contient des informations supplémentaires sur le rôle. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `rl-customcomputeadmin` |
| Compte de service | `dans-description@projectid.iam.gserviceaccount.com` Où: description contient des informations supplémentaires sur le compte de service. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. projectid est l'identifiant de projet unique au monde. Par exemple: `sa-terraform-net@prj-b-seed-a1b2.iam.gserviceaccount.com` |
| Seau de stockage | `bkt-projectid-description` Où: projectid est l'identifiant de projet unique au monde. description contient des informations supplémentaires sur le compartiment de stockage. Vous pouvez utiliser des abréviations courtes et lisibles par l’homme. Par exemple: `bkt-prj-c-infra-pipeline-a1b2-app-artefacts` |

# 

# Annexe 2 : Mappage des contrôles au code <a name="annexe-2"></a>

Remarques : 

* Le respect des exigences ITSG-33/PBMM nécessitera une ou plusieurs configurations dans des systèmes Google supplémentaires (par exemple, les identités et attributs des utilisateurs tels que les noms d'utilisateur, les mots de passe, l'authentification multifacteur (MFA), la vérification en deux étapes (2SV) et la signature unique. \-on (SSO) sont configurés et gérés via [Espace de travail Google](https://workspace.google.com/?hl=fr) ou [Identité cloud](https://cloud.google.com/identity?hl=fr)).   
* Les contrôles répertoriés dans ce document n'ont souvent pas de mappage 1:1 entre le contrôle lui-même et un bloc de code unique où il peut être invoqué.   
* La ligne d'en-tête est automatiquement épinglée afin qu'elle apparaisse en haut de chaque page.

## Contrôle d'accès (CA)

### AC-2 (2) \- CONTRÔLE D'ACCÈS

**Description du contrôle :** Le système d'information supprime automatiquement ; désactive les comptes temporaires et d'urgence après 30 jours maximum

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects du contrôle d'accès pour les utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la désactivation des comptes de système d'information temporaires et d'urgence utilisés pour accéder à GCP conformément à la politique du client.

Considérations relatives à l'espace de travail :  
Les comptes temporaires ou d'urgence ne peuvent pas être créés dans le service d'authentification des applications de Google.  
Les agences clientes ne doivent pas fournir de comptes temporaires ou d’urgence.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AC-2 (3)

**Description du contrôle :** Le système d'information désactive automatiquement les comptes inactifs au bout de 90 jours pour les comptes utilisateurs

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects du contrôle d'accès pour les utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la désactivation des comptes de système d'information temporaires et d'urgence utilisés pour accéder à GCP conformément à la politique du client.

Considérations relatives à l'espace de travail :  
Grâce à la mise en œuvre du SSO basé sur SAML, une agence peut automatiquement désactiver les comptes Google après 90 jours d'inactivité.  
L'agence devrait envisager de désactiver automatiquement les comptes inactifs via l'intégration avec le SSO basé sur SAML après une période de temps définie par l'agence ne dépassant pas l'exigence de contrôle FedRAMP de 90 jours.

La connexion à Chrome Sync s'effectue via le navigateur Chrome installé localement sur l'ordinateur d'un utilisateur, et l'activité de connexion à Chrome Sync est indépendante du compte Workspace actuel utilisé par un client de l'agence. Par exemple, un client d'agence peut se connecter à Chrome Sync en utilisant "alice@agency.gov" tout en étant simultanément connecté à Gmail en tant que "bob@agency.gov". Les comptes Chrome Sync et Workspace utilisés ne sont pas liés entre eux. Les clients d'agence utilisant Chrome Sync ne doivent se connecter à Chrome Sync qu'à l'aide de leurs comptes d'agence autorisés.

Les clients de l'agence doivent se déconnecter de Chrome Sync sur les navigateurs et les appareils qu'ils n'utilisent plus. 

Les clients de l'agence sont tenus de se connecter uniquement à Chrome Sync via leur compte d'agence, sur l'appareil fourni par leur agence et d'effectuer le travail d'agence uniquement lorsqu'ils sont connectés à leur compte d'agence afin d'éviter tout flux accidentel d'informations vers d'autres comptes. 

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AC-2 (4)

**Description du contrôle :** Le système d'information audité automatiquement les actions de création, de modification, d'activation, de désactivation et de suppression de compte, et informe le personnel ou les rôles définis par l'organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf \- pour les politiques d'organisation et de dossier  
* \- 1-org/envs/shared/log\_sinks.tf \- pour configurer la capture des journaux d'audit, la journalisation centralisée, la surveillance en temps réel, le stockage et l'analyse à long terme

#### Politiques de l'organisation

* AC-2 iam.disableServiceAccountKeyCreation : cette contrainte empêche les utilisateurs de créer des clés persistantes pour les comptes de service afin de réduire le risque d'exposition des informations d'identification du compte de service.  
* AC-2 essentialcontacts.allowedContactDomains : cette stratégie limite les contacts essentiels pour autoriser uniquement les identités d'utilisateurs gérés dans les domaines sélectionnés à recevoir des notifications de plateforme.  
* AC-2 iam.allowedPolicyMemberDomains : cette stratégie limite les stratégies IAM pour autoriser uniquement les identités d'utilisateurs gérés dans les domaines sélectionnés à accéder aux ressources au sein de cette organisation.  
* AC-2 computing.disableGuestAttributesAccess : cette autorisation contrôle si un utilisateur ou un compte de service peut modifier les attributs d'invité sur une instance de machine virtuelle (VM). Les attributs d'invité peuvent contenir des métadonnées ou des données de configuration susceptibles d'avoir un impact sur la sécurité ou le fonctionnement de la VM.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects du contrôle d'accès pour les utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la désactivation des comptes de système d'information temporaires et d'urgence utilisés pour accéder à GCP conformément à la politique du client.                

Considérations relatives à l'espace de travail :  
L'agence est chargée d'auditer automatiquement les actions de création, de modification, de désactivation et de résiliation de compte et d'informer, si nécessaire, les personnes appropriées lors de l'utilisation du SSO basé sur SAML.  
Les agences clientes sont tenues de déterminer les rôles et responsabilités définis par l'organisation pour remplir leurs obligations concernant les exigences FedRAMP suivantes. Les agences clientes doivent définir le personnel ou les rôles à notifier lors de l'audit automatique des actions de création, de modification, d'activation, de désactivation et de suppression de compte.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr) 

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### AC-2 (10)

**Description du contrôle :** Le système d'information met fin aux informations d'identification du compte partagé/groupe lorsque les membres quittent le groupe.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects du contrôle d'accès pour les utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la désactivation des comptes de système d'information temporaires et d'urgence utilisés pour accéder à GCP conformément à la politique du client.                

Considérations relatives à l'espace de travail :  
Les agences sont chargées de définir leurs propres exigences en matière d'accès aux comptes partagés. Chaque compte Workspace est destiné et conçu pour être utilisé par un utilisateur individuel.  
Si une agence met en place des comptes partagés, elle est également responsable de mettre fin aux informations d'identification du groupe lorsqu'un membre quitte. Workspace Admin Console offre aux administrateurs la possibilité de modifier le mot de passe d'un compte.

La connexion à Chrome Sync s'effectue via le navigateur Chrome installé localement sur l'ordinateur d'un utilisateur, et l'activité de connexion à Chrome Sync est indépendante du compte Workspace actuel utilisé par un client de l'agence. Par exemple, un client d'agence peut se connecter à Chrome Sync en utilisant "alice@agency.gov" tout en étant simultanément connecté à Gmail en tant que "bob@agency.gov". Les comptes Chrome Sync et Workspace utilisés ne sont pas liés entre eux. Les clients d'agence utilisant Chrome Sync ne doivent se connecter à Chrome Sync qu'à l'aide de leurs comptes d'agence autorisés.

\- Les clients de l'agence doivent se déconnecter de Chrome Sync sur les navigateurs et les appareils qu'ils n'utilisent plus.

\- Les clients de l'agence sont tenus de se connecter uniquement à Chrome Sync via leur compte d'agence, sur l'appareil fourni par leur agence et d'effectuer uniquement du travail d'agence lorsqu'ils sont connectés à leur compte d'agence afin d'éviter tout flux accidentel d'informations vers d'autres comptes.

### AC-3

**Description du contrôle :** Le système d'information applique les autorisations approuvées pour l'accès logique aux informations et aux ressources du système conformément aux politiques de contrôle d'accès applicables.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Le client serait responsable de l'ajout d'utilisateurs aux rôles d'accès au système.

Les autorisations et les groupes IAM sont utilisés pour appliquer les autorisations pour le système. Il est appliqué via une combinaison de rôles standard GCP et de rôles personnalisés.  L'application de l'accès est effectuée pour les comptes d'utilisateurs et de services.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf \- journalisation d'audit  
* \- 1-org/envs/shared/iam.tf \- rôles personnalisés  
* \- 1-org/envs/shared/projects.tf \- séparation logique des projets pour des autorisations limitées  
* \- 1-org/envs/shared/folders.tf \- hiérarchie logique des ressources pour des autorisations limitées

#### Politiques de l'organisation

* AC-3 iam.automaticIamGrantsForDefaultServiceAccounts : cette contrainte empêche les comptes de service par défaut de recevoir le rôle trop permissif d'éditeur de gestion des identités et des accès (IAM) lors de leur création.  
* AC-3, AC-6 computation.disableNestedVirtualization : cette stratégie désactive la virtualisation imbriquée pour réduire les risques de sécurité dus aux instances imbriquées non surveillées.  
* AC-3, AC-6 Compute.disableSerialPortAccess : cette stratégie empêche les utilisateurs d'accéder au port série de la VM qui peut être utilisé pour l'accès par porte dérobée à partir du plan de contrôle de l'API Compute Engine.  
* AC-3, AC-6 computation.skipDefaultNetworkCreation : cette stratégie désactive la création automatique d'un réseau VPC par défaut et des règles de pare-feu par défaut dans chaque nouveau projet, garantissant ainsi que les règles de réseau et de pare-feu sont créées intentionnellement.  
* AC-3, AC-6 calculate.restrictXpnProjectLienRemoval : cette stratégie empêche la suppression accidentelle des projets hôtes de VPC partagé en limitant la suppression des privilèges de projet.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 Compute.setNewProjectDefaultToZonalDNSOnly : cette stratégie empêche les développeurs d'applications de choisir des paramètres DNS existants pour les instances Compute Engine dont la fiabilité du service est inférieure à celle des paramètres DNS modernes.  
* AC-3, AC-6 sql.restrictPublicIp : cette stratégie empêche la création d'instances Cloud SQL avec des adresses IP publiques, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-3, AC-6 sql.restrictAuthorizedNetworks : cette stratégie empêche les plages de réseaux publics ou non RFC 1918 d'accéder aux bases de données Cloud SQL.  
* AC-3, AC-6 storage.uniformBucketLevelAccess : cette stratégie empêche les buckets Cloud Storage d'utiliser l'ACL par objet (un système distinct des stratégies IAM) pour fournir l'accès, garantissant ainsi la cohérence de la gestion des accès et de l'audit.  
* AC-3, AC-6 storage.publicAccessPrevention : cette stratégie empêche les buckets Cloud Storage d'être ouverts à un accès public non authentifié.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 computation.vmExternalIpAccess : cette stratégie empêche la création d'instances Compute Engine avec une adresse IP publique, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-3, AU-12 computation.requireOsLogin : cette stratégie nécessite une connexion au système d'exploitation sur les machines virtuelles nouvellement créées pour gérer plus facilement les clés SSH, fournir une autorisation au niveau des ressources avec les stratégies IAM et enregistrer l'accès des utilisateurs.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects du contrôle d'accès pour les utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la désactivation des comptes de système d'information temporaires et d'urgence utilisés pour accéder à GCP conformément à la politique du client.   

Considérations relatives à l'espace de travail :  
Workspace applique l'autorisation de l'administrateur pour l'accès logique au domaine de l'agence. Workspace permet aux administrateurs d'établir des rôles et des groupes d'administrateur au sein d'un domaine, et l'accès aux rôles et aux groupes peut être restreint en fonction de l'autorisation requise. Dans les paramètres de domaine de la console d'administration, il existe des rôles d'administrateur établis, ainsi que l'option pour les rôles créés par le client. Pour chaque rôle d'administrateur, des privilèges spécifiques sont définis pour contrôler ce à quoi les administrateurs sont autorisés à accéder dans Admin Console. Les administrateurs établissent des groupes en définissant un nom de groupe, une adresse e-mail de groupe et une brève explication du groupe.  
L'administrateur détermine les préréglages d'autorisation pour le groupe en déterminant si le groupe doit être destiné au public, aux annonces, à l'équipe ou personnalisé. Un groupe public est destiné aux sujets d’intérêt général et les e-mails sont illimités. Un groupe d'annonces est destiné à être diffusé à un large public et le courrier électronique est réservé aux propriétaires du groupe.  Un groupe d'équipe est destiné aux équipes et autres groupes de travail et le courrier électronique est réservé aux utilisateurs du domaine.  Un groupe personnalisé permet un contrôle précis des autorisations du groupe.  Les utilisateurs peuvent également créer des groupes et être administrateurs de leur propre contenu et des sous-groupes au sein des groupes qu'ils créent.

Séparer l'accès des utilisateurs au sein de votre domaine :

Pour gérer les autorisations des utilisateurs, l'administrateur peut simplement créer des unités organisationnelles pour séparer logiquement les comptes d'utilisateurs finaux. Une fois ces unités configurées, l'administrateur peut activer ou désactiver des services spécifiques pour les utilisateurs.

Pour en savoir plus, veuillez vous référer à nos ressources d'assistance qui expliquent « comment configurer des unités organisationnelles » et « comment activer et désactiver les services ».

Google Vault :

Les privilèges d'administrateur liés à Google Vault sont attribués aux utilisateurs dans la console d'administration. Les administrateurs de domaine dotés du rôle de super-administrateur ont par défaut accès à tous les privilèges d'accès à Vault. Les clients peuvent également attribuer n'importe quelle combinaison de privilèges Vault aux utilisateurs via des rôles créés sur mesure dans la console d'administration. Google Vault est uniquement disponible pour les clients disposant des éditions Workspace for Business ou Workspace for Enterprise, ou en tant que complément payant à Workspace Basic. Il est de la responsabilité du client d'acheter Google Vault s'il est un client Workspace Basic.

L'agence est chargée d'établir les rôles d'administrateur, les groupes et les autorisations créés par les utilisateurs dans Workspace, de s'assurer que les autorisations sont approuvées et de garantir que le processus est effectué conformément à la politique de l'agence applicable. (Responsabilité du client n°2)             

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AC-4

**Description du contrôle :** Le système d'information applique les autorisations approuvées pour contrôler le flux d'informations au sein du système et entre les systèmes interconnectés sur la base des politiques de contrôle de flux d'informations définies par l'organisation du client.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Cette Landing Zone utilise le mode d'architecture Hub and Spoke. Le modèle Landing Zone utilise des zones DNS, des pare-feu d'appliance virtuelle réseau, un réseau Virtual Private Cloud (VPC) et des contrôles de service VPC pour satisfaire cette exigence. Plus de détails peuvent être trouvés dans la section Mise en réseau du guide des bases de la sécurité du cloud de Google ([https://cloud.google.com/architecture/security-foundations/networking\#hub-and-spoke](https://cloud.google.com/architecture/security-foundations/networking#hub-and-spoke)).

Une description détaillée de la mise en œuvre peut être trouvée dans 3\. réseaux-dual-svpc ([https://github.com/terraform-google-modules/terraform-example-foundation\#3-networks-dual-svpc](https://github.com/terraform-google-modules/terraform-example-foundation#3-networks-dual-svpc)) et 3\. réseaux en étoile ([https://github.com/terraform-google-modules/terraform-example-foundation\#3-networks-hub-and-spoke](https://github.com/terraform-google-modules/terraform-example-foundation#3-networks-hub-and-spoke));

Fortigate de Fortinet sera l’appliance de pare-feu de nouvelle génération utilisée.  

Des règles de pare-feu sont implémentées par défaut pour empêcher les connexions en dehors des limites du système. Les informations/données ne sont pas présentes sur la solution (il s'agit d'une solution d'infrastructure uniquement) avant l'intégration de la charge de travail du client. Toute règle autorisant la diffusion d'informations en dehors des limites du système relèverait de la responsabilité du propriétaire des informations/données dans le cadre de sa réponse à ce contrôle.

IAM Asset Inventory permet la découverte/l'exportation automatisée des services actuellement déployés dans l'organisation ou dans des projets individuels.

Reportez-vous à Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf pour la définition de base du réseau, des contrôles de service, des politiques et de la journalisation  
* \- 3-networks-hub-and-spoke/envs/shared/dns-hub.tf \- définition DNS

#### Recommandations de mise en œuvre

Les clients sont responsables du contrôle du flux d'informations au sein de leur système, y compris les composants intégrés dans GCP, et entre le système du client et d'autres systèmes interconnectés. Les clients peuvent choisir d'utiliser le service Virtual Private Cloud (VPC) au sein de la famille de produits GCP Networking pour répondre à cette exigence. VPC est un ensemble complet de fonctionnalités réseau gérées par Google, notamment une sélection granulaire de plages d'adresses IP, des routes, des pare-feu et un réseau privé virtuel (VPN). VPC permet aux clients de provisionner leurs ressources GCP, de les connecter les unes aux autres et de les isoler les unes des autres dans un cloud privé virtuel (VPC).

Considérations relatives à l'espace de travail :  
Les clients de l'agence ayant des exigences en matière de localisation des données sont responsables de la désactivation de Chrome Sync. Chrome Sync n'est pas un produit de localisation de données et synchronise les données du navigateur de l'utilisateur, qui peuvent contenir des données localisées.  
La connexion à Chrome Sync s'effectue via le navigateur Chrome installé localement sur l'ordinateur d'un utilisateur, et l'activité de connexion à Chrome Sync est indépendante du compte Workspace actuel utilisé par un client de l'agence. Par exemple, un client d'agence peut se connecter à Chrome Sync en utilisant "alice@agency.gov" tout en étant simultanément connecté à Gmail en tant que "bob@agency.gov". Les comptes Chrome Sync et Workspace utilisés ne sont pas liés entre eux. Les clients d'agence utilisant Chrome Sync ne doivent se connecter à Chrome Sync qu'à l'aide de leurs comptes d'agence autorisés.

Les clients de l'agence sont tenus de se connecter uniquement à Chrome Sync via leur compte d'agence, sur l'appareil fourni par leur agence et d'effectuer le travail d'agence uniquement lorsqu'ils sont connectés à leur compte d'agence afin d'éviter tout flux accidentel d'informations vers d'autres comptes.

Les agences clientes sont responsables de la configuration de leurs navigateurs et connexions côté client sur les postes de travail, serveurs et appareils mobiles applicables pour activer les connexions utilisant le cryptage. Les clients doivent appliquer les paramètres USGCB sur les postes de travail fournis par le gouvernement pour établir des connexions avec des chiffrements approuvés par FIPS. Les clients doivent activer la liste des fonctions nécessitant une connexion par chemin de confiance qui doit être examinée et approuvée par l'agence AO ou FedRAMP JAB.

Bonne pratique : implémentez VPC Service Controls (lien) pour bloquer l'accès externe aux services protégés par le périmètre.  
Bonne pratique : activer les journaux de flux VPC (lien) pour surveiller le trafic réseau envoyé vers/depuis les instances de VM

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Google Cloud Load Balancing : implémentez l'auto scaling du réseau mondial, HTTP(S), TCP, SSL et l'équilibrage de charge interne   
[https://cloud.google.com/load-balancing/](https://cloud.google.com/load-balancing/) 

Cloud DNS – Service DNS (Domain Name System) faisant autorité, évolutif, fiable, résilient et géré. Publiez et gérez facilement des millions de zones et d'enregistrements DNS.  
[https://cloud.google.com/dns/?hl=fr](https://cloud.google.com/dns/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

### AC-4 (21)

**Description du contrôle :** Le système d'information sépare les flux d'informations logiquement ou physiquement à l'aide de mécanismes et/ou de techniques définis par l'organisation pour réaliser les séparations requises définies par l'organisation par types d'informations.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Oui

#### Notes de mise en œuvre

Les ressources sont logiquement séparées pour l’organisation et en aval pour les charges de travail. Des projets distincts et des rôles d'accès sont créés pour différents types d'informations et de rôles commerciaux tels que la facturation, l'audit, la journalisation, les km, les secrets et le réseau.  Les projets sont créés pour les équipes et les charges de travail

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf pour la définition de base du réseau, des contrôles de service, des politiques et de la journalisation  
* \- 3-networks-hub-and-spoke/modules/hierarchical\_firewall\_policy pour les politiques d'accès contextuelles, y compris l'entrée et la sortie

#### Recommandations de mise en œuvre

Les clients sont responsables du contrôle du flux d'informations au sein de leur système, notamment en séparant logiquement les flux de données en fonction des exigences du client.

Bonne pratique : mettre en œuvre VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters)) pour bloquer l'accès externe aux services protégés par le périmètre.  
Bonne pratique : activer les journaux de flux VPC ([https://cloud.google.com/vpc/docs/using-flow-logs](https://cloud.google.com/vpc/docs/using-flow-logs)) pour surveiller le trafic réseau envoyé vers/depuis les instances de VM \- Fonction App/Propriétaire du projet 

### AC-6 (9)

**Description du contrôle :** Le système d'information audité l'exécution des fonctions privilégiées.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La Landing Zone définit les rôles et la séparation logique des ressources pour des autorisations limitées.

#### Définitions des ressources

* \- 1-org/envs/shared/iam.tf \- rôles personnalisés  
* \- 1-org/envs/shared/projects.tf \- séparation logique des projets pour des autorisations limitées  
* \- 1-org/envs/shared/folders.tf \- hiérarchie logique des ressources pour des autorisations limitées

#### Politiques de l'organisation

* AC-3, AC-6 computation.disableNestedVirtualization : cette stratégie désactive la virtualisation imbriquée pour réduire les risques de sécurité dus aux instances imbriquées non surveillées.  
* AC-3, AC-6 Compute.disableSerialPortAccess : cette stratégie empêche les utilisateurs d'accéder au port série de la VM qui peut être utilisé pour l'accès par porte dérobée à partir du plan de contrôle de l'API Compute Engine.  
* AC-3, AC-6 computation.skipDefaultNetworkCreation : cette stratégie désactive la création automatique d'un réseau VPC par défaut et des règles de pare-feu par défaut dans chaque nouveau projet, garantissant ainsi que les règles de réseau et de pare-feu sont créées intentionnellement.  
* AC-3, AC-6 calculate.restrictXpnProjectLienRemoval : cette stratégie empêche la suppression accidentelle des projets hôtes de VPC partagés en limitant la suppression des privilèges de projet.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 Compute.setNewProjectDefaultToZonalDNSOnly : cette stratégie empêche les développeurs d'applications de choisir des paramètres DNS existants pour les instances Compute Engine dont la fiabilité du service est inférieure à celle des paramètres DNS modernes.  
* AC-3, AC-6 sql.restrictPublicIp : cette stratégie empêche la création d'instances Cloud SQL avec des adresses IP publiques, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-3, AC-6 sql.restrictAuthorizedNetworks : cette stratégie empêche les plages de réseaux publics ou non RFC 1918 d'accéder aux bases de données Cloud SQL.  
* AC-3, AC-6 storage.uniformBucketLevelAccess : cette stratégie empêche les buckets Cloud Storage d'utiliser l'ACL par objet (un système distinct des stratégies IAM) pour fournir l'accès, garantissant ainsi la cohérence de la gestion des accès et de l'audit.  
* AC-3, AC-6 storage.publicAccessPrevention : cette stratégie empêche les buckets Cloud Storage d'être ouverts à un accès public non authentifié.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 computation.vmExternalIpAccess : cette stratégie empêche la création d'instances Compute Engine avec une adresse IP publique, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-6 iam.disableServiceAccountKeyUpload : cette contrainte évite le risque de fuite et de réutilisation des éléments de clé personnalisés dans les clés de compte de service.

#### Recommandations de mise en œuvre

Les clients sont responsables de l'audit de l'exécution des fonctions privilégiées pour tous les composants contrôlés par le client et hébergés sur GCP.

Considérations relatives à l'espace de travail :  
Workspace donne accès aux rapports de journalisation des événements des comptes privilégiés. Le journal d'audit de la console d'administration affiche un historique de chaque tâche effectuée dans votre console d'administration Google et indique qui a effectué la tâche, à quelle heure et à partir de quelle adresse IP. Les rapports sont accessibles en accédant à  la Console d'administration \\ Rapports \\ Admin.

Les rapports d'audit peuvent être filtrés par attributs d'événement.

Plus de détails et de conseils concernant la journalisation des événements de compte privilégié peuvent être trouvés ici ([https://support.google.com/a/answer/4579579](https://support.google.com/a/answer/4579579))

Bonne pratique facultative : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources ([https://cloud.google.com/logging/docs/audit/configure-data-access](https://cloud.google.com/logging/docs/audit/configure-data-access))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr) 

### AC-6 (10)

**Description du contrôle :** Le système d'information empêche les utilisateurs non privilégiés d'exécuter des fonctions privilégiées, notamment la désactivation, le contournement ou la modification des mesures de protection/contre-mesures de sécurité mises en œuvre.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La Landing Zone définit les rôles et la séparation logique des ressources pour des autorisations limitées. 

Le modèle Landing Zone utilise l'accès du compte de service GCP à ces comptes privilégiés. Le rôle d’administrateur organisationnel doit être utilisé avec parcimonie, conformément à la stratégie de bris de glace.

#### Définitions des ressources

* \- 1-org/envs/shared/iam.tf \- rôles personnalisés  
* \- 1-org/envs/shared/projects.tf \- séparation logique des projets pour des autorisations limitées  
* \- 1-org/envs/shared/folders.tf \- hiérarchie logique des ressources pour des autorisations limitées

#### Politiques de l'organisation

* AC-3, AC-6 computation.disableNestedVirtualization : cette stratégie désactive la virtualisation imbriquée pour réduire les risques de sécurité dus aux instances imbriquées non surveillées.  
* AC-3, AC-6 Compute.disableSerialPortAccess : cette stratégie empêche les utilisateurs d'accéder au port série de la VM qui peut être utilisé pour l'accès par porte dérobée à partir du plan de contrôle de l'API Compute Engine.  
* AC-3, AC-6 computation.skipDefaultNetworkCreation : cette stratégie désactive la création automatique d'un réseau VPC par défaut et des règles de pare-feu par défaut dans chaque nouveau projet, garantissant ainsi que les règles de réseau et de pare-feu sont créées intentionnellement.  
* AC-3, AC-6 calculate.restrictXpnProjectLienRemoval : cette stratégie empêche la suppression accidentelle des projets hôtes de VPC partagé en limitant la suppression des privilèges de projet.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 Compute.setNewProjectDefaultToZonalDNSOnly : cette stratégie empêche les développeurs d'applications de choisir des paramètres DNS existants pour les instances Compute Engine dont la fiabilité du service est inférieure à celle des paramètres DNS modernes.  
* AC-3, AC-6 sql.restrictPublicIp : cette stratégie empêche la création d'instances Cloud SQL avec des adresses IP publiques, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-3, AC-6 sql.restrictAuthorizedNetworks : cette stratégie empêche les plages de réseaux publics ou non RFC 1918 d'accéder aux bases de données Cloud SQL.  
* AC-3, AC-6 storage.uniformBucketLevelAccess : cette stratégie empêche les buckets Cloud Storage d'utiliser l'ACL par objet (un système distinct des stratégies IAM) pour fournir l'accès, garantissant ainsi la cohérence de la gestion des accès et de l'audit.  
* AC-3, AC-6 storage.publicAccessPrevention : cette stratégie empêche les buckets Cloud Storage d'être ouverts à un accès public non authentifié.  
* AC-3, AC-6 computation.disableVpcExternalIpv6 : cette stratégie empêche la création de sous-réseaux IPv6 externes, qui peuvent être exposés au trafic Internet entrant et sortant.  
* AC-3, AC-6 computation.vmExternalIpAccess : cette stratégie empêche la création d'instances Compute Engine avec une adresse IP publique, ce qui peut les exposer au trafic Internet entrant et au trafic Internet sortant.  
* AC-6 iam.disableServiceAccountKeyUpload : cette contrainte évite le risque de fuite et de réutilisation des éléments de clé personnalisés dans les clés de compte de service.

#### Recommandations de mise en œuvre

Les clients sont responsables d'empêcher les utilisateurs non privilégiés d'exécuter des fonctions privilégiées pour tous les composants contrôlés par le client hébergés sur GCP. GCP permet aux clients d'attribuer des rôles administratifs et non administratifs aux comptes clients au sein de GCP. Les rôles non administratifs ne peuvent pas exécuter de fonctions privilégiées au sein du projet GCP du client, notamment désactiver, contourner ou modifier les mesures de sécurité/contre-mesures mises en œuvre.

Considérations relatives à l'espace de travail :  
Les clients de l'agence sont responsables d'établir les conditions d'adhésion au groupe en fonction de critères définis par l'agence, notamment l'identification des utilisateurs autorisés de Workspace et la spécification des privilèges/rôles d'accès.  
Accordez l’accès au système en fonction d’une autorisation d’accès valide et de l’utilisation prévue du système.

Autorisez et établissez les rôles d'administrateur, les groupes et les autorisations créés par les utilisateurs, en garantissant que les autorisations sont approuvées et attribuées conformément à la politique de l'agence.

Bonne pratique : demandez à l'administrateur d'identité de vérifier et de recalibrer les autorisations IAM en fonction de Cloud IAM Recommender ([https://cloud.google.com/iam/docs/recommemender-overview?hl=fr](https://cloud.google.com/iam/docs/recommender-overview?hl=fr) )

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

### AC-7

**Description du contrôle :** Le système d'information :

 un. Applique une limite de pas plus de 3 tentatives de connexion non valides consécutives par un utilisateur, pendant une période de 15 minutes ; et

 b. Verrouille automatiquement le compte/nœud pendant 30 minutes ; ou  
verrouille le compte/nœud jusqu'à ce qu'il soit libéré par un administrateur ; ou  
retarde l'invite de connexion suivante selon un algorithme de retard défini par l'organisation lorsque le nombre maximum de tentatives infructueuses est dépassé.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de l'application d'une limite de tentatives de connexion invalides consécutives pour les comptes d'utilisateurs clients et verrouillent automatiquement le compte jusqu'à ce qu'il soit déverrouillé par un administrateur. 

Considérations relatives à Google Workspace :

Lors de la connexion à un compte Google, le service d'authentification des applications de Google n'applique pas par défaut les paramètres de verrouillage du compte après un certain nombre de tentatives de connexion non valides. Le service d'authentification des applications de Google institue l'utilisation d'un défi de connexion tel qu'un Captcha (type de test défi-réponse utilisé pour déterminer si l'utilisateur est un ordinateur ou un humain) après un nombre défini par un algorithme de tentatives de connexion invalides. Si un utilisateur répond de manière incorrecte au Captcha, des Captchas lui sont présentés jusqu'à ce que le Captcha et le mot de passe soient saisis correctement. De plus, Google peut envoyer un code d'authentification secondaire à un compte que l'utilisateur a inclus dans son profil de domaine Google, comme un SMS envoyé à un numéro de téléphone portable de secours. Remarque : pour qu'un code de sécurité soit envoyé au téléphone portable d'un utilisateur, celui-ci doit fournir ces informations dans les paramètres de son compte Google Workspace et terminer le processus d'inscription, qui comprend l'enregistrement du numéro de téléphone dans les paramètres de son compte et la réception d'un code de test. et en saisissant correctement le code de test à l'invite Paramètres du compte Google.  
Pour les agences utilisant l'authentification unique basée sur SAML, les paramètres de verrouillage du compte sont contrôlés par le système de gestion de compte de l'agence qui peut être configuré pour appliquer une limite de trois (3) tentatives d'accès non valides consécutives par un utilisateur pendant une période de 15 minutes. période et verrouille automatiquement le compte/nœud pendant une période de 30 minutes.

Pour les agences utilisant le SSO basé sur SAML, l'agence devrait envisager : (a) d'appliquer une limite définie par l'agence de tentatives d'accès non valides consécutives par un utilisateur pendant une période définie par l'agence ; (b) verrouiller automatiquement le compte pendant une période définie par l'agence, verrouiller le compte jusqu'à ce qu'il soit libéré par un administrateur, ou retarder la prochaine invite de connexion pendant un délai défini par l'agence lorsque le nombre maximum de tentatives infructueuses est dépassé. Ce contrôle doit s'appliquer indépendamment du fait que la connexion s'effectue via une connexion locale ou réseau. Les administrateurs de l'agence doivent configurer leur service d'authentification pour appliquer une limite de trois (3) tentatives de connexion invalides au maximum sur une période de 15 minutes et verrouiller le compte/nœud pendant au moins 30 minutes.

Google propose également une authentification à 2 facteurs, soit des options d'authentification OTP ou par clé de sécurité, que les administrateurs peuvent activer dans la console d'administration. La mise en œuvre de l'authentification à 2 facteurs fournit une deuxième couche de vérification pour les administrateurs clients et les utilisateurs. Une fois activé, les utilisateurs ou les administrateurs clients doivent s'inscrire au processus de vérification à 2 facteurs pour recevoir un code de vérification à six chiffres (OTP) ou appuyer sur leur jeton USB (clé de sécurité) requis pour se connecter à Google Workspace en plus de leur nom d'utilisateur habituel et identifiants de mot de passe. Si les agences choisissent d'utiliser l'authentification à 2 facteurs de Google et choisissent l'option d'authentification par clé de sécurité, elles doivent noter que les clés de sécurité gérées par l'administrateur à l'échelle du domaine et la gestion des clés de sécurité ne sont disponibles que pour les clients Google Workspace Business et Google Workspace Enterprise Edition.

Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue. Les clients Google Workspace Entreprise et Business peuvent configurer une durée de résiliation de session Google aussi courte qu'une (1) heure (https://support.google.com/a/answer/7576830?hl=en). Il convient de noter que pour que ces paramètres prennent effet, les utilisateurs de l'Agence doivent se déconnecter et se reconnecter pour lancer la nouvelle application de la durée de session. Il est également possible pour les administrateurs d'agence de réinitialiser manuellement les cookies de connexion d'un utilisateur pour chaque utilisateur (https://support.google.com/a/answer/178854?hl=en). Les agences qui décident de mettre en œuvre une durée de résiliation de session inférieure à une (1) heure doivent implémenter USGCB pour les postes de travail de l'agence, qui expirera l'utilisateur au niveau du poste de travail après une période d'inactivité spécifiée par l'agence.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AC-8

**Description du contrôle :** Le système d'information :

 Il affiche aux utilisateurs un message ou une bannière de notification d'utilisation du système défini par l'organisation avant d'accorder l'accès au système qui fournit des avis de confidentialité et de sécurité conformes aux lois fédérales, décrets, directives, politiques, réglementations, normes et orientations fédéraux applicables et indique que :  
   1\. Les utilisateurs accèdent à un système d'information du gouvernement américain ;  
   2\. L'utilisation du système d'information peut être surveillée, enregistrée et soumise à un audit ;  
   3\. L'utilisation non autorisée du système d'information est interdite et passible de sanctions pénales et civiles ; et  
   4\. L'utilisation du système d'information indique le consentement à la surveillance et à l'enregistrement ;

 b. Conserve le message de notification ou la bannière à l'écran jusqu'à ce que les utilisateurs prennent connaissance des conditions d'utilisation et effectuent des actions explicites pour se connecter ou accéder davantage au système d'information ; et 

 c. Pour les systèmes accessibles au public :  
   1\. Affiche les informations d'utilisation du système en fonction des conditions définies par l'organisation, avant d'accorder un accès supplémentaire ;  
   2\. Affiche les références, le cas échéant, à la surveillance, à l'enregistrement ou à l'audit qui sont conformes aux aménagements en matière de confidentialité pour de tels systèmes qui interdisent généralement ces activités ; et  
   3\. Comprend une description des utilisations autorisées du système.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables d'afficher la bannière d'utilisation du système appropriée aux utilisateurs clients avant d'accorder l'accès à leurs systèmes clients. La bannière d'utilisation du système doit fournir des avis de confidentialité et de sécurité conformes aux lois fédérales, décrets, directives, politiques, réglementations, normes et orientations fédérales applicables.

Parb B :  
Les clients sont responsables de conserver le message de notification ou la bannière à l'écran jusqu'à ce que les utilisateurs clients reconnaissent les conditions d'utilisation et prennent des mesures explicites pour se connecter ou accéder davantage au système d'information client.

Partie C :  
Les clients sont responsables de :

Affichage des informations d'utilisation du système pour les systèmes clients accessibles au public avant d'accorder un accès supplémentaire  
Afficher les références, le cas échéant, à la surveillance, à l'enregistrement ou à l'audit qui sont conformes aux aménagements en matière de confidentialité pour de tels systèmes qui interdisent généralement ces activités  
Incluant une description des utilisations autorisées du système.

Considérations relatives à l'espace de travail :  
Afin d'utiliser les contrôles de notification d'utilisation du système, l'agence est responsable de la mise en œuvre de l'authentification unique et de l'approbation d'un message ou d'une bannière de notification d'utilisation du système affiché sur une page de connexion SSO contrôlée par l'agence. L'agence doit utiliser l'authentification unique basée sur SAML pour afficher la notification d'utilisation approuvée du système de l'agence lorsque les utilisateurs de l'agence tentent de s'authentifier auprès du domaine de l'agence et utiliser la console d'administration pour configurer l'authentification unique pour l'authentification de l'agence. L'agence est chargée d'identifier, de vérifier et d'approuver la notification ou la bannière d'utilisation du système ainsi que la périodicité appropriée du contrôle.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google App Engine : exploitez Google App Engine et Google Compute Engine pour gérer des sites Web, configurer des sites Web statiques pour les notifications et créer des applications évolutives.  
[https://cloud.google.com/solutions/websites/?hl=fr](https://cloud.google.com/solutions/websites/?hl=fr) 

Cloud Pub/Sub – Messagerie globale et même ingestion à grande échelle  
[https://cloud.google.com/pubsub/?hl=fr](https://cloud.google.com/pubsub/?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr) 

Fonctions Cloud – Plateforme de calcul sans serveur basée sur les événements.  
[https://cloud.google.com/functions/?hl=fr](https://cloud.google.com/functions/?hl=fr)

### AC-10

**Description du contrôle :** Le système d'information limite le nombre de sessions simultanées pour les comptes privilégiés à (3) et les sessions pour les comptes non privilégiés à (2).

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de limiter le nombre de sessions simultanées pour les utilisateurs clients en fonction du type de compte client.

Considérations relatives à l'espace de travail :  
Les clients de l'agence doivent examiner périodiquement l'activité récente de leurs paramètres de compte pour déterminer si l'activité de leur compte est appropriée et informer un administrateur de domaine de l'agence si une activité suspecte est détectée. De plus, les clients des agences doivent mettre en œuvre la vérification en deux étapes (2SV) pour limiter la capacité d'une connexion malveillante réussie, car les utilisateurs devraient fournir un nom d'utilisateur, un mot de passe et un jeton 2SV délivrés à un appareil (OTP) ou appuyer sur leur périphérique USB (sécurité). Key) qui est en possession physique de l'utilisateur qui tente de se connecter. De plus, les utilisateurs peuvent configurer les notifications et alertes pour surveiller davantage les sessions simultanées.

La connexion à Chrome Sync s'effectue via le navigateur Chrome installé localement sur l'ordinateur d'un utilisateur, et l'activité de connexion à Chrome Sync est indépendante du compte Workspace actuel utilisé par un client de l'agence. Par exemple, un client d'agence peut se connecter à Chrome Sync en utilisant "alice@agency.gov" tout en étant simultanément connecté à Gmail en tant que "bob@agency.gov". Les comptes Chrome Sync et Workspace utilisés ne sont pas liés entre eux. Les clients d'agence utilisant Chrome Sync ne doivent se connecter à Chrome Sync qu'à l'aide de leurs comptes d'agence autorisés.

Si les agences choisissent d'utiliser la vérification en deux étapes de Google et choisissent l'option d'authentification par clé de sécurité, elles doivent noter que les clés de sécurité gérées par l'administrateur à l'échelle du domaine et la gestion des clés de sécurité ne sont disponibles que pour les clients Workspace Business et Workspace Enterprise Edition.

GSA a examiné et accepté cette mise en œuvre alternative

Les clients de l'agence doivent se déconnecter des sessions Chrome Sync lorsqu'ils n'utilisent plus de navigateur ou d'appareil.

Bonne pratique : configurez Cloud Identity pour limiter la durée de session pour les services Google (https://support.google.com/cloudidentity/answer/7576830?hl=en). Par défaut, la durée de session pour les services Google est de 14 jours

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr) 

### AC-11

**Description du contrôle :** Le système d'information :  
   
un. Empêche tout accès ultérieur au système en déclenchant un verrouillage de session après une période d'inactivité de 15 minutes ou à la réception d'une demande d'un utilisateur ; et

 b. Conserve le verrouillage de session jusqu'à ce que l'utilisateur rétablisse l'accès à l'aide des procédures d'identification et d'authentification établies.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables d'initier un verrouillage de session pour les sessions client après 15 minutes d'inactivité ou dès réception d'une demande d'un utilisateur.

Partie B :  
Les clients sont responsables du maintien des verrous de session jusqu'à ce que l'utilisateur client rétablisse l'accès à l'aide des procédures d'identification et d'authentification client établies.

Considérations relatives à l'espace de travail :  
L'agence doit utiliser des économiseurs d'écran pour (a) activer le verrouillage de session après une fréquence d'inactivité définie par l'agence et (b) conserver le verrouillage de session jusqu'à ce que l'utilisateur rétablisse l'accès à l'aide des procédures d'identification et d'authentification établies. En outre, le cas échéant, l'agence doit demander aux utilisateurs de se déconnecter des services Google après avoir terminé une session sur un poste de travail/ordinateur portable non sécurisé ou après avoir retiré un poste de travail/ordinateur portable d'une installation non sécurisée.

De plus, les clients accédant à Workspace à partir d'appareils autres que des postes de travail, tels que des appareils mobiles, doivent appliquer une politique de gestion des appareils mobiles pour verrouiller les appareils après 15 minutes d'inactivité et exiger un mot de passe pour les déverrouiller. Le verrouillage de session ne doit pas dépasser l'exigence FedRAMP de 15 minutes d'inactivité.

Bonne pratique : configurez Cloud Identity pour limiter la durée de session pour les services Google (https://support.google.com/cloudidentity/answer/7576830?hl=en). Par défaut, la durée de session pour les services Google est de 14 jours

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace \- Ajoutez facilement des utilisateurs, gérez les appareils et configurez la sécurité et les paramètres pour que vos données restent en sécurité. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### AC-11 (1)

**Description du contrôle :** Le système d'information dissimule, via le verrouillage de session, les informations précédemment visibles sur l'écran avec une image visible publiquement.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de s'assurer que leurs systèmes masquent, via un verrouillage de session, les informations précédemment visibles sur l'écran avec une image visible publiquement.

Considérations relatives à l'espace de travail :  
L'agence doit utiliser des économiseurs d'écran pour activer le verrouillage de session afin de masquer les informations précédemment visibles sur l'écran avec une image visible publiquement et conserver le verrouillage de session jusqu'à ce que l'utilisateur rétablisse l'accès à l'aide des procédures d'identification et d'authentification établies.

Bonne pratique : configurez Cloud Identity pour limiter la durée de session pour les services Google (https://support.google.com/cloudidentity/answer/7576830?hl=en). Par défaut, la durée de session pour les services Google est de 14 jours

### AC-12

**Description du contrôle :** Le système d'information met automatiquement fin à une session utilisateur lorsque des conditions définies par l'organisation ou des événements déclencheurs nécessitent une déconnexion de session.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM.

#### Recommandations de mise en œuvre

Les clients sont responsables de s'assurer que les systèmes clients mettent automatiquement fin à une session utilisateur après qu'une condition définie par le client se produit.

Considérations relatives à l'espace de travail :  
Workspace ne met pas fin à une connexion après une période d'inactivité. En guise de contrôle compensatoire, les agences devraient mettre en œuvre le SSO basé sur SAML ainsi que l'USGCB pour les postes de travail de l'agence, ce qui entraînera une expiration du délai d'attente de l'utilisateur au niveau du poste de travail après une période d'inactivité spécifiée par l'agence.

La connexion à Chrome Sync s'effectue via le navigateur Chrome installé localement sur l'ordinateur d'un utilisateur, et l'activité de connexion à Chrome Sync est indépendante du compte Workspace actuel utilisé par un client de l'agence. Par exemple, un client d'agence peut se connecter à Chrome Sync en utilisant "alice@agency.gov" tout en étant simultanément connecté à Gmail en tant que "bob@agency.gov". Les comptes Chrome Sync et Workspace utilisés ne sont pas liés entre eux. Les clients d'agence utilisant Chrome Sync ne doivent se connecter à Chrome Sync qu'à l'aide de leurs comptes d'agence autorisés.

Les clients de l'agence doivent se déconnecter de Chrome Sync sur les navigateurs et les appareils qu'ils n'utilisent plus.   
GSA a accepté cette mise en œuvre alternative.  
Les agences doivent mettre en œuvre l'authentification unique basée sur SAML ainsi que l'USGCB pour les postes de travail de l'agence, qui expirent l'utilisateur au niveau du poste de travail après une période d'inactivité spécifiée par l'agence.

Bonne pratique : configurez Cloud Identity pour limiter la durée de session pour les services Google (https://support.google.com/cloudidentity/answer/7576830?hl=en). Par défaut, la durée de session pour les services Google est de 14 jours

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

### AC-17 (1)

**Description du contrôle :** Le système d'information surveille et contrôle les méthodes d'accès à distance.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client. 

Le modèle Landing Zone déploie un bunker de journaux immuable pour collecter les données de journalisation. Les organisations peuvent utiliser ces journaux pour effectuer des actions automatisées. Le modèle Landing Zone utilise également Identity Aware Proxy, une fonctionnalité qui utilise l'identité et le contexte pour protéger l'accès aux services et aux machines virtuelles.

#### Recommandations de mise en œuvre

Les clients sont responsables de l'audit de l'exécution des fonctions privilégiées pour tous les composants contrôlés par le client et hébergés sur GCP.

Considérations relatives à l'espace de travail :  
Workspace donne accès aux rapports de journalisation des événements des comptes privilégiés. Le journal d'audit de la console d'administration affiche un historique de chaque tâche effectuée dans votre console d'administration Google et indique qui a effectué la tâche, à quelle heure et à partir de quelle adresse IP. Les rapports sont accessibles en accédant à Console d'administration \\ Rapports \\ Admin.

Les rapports d'audit peuvent être filtrés par attributs d'événement.

Plus de détails et de conseils concernant la journalisation des événements de compte privilégié peuvent être trouvés ici

Bonne pratique facultative : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources (lien)

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)  
 

### AC-17 (2)

**Description du contrôle :** Le système d'information met en œuvre des mécanismes cryptographiques pour protéger la confidentialité et l'intégrité des sessions d'accès à distance.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la mise en œuvre de mécanismes cryptographiques pour protéger la confidentialité et l'intégrité des sessions d'accès à distance aux systèmes clients. De plus, les clients doivent s'assurer que les machines se connectant à Google Cloud sont configurées pour utiliser le cryptage approprié pour les communications entre Google et l'agence.

Google utilise le chiffrement en transit avec TLS ([https://cloud.google.com/security/encryption-in-transit\#encryption\_in\_transit\_by\_default](https://cloud.google.com/security/encryption-in-transit#encryption_in_transit_by_default)) par défaut des utilisateurs finaux (Internet) vers tous les services Google.  
Décrivez tout chiffrement supplémentaire configuré par les propriétaires du système (par exemple, certificats SSL gérés, LB HTTPS, etc.) \- Chiffrement configurable par l'utilisateur ([https://cloud.google.com/security/encryption-in-transit\#user\_config\_encrypt](https://cloud.google.com/security/encryption-in-transit#user_config_encrypt))  
Bonne pratique : mettez en œuvre une interconnexion dédiée pour isoler les données et le trafic de votre organisation de l'Internet public ([https://cloud.google.com/interconnect/docs/concepts/overview](https://cloud.google.com/interconnect/docs/concepts/overview)) \- la fonction des propriétaires du système  
Bonne pratique : configurer Cloud VPN pour protéger davantage les informations en transit ([https://cloud.google.com/vpn/docs/concepts/overview](https://cloud.google.com/vpn/docs/concepts/overview)) \- Fonction IC  
Bonne pratique : mettre en œuvre un ou plusieurs équilibreurs de charge Cloud pour une protection supplémentaire par chiffrement des applications ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer](https://cloud.google.com/load-balancing/docs/choosing-load-balancer)) \- Fonction App/Propriétaire du projet

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

### AC-17 (3)

**Description du contrôle :** Le système d'information achemine tous les accès à distance via un nombre défini par l'organisation de points de contrôle d'accès réseau gérés.

Conseils supplémentaires : les organisations prennent en compte les exigences de l’initiative Trusted Internet Connections (TIC) pour les connexions réseau externes.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de s'assurer que tous leurs accès à distance au système d'information se font via un nombre défini par le client de points de contrôle d'accès réseau gérés.

Décrire comment Google sécurise les données en transit ([https://cloud.google.com/security/overview/whitepaper?hl=fr\#securing\_data\_in\_transit](https://cloud.google.com/security/overview/whitepaper?hl=fr#securing_data_in_transit)) à l'aide de serveurs Google Front End (GFE) et TLS ([https://cloud.google.com/security/encryption-in-transit?hl=fr\#user\_to\_google\_front\_end\_encryption](https://cloud.google.com/security/encryption-in-transit?hl=fr#user_to_google_front_end_encryption)).  
Bonne pratique : mettez en œuvre une interconnexion dédiée pour isoler les données et le trafic de votre organisation de l'Internet public ([https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr](https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr))  
Bonne pratique : configurer Cloud VPN pour protéger davantage les informations en transit ([https://cloud.google.com/vpn/docs/concepts/overview?hl=fr](https://cloud.google.com/vpn/docs/concepts/overview?hl=fr))  
Bonne pratique : mettre en œuvre un ou plusieurs équilibreurs de charge Cloud pour une protection supplémentaire par chiffrement des applications ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer?hl=fr](https://cloud.google.com/load-balancing/docs/choosing-load-balancer?hl=fr))  
Bonne pratique facultative : activer le proxy Cloud Identity Aware ([https://cloud.google.com/iap/docs/concepts-overview?hl=fr](https://cloud.google.com/iap/docs/concepts-overview?hl=fr)) pour gérer et restreindre l'accès à distance aux applications FedRAMP 

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Accès contextuel : fonctionnalité de Cloud IAP qui vous permet de gérer l'accès aux applications et à l'infrastructure en fonction de l'identité et du contexte d'un utilisateur. [https://cloud.google.com/context-aware-access/?hl=fr](https://cloud.google.com/context-aware-access/?hl=fr) 

## Audit et responsabilité (AU)

### AU-3 \- AUDIT ET RESPONSABILITÉ

**Description du contrôle :** Le système d'information génère des enregistrements d'audit contenant des informations qui établissent quel type d'événement s'est produit, quand l'événement s'est produit, où l'événement s'est produit, la source de l'événement, le résultat de l'événement et l'identité de toute personne ou sujet associé à l'événement. .

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

Le modèle Landing Zone déploie un compartiment de stockage verrouillé en tant que bunker de journaux immuable pour stocker les données de journaux médico-légales (à des fins d'audit) à l'aide d'un récepteur de journaux d'organisation. La durée de rétention est configurable.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit

#### Recommandations de mise en œuvre

GCP permet aux développeurs des agences clientes d'écrire du code et de gérer les ressources cloud afin de déterminer quels enregistrements d'audit sont générés et quelles informations sont contenues dans les enregistrements d'audit des clients. Le journal d'activité de l'administrateur GCP produit des enregistrements d'audit contenant suffisamment d'informations pour, au minimum, établir quel type d'événement s'est produit, quand (date et heure) l'événement s'est produit, la source de l'événement, le résultat de l'événement et l'identité. de tout utilisateur/sujet associé à l’événement. Dans le cas du journal d'activité de l'administrateur, « l'endroit où l'événement s'est produit » signifie implicitement qu'il s'est produit dans les projets, dossiers ou organisations GCP du client. En plus du journal d'administration disponible via GCP Cloud Console, les journaux d'application sur l'activité des applications sont disponibles via GCP Cloud Console et les clients ont la possibilité de personnaliser les journaux pour leurs applications.

Les clients peuvent choisir d'utiliser plusieurs outils GCP tels que les journaux d'audit d'administration et les journaux d'accès aux données pour garantir qu'une journalisation adéquate existe pour établir quel type d'événement s'est produit, quand (date et heure) l'événement s'est produit, où l'événement s'est produit, la source de l'événement. , le résultat (succès ou échec) de l'événement et l'identité de tout utilisateur/sujet associé à l'événement. Les clients doivent s'assurer qu'ils configurent correctement les journaux d'audit GCP appropriés, le cas échéant, et qu'ils configurent des journaux supplémentaires si nécessaire.

Considérations relatives à l'espace de travail :

L'agence doit examiner le contenu du journal fourni par l'API Admin SDK Reports et les historiques de révision pour déterminer si le contenu répond aux exigences de journalisation définies par l'agence. De plus, l'agence peut utiliser le SSO basé sur SAML pour autoriser l'accès à Workspace et enregistrer des événements supplémentaires.

Bonne pratique : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources ([https://cloud.google.com/logging/docs/audit/configure-data-access?hl=fr](https://cloud.google.com/logging/docs/audit/configure-data-access?hl=fr))  
Bonne pratique facultatif : activez les journaux de transparence des accès pour savoir quand l'administrateur Google accède à vos données cloud ([https://cloud.google.com/logging/docs/audit/access-transparency-overview?hl=fr](https://cloud.google.com/logging/docs/audit/access-transparency-overview?hl=fr))

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Access Transparency : une fonctionnalité activée dans Stackdriver Logging qui permet aux utilisateurs d'obtenir une visibilité sur les actions du fournisseur de cloud sur vos données via des journaux en temps quasi réel.  
[https://cloud.google.com/access-transparency/?hl=fr](https://cloud.google.com/access-transparency/?hl=fr) 

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)  
    
Centre de sécurité Google Workspace \- Une fonctionnalité Google Workspace ; Informations de sécurité exploitables pour Google Workspace. Tableau de bord de sécurité unifié. Obtenez des informations sur le partage de fichiers externes, une visibilité sur le spam et les logiciels malveillants ciblant les utilisateurs de votre organisation, ainsi que des mesures pour démontrer l'efficacité de votre sécurité dans un tableau de bord unique et complet.  
[https://workspace.google.com/products/admin/security-center/?hl=fr](https://workspace.google.com/products/admin/security-center/?hl=fr)

### AU-3 (1)

**Description du contrôle :** Le système d'information génère des enregistrements d'audit contenant les informations supplémentaires suivantes : durée de la session, de la connexion, de la transaction ou de l'activité ; pour les transactions client-serveur, le nombre d'octets reçus et d'octets envoyés ; des messages d'information supplémentaires pour diagnostiquer ou identifier l'événement ; caractéristiques qui décrivent ou identifient l'objet ou la ressource sur lequel on agit

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- projet de surveillance partagé  
* \- 3-networks-hub-and-spoke/modules/base\_env \- journal de flog réseau 

#### Recommandations de mise en œuvre

GCP permet aux développeurs des agences clientes d'écrire du code et de gérer les ressources cloud afin de déterminer quels enregistrements d'audit sont générés et quelles informations sont contenues dans les enregistrements d'audit des clients. Le journal d'activité de l'administrateur GCP produit des enregistrements d'audit contenant suffisamment d'informations pour, au minimum, établir quel type d'événement s'est produit, quand (date et heure) l'événement s'est produit, la source de l'événement, le résultat de l'événement et l'identité. de tout utilisateur/sujet associé à l’événement. Dans le cas du journal d'activité de l'administrateur, « l'endroit où l'événement s'est produit » signifie implicitement qu'il se produit dans les projets, dossiers ou organisations GCP du client. En plus du journal d'administration disponible via GCP Cloud Console, les journaux d'application sur l'activité des applications sont disponibles via GCP Cloud Console et les clients ont la possibilité de personnaliser les journaux pour leurs applications.

Les clients peuvent choisir d'utiliser plusieurs outils GCP tels que les journaux d'audit d'administration et les journaux d'accès aux données pour garantir qu'une journalisation adéquate existe pour établir quel type d'événement s'est produit, quand (date et heure) l'événement s'est produit, où l'événement s'est produit, la source de l'événement. , le résultat (succès ou échec) de l'événement et l'identité de tout utilisateur/sujet associé à l'événement. Les clients doivent s'assurer qu'ils configurent correctement les journaux d'audit GCP appropriés, le cas échéant, et qu'ils configurent des journaux supplémentaires si nécessaire.

Considérations relatives à l'espace de travail :

L'agence doit examiner le contenu du journal fourni par l'API Admin SDK Reports et les historiques de révision pour déterminer si le contenu répond aux exigences de journalisation définies par l'agence. De plus, l'agence peut utiliser le SSO basé sur SAML pour autoriser l'accès à Workspace et enregistrer des événements supplémentaires.

Bonne pratique : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources ([https://cloud.google.com/logging/docs/audit/configure-data-access?hl=fr](https://cloud.google.com/logging/docs/audit/configure-data-access?hl=fr))  
Bonne pratique facultative : activez les journaux de transparence des accès pour savoir quand l'administrateur Google accède à vos données cloud ([https://cloud.google.com/logging/docs/audit/access-transparency-overview?hl=fr](https://cloud.google.com/logging/docs/audit/access-transparency-overview?hl=fr))

### AU-5

**Description du contrôle :** Le système d'information :

 a. Alerte le personnel ou les rôles définis par l'organisation en cas d'échec du traitement d'audit ; et

 b. Prend les actions supplémentaires suivantes, telles que définies par l'organisation : (par exemple, arrêter le système d'information, écraser les enregistrements d'audit les plus anciens, arrêter de générer des enregistrements d'audit).

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Les journaux et les contrôles sont disponibles à partir de la plateforme IdM sélectionnée, par ex. Google Workspace ou Cloud Identity.

Le système Google Cloud et les journaux d'audit sont gérés dans la suite d'opérations. 

En cas d'échec d'une tâche de traitement d'audit, l'infrastructure de Google réaffecte automatiquement la tâche ayant échoué à une autre ressource disponible. Cela n’entraîne généralement aucun échec réel du traitement de l’audit. Une intervention manuelle dans ce processus est rarement nécessaire.

Si une intervention manuelle est requise, des alertes sont effectuées pour permettre aux groupes responsables de réparer les composants de traitement d'audit qui échouent. L'équipe GCP Site Reliability Engineering (SRE) est alertée. En première ligne d'action, l'équipe SRE isole les composants défaillants et les déconnecte du réseau.

#### Définitions des ressources

* \- 1-org/envs/shared/scc\_notification.tf \- Notification SCC pour tous les résultats actifs

#### Recommandations de mise en œuvre

Les clients sont responsables de la surveillance et de la correction des échecs de traitement d'audit pour leurs systèmes et applications.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)      

Centre de sécurité Google Workspace \- Une fonctionnalité Google Workspace ; Informations de sécurité exploitables pour Google Workspace. Tableau de bord de sécurité unifié. Obtenez des informations sur le partage de fichiers externes, une visibilité sur le spam et les logiciels malveillants ciblant les utilisateurs de votre organisation, ainsi que des mesures pour démontrer l'efficacité de votre sécurité dans un tableau de bord unique et complet.  
[https://workspace.google.com/products/admin/security-center/?hl=fr](https://workspace.google.com/products/admin/security-center/?hl=fr)    

Cloud Pub/Sub – Messagerie globale et même ingestion à grande échelle  
[https://cloud.google.com/pubsub/?hl=fr](https://cloud.google.com/pubsub/?hl=fr) 

Fonctions Cloud – Plateforme de calcul sans serveur basée sur les événements.  
[https://cloud.google.com/functions/?hl=fr](https://cloud.google.com/functions/?hl=fr) 

### AU-7 (1)

**Description du contrôle :** Le système d'information offre la capacité de traiter les enregistrements d'audit pour les événements d'intérêt en fonction des champs d'audit définis par l'organisation dans les enregistrements d'audit.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

Notification d'inventaire des actifs cloud : utilise Google Cloud Asset Inventory pour créer un flux d'événements de modification de stratégie IAM, puis les traite pour détecter lorsqu'un rôle (à partir d'une liste prédéfinie) est attribué à un membre (compte de service, utilisateur ou groupe). Génère ensuite une conclusion SCC avec le membre, le rôle, la ressource pour laquelle il a été accordé et le temps qui a été accordé.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- projet de surveillance partagé  
* \- 3-networks-hub-and-spoke/modules/base\_env \- journal de flog réseau   
* \- 1-org/modules/cai-monitoring \- pour la notification d'inventaire des actifs cloud

#### Recommandations de mise en œuvre

Les clients sont responsables de fournir la capacité de traiter les enregistrements d'audit pour les événements d'intérêt en fonction des champs d'audit dans les enregistrements d'audit.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### AU-8

**Description du contrôle :** Le système d'information :

 a. Utilise les horloges internes du système pour générer des horodatages pour les enregistrements d'audit ; et

 b. Enregistre des horodatages pour les enregistrements d'audit qui peuvent être mappés au temps universel coordonné (UTC) ou au temps moyen de Greenwich (GMT) et répond à une granularité de mesure du temps définie par l'organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La solution fournit des journaux d'audit détaillés de l'activité du système, permettant un suivi et un examen complets. De plus, les solides fonctionnalités de gestion des identités et des accès (IAM) de Google Cloud permettent un contrôle précis des actions des utilisateurs, garantissant ainsi la responsabilité de toutes les interactions au sein de l'environnement cloud.

#### Recommandations de mise en œuvre

GCP permet aux développeurs clients des agences d'écrire du code et de gérer les ressources cloud. Cela inclut l'utilisation des horloges système internes des serveurs de Google pour générer des horodatages pour les journaux d'audit générés par les systèmes clients hébergés dans GCP.

Les clients doivent enregistrer des horodatages pour les enregistrements d'audit qui peuvent être mappés au temps universel coordonné (UTC) ou au temps moyen de Greenwich (GMT) et doivent définir la granularité de la mesure du temps.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Centre de sécurité Google Workspace \- Une fonctionnalité Google Workspace ; Informations de sécurité exploitables pour Google Workspace. Tableau de bord de sécurité unifié. Obtenez des informations sur le partage de fichiers externes, une visibilité sur le spam et les logiciels malveillants ciblant les utilisateurs de votre organisation, ainsi que des mesures pour démontrer l'efficacité de votre sécurité dans un tableau de bord unique et complet.  
[https://workspace.google.com/products/admin/security-center/?hl=fr](https://workspace.google.com/products/admin/security-center/?hl=fr)

### AU-9

**Description du contrôle :** Le système d’information protège les informations d’audit et les outils d’audit contre tout accès, modification et suppression non autorisés.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

#### Définitions des ressources

* \- 1-org/envs/shared/iam.tf \- rôles pour un accès privilégié aux journaux   
* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- projet de surveillance partagé  
* \- 3-networks-hub-and-spoke/modules/base\_env \- journal de flog réseau 

#### Recommandations de mise en œuvre

\- Prend en charge les exigences d'examen, d'analyse et de reporting d'audit à la demande et les enquêtes après coup sur les incidents de sécurité ; et

### AU-9 (2)

**Description du contrôle :** Le système d'information sauvegarde les enregistrements d'audit au moins une fois par semaine sur un système ou un composant de système physiquement différent du système ou du composant audité.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Google Cloud Logs auditera les actions de création, de modification, de désactivation, de suppression et d'activation de compte. ZA centralise ces journaux dans Pub/Sub. Il est de la responsabilité du client d'intégrer ces événements d'audit dans une solution SIEM.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- projet de surveillance partagé  
* \- 3-networks-hub-and-spoke/modules/base\_env \- journal de flog réseau 

#### Recommandations de mise en œuvre

GCP permet aux développeurs clients des agences d'écrire du code et de gérer les ressources cloud. De nombreux services GCP génèrent des journaux d'audit pour les systèmes clients construits sur ces services GCP. Les journaux d'audit sont conservés sur GCP pendant une période déterminée, après quoi ils sont supprimés. Les clients peuvent configurer une destination de sauvegarde pour ces journaux d'audit, afin d'augmenter la période de conservation et d'augmenter le nombre de copies répliquées des journaux à des fins de sauvegarde. La destination de sauvegarde peut être configurée en tant que service physiquement différent sur GCP ou en tant que service/système en dehors de GCP.

Considérations relatives à Google Workspace  
Le CLIENT doit déterminer si la fréquence, l'emplacement et la disponibilité des sauvegardes des journaux d'audit fournies par Google répondent à ses exigences et mettre en œuvre des processus pour sauvegarder les enregistrements d'audit fournis par Google via la console d'administration et les journaux d'audit fournis par l'agence sur un système ou un support différent au moins une fois par semaine.  
Si les informations d'audit sont stockées en dehors de l'application, l'agence est responsable de la protection des informations d'audit contre tout accès, modification et suppression non autorisés.

### AU-12

**Description du contrôle :** Le système d'information :

 a. Fournit une capacité de génération d’enregistrements d’audit pour les événements auditables définis dans AU-2 a. sur tous les composants du système d’information et du réseau où la capacité d’audit est déployée/disponible ;

 b. Permet au personnel ou aux rôles définis par l'organisation de sélectionner les événements auditables qui doivent être audités par des composants spécifiques du système d'information ; et  
   
c. Génère des enregistrements d'audit pour les événements définis dans AU-2 d. avec le contenu défini dans AU-3.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

L'équipe de sécurité de Google exige que tous les composants de l'environnement de production et des applications soient capables de générer les événements auditables définis comme décrit dans AU-2. Ceci est accompli via la politique de journalisation de sécurité.

OS Login simplifie la gestion des accès SSH en liant votre compte utilisateur Linux à votre identité Google. Les administrateurs peuvent facilement gérer l'accès aux instances au niveau d'une instance ou d'un projet en définissant les autorisations IAM.

#### Définitions des ressources

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf pour la journalisation d'audit  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- projet de surveillance partagé  
* \- 3-networks-hub-and-spoke/modules/base\_env \- journal de flog réseau   
* \- 1-org/envs/shared/iam.tf \- rôles pour un accès privilégié aux journaux 

#### Politiques de l'organisation

* AC-3, AU-12 computation.requireOsLogin : cette stratégie nécessite une connexion au système d'exploitation sur les machines virtuelles nouvellement créées pour gérer plus facilement les clés SSH, fournir une autorisation au niveau des ressources avec les stratégies IAM et enregistrer l'accès des utilisateurs. \- Cette stratégie nécessite une connexion au système d'exploitation sur les machines virtuelles nouvellement créées pour gérer plus facilement les clés SSH, fournir une autorisation au niveau des ressources avec les stratégies IAM et enregistrer l'accès des utilisateurs.

#### Recommandations de mise en œuvre

une, b, c. Les clients sont responsables de déterminer les rôles et les responsabilités afin de sélectionner les événements auditables qui doivent être audités par des composants spécifiques du système d'information afin de remplir leurs obligations relatives aux exigences FedRAMP suivantes.

## Gestion des configurations (CM)

### CM-5 (1)

**Description du contrôle :** Le système d'information applique les restrictions d'accès et prend en charge l'audit des mesures d'application.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La base de code de Landing Zone est construite avec Terraform et contrôlée par GitHub. Toutes les modifications apportées à la base de code sont traitées via un processus de révision par fusion/extraction, empêchant toute modification arbitraire du noyau IaC. Les modifications apportées au code ne sont pas reflétées dans l'infrastructure jusqu'à ce que le code soit effectivement déployé via Terraform.

Cependant, une fois le code déployé, la modification de l'infrastructure via des modifications hors bande (c'est-à-dire qu'un utilisateur privilégié modifie l'infrastructure via la console Google Cloud) est possible, mais romprait probablement l'héritage. Toutes les modifications apportées à l'infrastructure doivent être apportées via le processus d'examen de fusion/extraction, et les modifications hors bande doivent être interdites par la politique.

#### Recommandations de mise en œuvre

Les clients sont responsables de l’application des restrictions d’accès et prennent en charge l’audit des actions d’application.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Dépôts sources cloud : stockez, gérez et suivez le code dans un référentiel Git privé entièrement géré. Passez en revue les validations de code et automatisez les builds.  
[https://cloud.google.com/source-repositories/?hl=fr](https://cloud.google.com/source-repositories/?hl=fr)  

Cloud Build : créez, testez et déployez rapidement des logiciels. Définissez des flux de travail personnalisés pour la création, les tests et le déploiement dans plusieurs environnements.   
[https://cloud.google.com/cloud-build/?hl=fr](https://cloud.google.com/cloud-build/?hl=fr)  

Cloud Resource Manager : gérez hiérarchiquement les ressources par projet, dossier et organisation. Contrôlez de manière centralisée les politiques d’organisation et d’accès ainsi que les inventaires d’actifs. Étiquetez les ressources pour une meilleure gestion.   
[https://cloud.google.com/resource-manager/?hl=fr](https://cloud.google.com/resource-manager/?hl=fr)   

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)  

### CM-5 (3)

**Description du contrôle :** Le système d'information empêche l'installation de composants logiciels et micrologiciels définis par l'organisation sans vérifier que le composant a été signé numériquement à l'aide d'un certificat reconnu et approuvé par l'organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Responsabilité du client.

#### Recommandations de mise en œuvre

Les clients sont responsables d'empêcher l'installation de composants logiciels et micrologiciels sans vérifier que le composant a été signé numériquement à l'aide d'un certificat reconnu et approuvé par l'organisation du client.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr) 

Certificats SSL gérés par Google – Un élément de Cloud Load Balancing ; Les certificats SSL gérés par Google sont fournis, renouvelés et gérés pour vos noms de domaine.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr](https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr) 

Certificats SSL gérés par le client : un élément de Cloud Load Balancing ; Fournissez vos propres certificats SSL pour gérer l'accès sécurisé à vos domaines GCP. Les certificats autogérés peuvent prendre en charge les caractères génériques et plusieurs noms alternatifs de sujet (SAN).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr#working-self-managed) 

### CM-7 (2)

**Description du contrôle :** Le système d'information empêche l'exécution du programme conformément aux politiques définies par l'organisation, concernant l'utilisation et les restrictions des logiciels ; et/ou des règles autorisant les termes et conditions d'utilisation du logiciel.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Responsabilité du client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la configuration de leur système d'information afin d'empêcher l'exécution des programmes conformément aux politiques relatives à l'utilisation et aux restrictions des logiciels ; règles autorisant les termes et conditions d’utilisation des logiciels.

## Plans d'urgence (PC)

### CP-10(2)

**Description du contrôle :** Le système d'information met en œuvre la récupération des transactions pour les systèmes basés sur les transactions.

Conseils supplémentaires : les systèmes d'information basés sur les transactions comprennent, par exemple, les systèmes de gestion de bases de données et les systèmes de traitement des transactions. Les mécanismes prenant en charge la récupération des transactions incluent, par exemple, l'annulation des transactions et la journalisation des transactions.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Responsabilité du client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la mise en œuvre de la récupération des transactions pour leurs systèmes basés sur les transactions.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud Deployment Manager \- Créez des modèles déclaratifs qui spécifient toutes les ressources nécessaires à votre déploiement cloud. Établissez un processus de déploiement reproductible et basé sur des modèles.  
[https://cloud.google.com/deployment-manager/?hl=fr](https://cloud.google.com/deployment-manager/?hl=fr)	 

Guide de planification de reprise après sinistre de Google – Ce que vous devez savoir pour concevoir et mettre en œuvre un plan de reprise après sinistre. Cas d'utilisation et implémentations spécifiques de DR sur GCP. Remarque : Ce n'est pas un produit GCP  
[https://cloud.google.com/solutions/dr-scenarios-planning-guide?hl=fr](https://cloud.google.com/solutions/dr-scenarios-planning-guide?hl=fr) 

Groupes d'instances gérés : maintenez la haute disponibilité de vos applications en maintenant de manière proactive vos instances dans un état RUNNING. Les groupes d'instances gérés prennent en charge la mise à l'échelle automatique, l'équilibrage de charge, les mises à jour progressives et la réparation automatique.  
[https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances?hl=fr](https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances?hl=fr) 

## Identification et authentification (IA)

### IA-2 \- IDENTIFICATION ET AUTHENTIFICATION

**Description du contrôle :** Le système d'information identifie et authentifie de manière unique les utilisateurs de l'organisation (ou les processus agissant au nom des utilisateurs de l'organisation).

Remarque : Les organisations peuvent satisfaire aux exigences d'identification et d'authentification de ce contrôle avec les solutions MFA.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Il est recommandé au client de mettre en œuvre l'authentification unique à l'aide de son fournisseur IDp existant et de le synchroniser avec Cloud Identity/Google Workspace. Avec la mise en œuvre du SSO, toutes les procédures MFA en place aujourd’hui seront héritées aujourd’hui par la plateforme. La configuration de la synchronisation des identités est un processus qui nécessite une configuration manuelle, elle ne peut pas être automatisée à l'aide de Terraform et doit donc être configurée en dehors du flux de la zone d'accueil automatisée.

L’application MFA est une bonne pratique lors de l’administration des utilisateurs. Les comptes Google.com nécessitent toujours une authentification multifacteur basée sur le matériel. Google estime que l'activation de la MFA est le meilleur moyen de protéger les comptes contre le phishing et recommande aux partenaires et aux clients de toujours l'activer.

Ce contrôle est généralement assuré via une stratégie de bris de glace.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
De par sa conception, Google n'impose pas l'utilisation de SAML SSO sur la console d'administration, car si la solution SSO de l'agence n'est pas disponible, les administrateurs de domaine de l'agence ne pourront pas administrer le service Workspace. Google recommande aux agences d'utiliser la vérification en deux étapes pour les administrateurs de domaine afin de restreindre l'accès à la console d'administration. S'ils mettent en œuvre l'authentification SAML SSO, les clients doivent s'assurer que toutes les pages de connexion Google sont configurées pour pointer vers le portail SSO de l'agence. Pour les systèmes FIPS 199 à niveau d’impact modéré, une authentification multifacteur est requise. Lors de l'utilisation de SAML-SSO avec des installations de Workspace sur un appareil mobile (par exemple, Apple iOS, Android, Blackberry), un ordinateur de bureau ou un client lourd (par exemple, Outlook), des considérations de mise en œuvre supplémentaires s'appliquent en fonction de la configuration du contrôle AC et IA de l'agence. mise en œuvre et peut nécessiter que les mots de passe soient stockés dans le service d'authentification des applications de Google comme décrit ci-dessus. Au lieu de SAML, les agences peuvent également choisir d'activer la vérification en deux étapes (décrite ci-dessous).  
Si les agences choisissent d'utiliser la vérification en deux étapes de Google et choisissent l'option d'authentification par clé de sécurité, elles doivent noter que les clés de sécurité gérées par l'administrateur à l'échelle du domaine et la gestion des clés de sécurité ne sont disponibles que pour les clients Workspace Business et Workspace Enterprise Edition.

Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue ou une description du moment où les utilisateurs de son organisation doivent se déconnecter. Les clients de l'agence doivent former les employés à la fonctionnalité de déconnexion du système et au comportement attendu du système, et exiger la déconnexion lorsque la session de l'utilisateur est terminée ou conformément aux directives de l'agence.

Décrire comment les comptes de service dans GCP sont considérés à la fois comme des ressources et des identités ([https://cloud.google.com/iam/docs/understanding-service-accounts?hl=fr](https://cloud.google.com/iam/docs/understanding-service-accounts?hl=fr)) et comment Cloud IAM est utilisé pour authentifier et autoriser les comptes de service à accéder aux ressources cloud.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### AI-2 (1)

**Description du contrôle :** Le système d'information met en œuvre une authentification multifacteur pour l'accès réseau aux comptes privilégiés.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client. 

La Landing Zone utilise des rôles prédéfinis, des rôles IAM personnalisés et des comptes de service pour restreindre de manière appropriée la configuration des ressources. Le modèle Landing Zone utilise également Identity Aware Proxy, une fonctionnalité qui utilise l'identité et le contexte pour protéger l'accès aux services et aux machines virtuelles. IAP peut être utilisé pour fournir un tunnel sécurisé vers les ressources GCP et remplace le concept Bastion Host (référencé dans les modules projet et pare-feu).

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris la mise en œuvre de l'authentification multifacteur pour l'accès aux comptes clients privilégiés. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Lors de l'utilisation de SAML-SSO avec des installations de Workspace sur un appareil mobile (par exemple, Apple iOS, Android, Blackberry), un ordinateur de bureau ou un client lourd (par exemple, Outlook), des considérations de mise en œuvre supplémentaires s'appliquent en fonction de la configuration du contrôle AC et IA de l'agence. mise en œuvre et peut nécessiter que les mots de passe soient stockés dans le service d'authentification des applications de Google, comme décrit dans IA-2. Ce SSP n'envisage pas l'utilisation de clients « lourds » et traite uniquement l'accès via un navigateur Web. Au lieu de SAML, les agences peuvent également choisir d'activer la vérification en deux étapes (décrite ci-dessous) pour accéder à la console d'administration.  
Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue ou une description du moment où les utilisateurs de son organisation doivent se déconnecter. Les clients de l'agence doivent former les employés à la fonctionnalité de déconnexion du système et au comportement attendu du système, et exiger la déconnexion lorsque la session de l'utilisateur est terminée ou conformément aux directives de l'agence.

Bonne pratique : appliquer MFA/2SV pour un accès privilégié à Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr](https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr)) à l'aide de Cloud Identity

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### AI-2 (2)

**Description du contrôle :** Le système d'information met en œuvre une authentification multifacteur pour l'accès réseau aux comptes non privilégiés.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

La Landing Zone utilise des rôles prédéfinis, des rôles IAM personnalisés et des comptes de service pour restreindre de manière appropriée la configuration des ressources. Le modèle Landing Zone utilise également Identity Aware Proxy, une fonctionnalité qui utilise l'identité et le contexte pour protéger l'accès aux services et aux machines virtuelles. IAP peut être utilisé pour fournir un tunnel sécurisé vers les ressources GCP et remplace le concept Bastion Host (référencé dans les modules projet et pare-feu).

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris la mise en œuvre de l'authentification multifacteur pour l'accès aux comptes clients non privilégiés. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Lors de l'utilisation de SAML-SSO avec des installations de Workspace sur un appareil mobile (par exemple, Apple iOS, Android, Blackberry), un ordinateur de bureau ou un client lourd (par exemple, Outlook), des considérations de mise en œuvre supplémentaires s'appliquent en fonction de la configuration de la mise en œuvre des contrôles AC et IA de l'agence et peut exiger que les mots de passe soient stockés dans le service d'authentification des applications de Google, comme décrit dans IA-2. Au lieu de SAML, les agences peuvent également choisir d'activer la vérification en deux étapes (décrite ci-dessous) pour accéder à la console d'administration.  
Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue ou une description du moment où les utilisateurs de son organisation doivent se déconnecter. Les clients de l'agence doivent former les employés à la fonctionnalité de déconnexion du système et au comportement attendu du système, et exiger la déconnexion lorsque la session de l'utilisateur est terminée ou conformément aux directives de l'agence.

Bonne pratique : appliquer MFA/2SV pour un accès non privilégié à Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr](https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr)) à l'aide de Cloud Identity

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AI-2 (8)

**Description du contrôle :** Le système d'information met en œuvre des mécanismes d'authentification résistants à la relecture pour l'accès réseau aux comptes privilégiés.

Conseils supplémentaires : les processus d'authentification résistent aux attaques par réexécution s'il est impossible de réussir les authentifications en réexécutant les messages d'authentification précédents. Les techniques résistantes à la relecture incluent, par exemple, des protocoles qui utilisent des noms occasionnels ou des défis tels que Transport Layer Security (TLS) et des authentificateurs ponctuels synchrones dans le temps ou à défi-réponse.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en veillant à ce que des mécanismes d'authentification résistants à la relecture soient utilisés pour l'authentification des utilisateurs. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AI-2 (11)

**Description du contrôle :** Le système d'information met en œuvre une authentification multifacteur pour l'accès à distance aux comptes privilégiés et non privilégiés de telle sorte que l'un des facteurs est fourni par un périphérique distinct du système accédant et que le périphérique répond à la FIPS 140-2, à la certification NIAP ou à l'approbation de la NSA.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client. 

La Landing Zone utilise des rôles prédéfinis, des rôles IAM personnalisés et des comptes de service pour restreindre de manière appropriée la configuration des ressources. Le modèle Landing Zone utilise également Identity Aware Proxy, une fonctionnalité qui utilise l'identité et le contexte pour protéger l'accès aux services et aux machines virtuelles. IAP peut être utilisé pour fournir un tunnel sécurisé vers les ressources GCP et remplace le concept Bastion Host (référencé dans les modules projet et pare-feu).

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris la mise en œuvre de l'authentification multifacteur pour les utilisateurs clients et la garantie que les appareils utilisés par leur système d'authentification multifacteur pour accéder à Google Cloud sont fournis par un appareil distinct du système d'accès. et que l'appareil est conforme à la norme FIPS 140-2, à la certification NIAP ou à l'approbation de la NSA. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables d'utiliser l'authentification multifacteur pour leurs utilisateurs et de s'assurer que les appareils utilisés par leur système d'authentification multifacteur pour accéder à Google Cloud sont fournis par un appareil distinct du système d'accès et que l'appareil est conforme à la norme FIPS 140-2, certification NIAP. , ou approbation de la NSA.

Considérations relatives à l'espace de travail :  
L'agence doit utiliser la console d'administration pour configurer la vérification en 2 étapes afin de fournir un accès à distance aux comptes privilégiés et non privilégiés.  
L'agence devrait mettre en œuvre une authentification multifacteur à l'aide du SSO basé sur SAML. L'authentification multifactorielle serait établie avec l'entité émettant l'assertion SAML à Google. Les utilisateurs s'authentifient via le fournisseur SAML sur leur domaine et les utilisateurs privilégiés, tels que les administrateurs, pourraient alors accéder à la console d'administration du domaine. Si l'agence choisit de mettre en œuvre la fonctionnalité de vérification en deux étapes, tous les utilisateurs doivent s'inscrire à la vérification en deux étapes et sélectionner la méthode pour recevoir leur code de vérification sur leur téléphone mobile : l'application Google Authenticator, un SMS ou un appel téléphonique. S'ils mettent en œuvre l'authentification SAML SSO, les clients doivent s'assurer que toutes les pages de connexion Google sont configurées pour pointer vers le portail SSO de l'agence. Pour les systèmes FIPS 199 à niveau d’impact modéré, une authentification multifacteur est requise.

Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue ou une description du moment où les utilisateurs de son organisation doivent se déconnecter. Les clients de l'agence doivent également former leurs employés à la fonctionnalité de déconnexion décrite précédemment et au comportement attendu du système.

Bonne pratique : appliquer MFA/2SV pour un accès non privilégié à Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr](https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr)) à l'aide de Cloud Identity

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### AI-2 (12)

**Description du contrôle :** Le système d'information accepte et vérifie électroniquement les informations d'identification de vérification de l'identité personnelle (PIV).

Conseils supplémentaires : les informations d'identification de vérification de l'identité personnelle (PIV) sont les informations d'identification délivrées par les agences fédérales qui sont conformes à la publication FIPS 201 et aux documents d'orientation à l'appui.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en s'assurant que le système d'information accepte et vérifie électroniquement les informations d'identification PIV dans les systèmes d'authentification de leur agence pour les utilisateurs clients. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Les clients de l'agence doivent configurer et utiliser le SSO basé sur SAML pour s'authentifier auprès des services Workspace, ce qui leur permet d'hériter des authentificateurs à deuxième facteur mis en œuvre dans leur agence, tels que PIV. L'agence devrait envisager d'utiliser des mécanismes automatisés tels que LDAP, SSO, etc. pour prendre en charge la gestion de l'espace de travail.

Bonne pratique : appliquer MFA/2SV pour un accès non privilégié à Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr](https://cloud.google.com/identity/solutions/enforce-mfa?hl=fr) ) à l'aide de Cloud Identity

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### IA-3

**Description du contrôle :** Le système d'information identifie et authentifie de manière unique les appareils définis par l'organisation, spécifiques et/ou types avant d'établir une connexion locale, distante ou réseau.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Google décrit ce contrôle comme non applicable pour GCP et/ou Workspace.

Comment Google applique ce contrôle pour l'infrastructure commune de Google (GCI) :  
L'équipe de sécurité de Google exige que tous les appareils de l'environnement de production se voient attribuer une adresse IP unique dans un espace de noms privé à des fins d'identification. Les machines de l'environnement de production se voient attribuer un nom d'hôte unique lors de l'installation. Les restrictions IP VLAN autorisent uniquement les appareils autorisés à établir des connexions réseau. Dans le cadre de la configuration, des certificats spécifiques à la machine sont générés et installés sur chaque machine ; un certificat de machine est requis pour que les ordinateurs portables et les postes de travail puissent se connecter au réseau d'entreprise de Google

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### AI-5 (1)

**Description du contrôle :** Le système d'information, pour l'authentification par mot de passe :

 (a) Applique la complexité minimale des mots de passe selon les exigences définies par l'organisation en matière de respect de la casse, de nombre de caractères, de mélange de lettres majuscules, de lettres minuscules, de chiffres et de caractères spéciaux, y compris les exigences minimales pour chaque type ;

 (b) Applique au moins un caractère modifié lorsque de nouveaux mots de passe sont créés ;

 (c) Stocke et transmet uniquement des représentations cryptées de mots de passe ;

 (d) Applique les restrictions de durée de vie minimale et maximale des mots de passe des numéros définis par l'organisation pour la durée de vie minimale et maximale ;

 (e) Interdit la réutilisation des mots de passe pendant 24 générations ; et

 (f) Permet l'utilisation d'un mot de passe temporaire pour les connexions au système avec une modification immédiate en un mot de passe permanent.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris l'application d'une complexité minimale de mot de passe pour l'authentification par mot de passe. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Partie B :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en s'assurant qu'au moins un caractère a changé lors de la création de nouveaux mots de passe. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Partie C :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en veillant à ce que les mots de passe soient protégés par chiffrement lors du stockage et de la transmission. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Partie D :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en veillant à ce que les mots de passe soient protégés par chiffrement lors du stockage et de la transmission. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Partie e :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en veillant à ce que les mots de passe des clients ne soient pas réutilisés pendant 24 générations. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Partie f :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Cela inclut, si des mots de passe temporaires sont utilisés dans le système client, l'émission de mots de passe temporaires pour les connexions au système avec une modification immédiate en mot de passe permanent. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Les agences doivent utiliser l'API Admin SDK Directory/SSO basé sur SAML pour répondre au niveau d'impact FIPS 199 modéré.  
L'agence est responsable de la gestion de l'authentification par mot de passe, notamment :

Établir une longueur minimale de mot de passe de 12 caractères et imposer une complexité minimale de mot de passe d'au moins un de chaque : respect de la casse, mélange de lettres majuscules, de lettres minuscules, de chiffres et de caractères spéciaux ;  
Appliquer au moins un (1) caractère de mot de passe modifié lorsque de nouveaux mots de passe sont créés ;  
s'assurer que TLS est activé sur le domaine pour garantir une transmission sécurisée sur HTTPS ; et,  
Appliquer les restrictions d'un (1) jour minimum de mot de passe et de 60 jours maximum de durée de vie définies par l'agence ; et  
Interdire la réutilisation des mots de passe pendant 24 générations.  
Permet l'utilisation d'un mot de passe temporaire pour les connexions au système avec une modification immédiate en mot de passe permanent.  
Les appareils mobiles sont exclus de l'exigence de complexité du mot de passe.

Si une agence choisit de ne pas utiliser SAML SSO, elle est chargée de définir une période d'inactivité prévue ou une description du moment où les utilisateurs de son organisation doivent se déconnecter. Les clients de l'agence doivent former les employés à la fonctionnalité de déconnexion du système et au comportement attendu du système, et exiger la déconnexion lorsque la session de l'utilisateur est terminée ou conformément aux directives de l'agence.

Bonne pratique : utiliser Cloud Identity pour configurer des politiques de mot de passe pour les identités gérées dans le cloud (https://support.google.com/cloudidentity/answer/139399?hl=en)  
Bonne pratique : activer l'authentification unique (SSO) pour les applications basées sur le cloud ([https://cloud.google.com/identity/solutions/enable-sso?hl=fr](https://cloud.google.com/identity/solutions/enable-sso?hl=fr) )

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AI-5 (2)

**Description du contrôle :** Le système d'information, pour l'authentification par PKI :

 (a) Valide les certifications en construisant et en vérifiant un chemin de certification vers une ancre de confiance acceptée, y compris en vérifiant les informations sur l'état du certificat ;

 (b) Applique l'accès autorisé à la clé privée correspondante ;

 (c) mappe l'identité authentifiée sur le compte de l'individu ou du groupe ; et

 (d) Implémente un cache local de données de révocation pour prendre en charge la découverte et la validation du chemin en cas d'impossibilité d'accéder aux informations de révocation via le réseau.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de la gestion de l’infrastructure PKI client et de l’authentification dans leurs systèmes. Cela inclut la validation des certificats en construisant et en vérifiant le chemin de certification vers une ancre de confiance acceptée. Les clients peuvent choisir d'utiliser le service Cloud Key Management Service (Cloud KMS) au sein de la famille de produits GCP Identity & Security pour répondre à cette exigence. Cloud KMS est un service de gestion de clés hébergé dans le cloud qui permet aux clients de gérer le chiffrement de leurs services cloud.

Partie B :  
Les clients sont responsables de la gestion de l’infrastructure PKI client et de l’authentification dans leurs systèmes. Cela inclut l’application de l’accès autorisé aux clés privées des clients. Les clients peuvent utiliser le service Cloud Key Management pour les aider à gérer les clés client.

Partie C :  
Les clients sont responsables de la gestion de l’infrastructure PKI client et de l’authentification dans leurs systèmes. Cela inclut le mappage des identités authentifiées des identifiants clients avec des individus ou des groupes de clients. Les clients peuvent utiliser le service Cloud Key Management pour les aider à gérer les clés client.

Partie D :  
Les clients sont responsables de la gestion de l’infrastructure PKI client et de l’authentification dans leurs systèmes. Cela inclut la mise en œuvre d'un cache local de données de révocation pour la PKI de l'utilisateur. Les clients peuvent utiliser le service Cloud Key Management pour les aider à gérer les clés client.

Considérations relatives à l'espace de travail :  
Les agences clientes sont responsables du respect des exigences FedRAMP lors de la configuration de l'accès via le SSO basé sur SAML. Les agences doivent utiliser la configuration de la console d'administration SSO basée sur SAML. Pour l'authentification basée sur la PKI des clients d'agence, les clients d'agence doivent (a) valider les certificats en construisant un chemin de certification avec des informations d'état vers une ancre de confiance acceptée, (b) appliquer l'accès autorisé à la clé privée correspondante et (c) mapper l'identité authentifiée à le compte utilisateur, d) Mettre en œuvre un cache local des données de révocation pour prendre en charge la découverte et la validation du chemin en cas d'impossibilité d'accéder aux informations de révocation via le réseau

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Services de confiance Google \- L'infrastructure à clé publique de Google (« Google PKI ») permet une authentification d'identité fiable et sécurisée et facilite la préservation de la confidentialité et de l'intégrité des données dans les transactions électroniques. Remarque : Il ne s'agit pas d'un produit GCP.  
[https://pki.goog/](https://pki.goog/) 

### IA-5 (11)

**Description du contrôle :** Le système d'information, pour l'authentification basée sur des jetons matériels, utilise des mécanismes qui satisfont aux exigences de qualité des jetons définies par l'organisation.

Conseils supplémentaires : L'authentification matérielle basée sur des jetons fait généralement référence à l'utilisation de jetons basés sur PKI, tels que la carte de vérification d'identité personnelle (PIV) du gouvernement américain. Les organisations définissent des exigences spécifiques pour les jetons, comme le travail avec une PKI particulière.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris l'utilisation de jetons matériels qui répondent à leurs exigences. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Bonne pratique : Appliquer MFA/2SV pour les utilisateurs GCP privilégiés via les clés de sécurité Titan ([https://cloud.google.com/titan-security-key?hl=fr](https://cloud.google.com/titan-security-key?hl=fr)) comme authentification matérielle supplémentaire dans le cloud.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### IA-6

**Description du contrôle :** Le système d'information masque le retour d'informations d'authentification pendant le processus d'authentification afin de protéger les informations contre une éventuelle exploitation/utilisation par des personnes non autorisées.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, notamment en veillant à ce que les commentaires de l'authentificateur soient masqués pendant le processus d'authentification du client. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
L'agence doit garantir que les assertions SAML envoyées à Google sont sécurisées pendant la transmission afin de protéger les informations contre une éventuelle exploitation/utilisation par des personnes non autorisées.

Google utilise par défaut le cryptage en transit avec TLS depuis les utilisateurs finaux (Internet) vers tous les services Google.

Bonne pratique : mettez en œuvre une interconnexion dédiée pour isoler les données et le trafic de votre organisation de l'Internet public (lien)  
Bonne pratique : configurer Cloud VPN pour protéger davantage les informations en transit (lien)  
Bonne pratique : exploiter Cloud KMS pour chiffrer les données avec des clés de chiffrement symétriques et asymétriques (lien)

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Console : console de gestion intégrée conforme à FedRAMP pour GCP. Interface d'administration sécurisée pour se connecter à toutes les ressources et services GCP.  
[https://cloud.google.com/cloud-console/?hl=fr](https://cloud.google.com/cloud-console/?hl=fr) 

Google Application Layer Transport Security \- L'Application Layer Transport Security (ALTS) de Google est un système d'authentification mutuelle et de cryptage de transport généralement utilisé pour sécuriser les communications d'appel de procédure à distance (RPC) au sein de l'infrastructure de Google. Remarque : Il ne s'agit pas d'un produit GCP.  
[https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security/?hl=fr](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security/?hl=fr) 

Sécurité de l'infrastructure de Google : livre blanc qui donne un aperçu de la sécurité de l'infrastructure de Google pour le matériel, les services, l'identité des utilisateurs, le stockage, les communications et les opérations. Remarque : Il ne s'agit pas d'un produit GCP.  
https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf?utm\_medium=et\&utm\_source=google.com%2Fcloud\&utm\_campaign=multilayered\_security\&utm\_content=download\_the\_whitepaper   

### IA-7

**Description du contrôle :** Le système d'information met en œuvre des mécanismes d'authentification auprès d'un module cryptographique qui répondent aux exigences des lois fédérales applicables, des décrets, des directives, des politiques, des réglementations, des normes et des orientations pour une telle authentification.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Cela peut être réalisé en utilisant un système d'authentification unique géré par le client, basé sur SAML, et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Les clients sont responsables de la mise en œuvre de mécanismes d'authentification qui répondent à toutes les exigences applicables pour une telle authentification. De plus, les clients doivent s'assurer que les machines des clients se connectant à Google Cloud sont configurées pour utiliser le cryptage approprié pour les communications entre Google et l'agence.

Considérations relatives à l'espace de travail :  
Les agences clientes sont responsables de la configuration de leurs navigateurs et connexions côté client sur les postes de travail, serveurs et appareils mobiles applicables pour activer les connexions utilisant le cryptage. Les clients doivent appliquer les paramètres USGCB sur les postes de travail fournis par le gouvernement pour établir des connexions avec des chiffrements approuvés par FIPS.

Google utilise BoringSSL (une implémentation TLS gérée par Google avec BoringCrypto validé FIPS 140-2 niveau 1 (lien)  
Bonne pratique : exploitez Cloud KMS et/ou Cloud HSM pour créer, appliquer, gérer et protéger des clés cryptographiques dans le cloud conformément à la norme FIPS 140-2 niveau 3 (lien)

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr) 

### IA-8

**Description du contrôle :** Le système d'information identifie et authentifie de manière unique les utilisateurs non organisationnels (ou les processus agissant pour le compte d'utilisateurs non organisationnels).

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Hors de portée de la zone d'accueil. Système SSO géré par le client. 

Le modèle Landing Zone déploie une stratégie organisationnelle pour appliquer le partage restreint de domaine. Cela autorise uniquement les ID d'annuaire dans la liste des domaines autorisés en tant qu'entité GCP IAM, bloquant ainsi tous les autres comptes d'organisation, tels que, sans s'y limiter, les comptes Gmail.

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Cela inclut l'identification et l'authentification de manière unique des utilisateurs clients non organisationnels (ou des processus agissant au nom d'utilisateurs clients non organisationnels). Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
L'agence doit activer/désactiver les paramètres publics/privés pour chaque application dans la console d'administration conformément aux spécifications de l'agence.

Bonne pratique facultative : mettre en œuvre Cloud IAP ([https://cloud.google.com/iap?hl=fr](https://cloud.google.com/iap?hl=fr)) pour protéger l'accès aux applications et aux machines virtuelles \- Propriétaires de projets/applications

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### AI-8 (1)

**Description du contrôle :** Le système d'information accepte et vérifie électroniquement les informations d'identification de vérification de l'identité personnelle (PIV) provenant d'autres agences fédérales.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Ce contrôle ne s'applique pas à GCP, car GCP n'accepte ni ne vérifie directement les informations d'identification PIV des clients gouvernementaux. GCP accepte les assertions SAML pour authentifier les utilisateurs qui se sont authentifiés auprès d'un système d'authentification client via PIV.

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP, y compris l'acceptation et la vérification électronique des informations d'identification PIV dans les systèmes d'authentification de leur agence pour les utilisateurs clients. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Les clients de l'agence doivent configurer et utiliser le SSO basé sur SAML pour s'authentifier auprès des services Workspace, ce qui leur permet d'hériter des authentificateurs à deuxième facteur mis en œuvre dans leur agence, tels que PIV. L'agence devrait envisager d'utiliser des mécanismes automatisés tels que LDAP, SSO, etc. pour prendre en charge la gestion de l'espace de travail.

### AI-8 (2)

**Description du contrôle :** Le système d'information n'accepte que les identifiants tiers agréés par la FICAM.

Conseils supplémentaires : les informations d'identification tierces sont les informations d'identification délivrées par des entités gouvernementales non fédérales approuvées par l'initiative Federal Identity, Credential, and Access Management (FICAM) Trust Framework Solutions. Les informations d'identification tierces approuvées satisfont ou dépassent l'ensemble des exigences minimales de maturité organisationnelle, technique, de sécurité, de confidentialité et de l'ensemble du gouvernement fédéral.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Ce contrôle ne s'applique pas à GCP, car GCP n'accepte ni ne vérifie directement les informations d'identification FICAM des clients gouvernementaux. GCP accepte les assertions SAML pour authentifier les utilisateurs qui se sont authentifiés auprès d'un système d'authentification client via des informations d'identification tierces approuvées par la FICAM.

Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Cela inclut l'acceptation uniquement des informations d'identification de tiers approuvées par la FICAM dans les systèmes d'authentification de leurs agences pour les utilisateurs clients. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Si les administrateurs de domaine client accordent l'accès à leur domaine Workspace à des utilisateurs non organisationnels, les agences sont responsables d'accepter uniquement les informations d'identification tierces approuvées par la FICAM et de configurer l'authentification unique à l'aide de SAML 2.0 ou Web SSO pour hériter des contrôles d'authentification de leur agence.

### AI-8 (4)

**Description du contrôle :** Le système d'information est conforme aux profils émis par la FICAM.

Conseils supplémentaires : profils de mise en œuvre de protocoles approuvés publiés par la FICAM (par exemple, les protocoles d'authentification FICAM tels que SAML 2.0 et OpenID 2.0, ainsi que d'autres protocoles tels que FICAM Backend Attribute Exchange).

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Ce contrôle ne s'applique pas à GCP, car GCP n'accepte ni ne vérifie directement les informations d'identification FICAM des clients gouvernementaux. GCP accepte les assertions SAML pour authentifier les utilisateurs qui se sont authentifiés auprès d'un système d'authentification client via des informations d'identification tierces approuvées par la FICAM.

Responsabilité du client :  
Les clients sont responsables de la gestion de tous les aspects de l'authentification des utilisateurs clients de GCP. Cela inclut la conformité aux profils émis par la FICAM dans les systèmes d'authentification de leurs agences pour les utilisateurs clients. Ceci peut être réalisé en utilisant un système d'authentification unique basé sur SAML géré par le client et en synchronisant ce système avec GCP via Google Cloud Directory Sync.

Considérations relatives à l'espace de travail :  
Si les administrateurs de domaine client accordent l'accès à leur domaine Workspace à des utilisateurs non organisationnels, les agences sont responsables d'accepter uniquement les informations d'identification tierces approuvées par la FICAM et de configurer l'authentification unique à l'aide de SAML 2.0 ou Web SSO pour hériter des contrôles d'authentification de leur agence.

Bonnes pratiques : activez l'authentification unique pour que votre organisation gère l'accès aux applications cloud/SaaS ([https://cloud.google.com/identity/solutions/enable-sso?hl=fr](https://cloud.google.com/identity/solutions/enable-sso?hl=fr))

## indéfini (RA)

### DA-5 (5)

**Description du contrôle :** Le système d’information met en œuvre une autorisation d’accès privilégié aux systèmes d’exploitation/applications web/base de données pour toutes les activités d’analyse des vulnérabilités.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable de la mise en œuvre de l’autorisation d’accès aux systèmes d’exploitation/applications Web/base de données pour toutes les activités d’analyse des vulnérabilités.

## Protection du système et des communications (SC)

### SC-2

**Description du contrôle :** Le système d'information sépare les fonctionnalités utilisateur (y compris les services d'interface utilisateur) des fonctionnalités de gestion du système d'information.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Responsabilité du client. 

Les applications et les informations/données ne sont pas présentes dans la solution (il s'agit d'une solution d'infrastructure uniquement) avant l'intégration de la charge de travail du client. Toutes les politiques nécessaires au partitionnement des applications relèveraient de la responsabilité du propriétaire de l'application/des informations/des données et seraient traitées dans leur réponse à ce contrôle.

#### Recommandations de mise en œuvre

Il appartient au client de séparer les fonctionnalités utilisateur des fonctionnalités de gestion du système d’information.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Google Workspace : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://workspace.google.com/?hl=fr](https://workspace.google.com/?hl=fr)

### SC-4

**Description du contrôle :** Le système d'information empêche le transfert d'informations non autorisé et involontaire via des ressources système partagées.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable d’empêcher le transfert d’informations non autorisées et involontaires via des ressources système partagées.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

Accès privé à Google : composant de Cloud VPC utilisé pour accéder en toute sécurité aux services Google et aux SaaS tiers depuis le site vers le cloud, à l'aide de Cloud Interconnect ou d'un VPN.  
[https://cloud.google.com/vpc/docs/private-access-options?hl=fr](https://cloud.google.com/vpc/docs/private-access-options?hl=fr)

Accès contextuel : fonctionnalité de Cloud IAP qui vous permet de gérer l'accès aux applications et à l'infrastructure en fonction de l'identité et du contexte d'un utilisateur.  
[https://cloud.google.com/context-aware-access/?hl=fr](https://cloud.google.com/context-aware-access/?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### SC-5 \- PROTECTION DES SYSTÈMES ET DES COMMUNICATIONS

**Description du contrôle :** Le système d'information protège contre ou limite les effets des types d'attaques par déni de service définis par l'organisation ou de la référence à la source de ces informations en employant des mesures de sécurité définies par l'organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

L'infrastructure GCP (console GCP, API, etc.) est protégée par le service Google Front End ([https://cloud.google.com/docs/security/infrastructure/design](https://cloud.google.com/docs/security/infrastructure/design))

Google Cloud Armor aide à protéger vos applications et sites Web contre le déni de service et les attaques Web.

Les applications clientes peuvent utiliser Google Cloud Armor au sein de l'infrastructure de la solution pour fournir une protection DoS au niveau de l'application. Une partie de ce contrôle serait abordée dans l'évaluation de la sécurité des applications clientes.

Les clients doivent déployer Cloud Armor pour une protection par défaut supplémentaire sous la forme d'une atténuation des attaques DDoS L7 basée sur le ML, du top 10 OWASP, des attaques LB et de la gestion des robots via reCAPTCHA.

#### Recommandations de mise en œuvre

Les clients sont responsables de s'assurer que les ressources de leurs systèmes d'information construites sur GCP sont protégées contre ou limitent les effets des attaques par déni de service. Les machines virtuelles des clients ne se trouvent pas derrière Google Front End (GFE) et nécessitent une protection supplémentaire contre les attaques DDOS. Les clients peuvent choisir d'utiliser l'équilibreur de charge multirégional GCP dans le produit Compute Engine pour bénéficier de la protection DDoS de Google ; activer l'équilibrage de charge HTTP(s) et proxy SSL de Google Cloud pour leurs instances GCE afin d'atténuer les attaques DDoS ; activer Cloud Armor pour les équilibreurs de charge HTTP(s) ou GKE ; ou acheter et configurer un autre produit commercial. Les équilibreurs de charge Google Cloud peuvent gérer une augmentation soudaine du trafic en répartissant le trafic sur tous les back-ends disposant de la capacité disponible.

GCP fournit une sécurité réseau native et une protection contre le déni de service à l'aide de Google Front Ends (GFE). Les GFE terminent le trafic pour le trafic proxy HTTP(S), TCP et TLS entrant, fournissent des contre-mesures contre les attaques DDoS, et acheminent et équilibrent la charge du trafic vers les services Google Cloud ([https://cloud.google.com/security/encryption-in-transit?hl=fr\#how\_traffic\_gets\_routed](https://cloud.google.com/security/encryption-in-transit?hl=fr#how_traffic_gets_routed)).  
Bonne pratique : configurez Cloud Armor pour protéger davantage vos services contre le déni de service et les attaques Web ([https://cloud.google.com/armor?hl=fr](https://cloud.google.com/armor?hl=fr)). Configurer les stratégies de sécurité Cloud Armor pour filtrer le trafic entrant ([https://cloud.google.com/armor/docs/configure-security-policies?hl=fr](https://cloud.google.com/armor/docs/configure-security-policies?hl=fr)).

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Armor – Protégez votre infrastructure et vos applications Web contre les attaques par déni de service distribué (DDoS).  
[https://cloud.google.com/armor/?hl=fr](https://cloud.google.com/armor/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Google Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Google Cloud Load Balancing : implémentez l'autoscaling du réseau mondial, HTTP(S), TCP, SSL et l'équilibrage de charge interne   
[https://cloud.google.com/load-balancing/?hl=fr](https://cloud.google.com/load-balancing/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

### SC-6

**Description du contrôle :** Le système d'information protège la disponibilité des ressources en allouant les ressources définies par l'organisation par priorité ou par quota, ainsi que par des mesures de sécurité définies par l'organisation.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable de la protection contre ou de limiter les effets des types d'attaques par déni de service définis par l'organisation ou de référence à la source de ces informations en employant des mesures de sécurité définies par l'organisation.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Resource Manager : gérez hiérarchiquement les ressources par projet, dossier et organisation. Contrôlez de manière centralisée les politiques d’organisation et d’accès ainsi que les inventaires d’actifs. Étiquetez les ressources pour une meilleure gestion.   
[https://cloud.google.com/resource-manager/?hl=fr](https://cloud.google.com/resource-manager/?hl=fr)

Google Cloud Storage – Stockage d'objets avec mise en cache globale en périphérie. Options de stockage d'archives multirégionales, régionales, Nearline \- accès basse fréquence et Coldline \-.   
[https://cloud.google.com/storage/?hl=fr](https://cloud.google.com/storage/?hl=fr)

Groupes d'instances gérés : maintenez la haute disponibilité de vos applications en maintenant de manière proactive vos instances dans un état RUNNING. Les groupes d'instances gérés prennent en charge la mise à l'échelle automatique, l'équilibrage de charge, les mises à jour progressives et la réparation automatique.  
[https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances?hl=fr](https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances?hl=fr)

Ressources mondiales, régionales et zonales : bénéficiez d'une haute disponibilité en tirant parti des ressources Google Cloud mondiales, zonales et régionales. Remarque : Ce n'est pas un produit GCP  
[https://cloud.google.com/compute/docs/regions-zones/global-regional-zonal-resources?hl=fr](https://cloud.google.com/compute/docs/regions-zones/global-regional-zonal-resources?hl=fr)

Quotas de ressources Google Cloud : gérez vos quotas de taux GCP pour les requêtes d'API et les quotas d'allocation de ressources. Remarque : Ce n'est pas un produit GCP  
[https://cloud.google.com/docs/quota?hl=fr](https://cloud.google.com/docs/quota?hl=fr)

### SC-7

**Description du contrôle :** Le système d'information :

 a. Surveille et contrôle les communications à la limite externe du système et aux limites internes clés du système ;

 b. Met en œuvre des sous-réseaux pour les composants du système accessibles au public qui sont physiquement et logiquement séparés des réseaux organisationnels internes ; et

 c. Se connecte à des réseaux ou systèmes d'information externes uniquement via des interfaces gérées constituées de dispositifs de protection des limites disposés conformément à une architecture de sécurité organisationnelle.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Le réseau VPC permet des règles de pare-feu entrantes et sortantes pour autoriser ou limiter le flux d'informations en fonction des IP ou des ports de couche 4\.

La configuration du réseau et des ressources est définie dans 3 réseaux en étoile. Ce ZA utilise des appareils Fortigate comme périphériques frontaux, ceci est défini dans 7-fortigate. 

Protection des limites assurée par les contrôles de service VPC, l'accès privé à Google et le NGFW 1p ou 3p.  

Access Context Manager (ACM) vous aide à sécuriser vos ressources Google Cloud en fournissant un cadre permettant de définir et d'appliquer des politiques de contrôle d'accès précises basées sur divers attributs contextuels. 

Reportez-vous à Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env \- définit l'architecture réseau et la configuration du journal de flog réseau  
* \- 3-networks-hub-and-spoke/modules/restricted\_shared\_vpc/service\_control.tf \- définit les politiques d'accès et l'adhésion  
* \- 7-fortigate \- définition du périphérique frontal

#### Politiques de l'organisation

* SC-7 computing.restrictVpcPeering : vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP. \- Vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP.  
* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité.  \- Cette autorisation contrôle si une instance de VM peut agir comme un routeur réseau, transmettant des paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité. 

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes clients GCP sont connectées aux systèmes réseau externes via des interfaces gérées cohérentes avec l'architecture de sécurité de l'organisation. Tout le trafic des utilisateurs et des applications n'est pas surveillé par Google. Les applications hébergées sur GCP peuvent contourner le GFE si elles utilisent Cloud VPN, Cloud Interconnect ou une VM à instance unique (car elles utilisent une adresse IP publique par défaut). Les clients peuvent segmenter leurs réseaux avec des pare-feu distribués mondiaux pour restreindre l'accès à certaines instances.

Partie B :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes d'information GCP sont connectées aux systèmes de réseau externes uniquement via des interfaces gérées. Les machines virtuelles des clients disposent d'adresses IP publiques et peuvent se connecter à Internet par défaut. Les clients peuvent choisir d'utiliser le cloud privé virtuel situé dans le produit de mise en réseau. Les clients peuvent provisionner des ressources GCP en segmentant leurs réseaux avec un pare-feu distribué mondial pour restreindre l'accès à certaines instances.

Partie C :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes clients GCP sont connectées aux systèmes réseau externes via des interfaces gérées cohérentes avec l'architecture de sécurité de l'organisation. Tout le trafic des utilisateurs et des applications n'est pas surveillé par Google. Les applications hébergées sur GCP peuvent contourner le GFE si elles utilisent Cloud VPN, Cloud Interconnect ou une VM à instance unique (car elles utilisent une adresse IP publique par défaut). Les clients peuvent segmenter leurs réseaux avec des pare-feu distribués mondiaux pour restreindre l'accès à certaines instances.

Bonne pratique : mettre en œuvre VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr)) pour bloquer l'accès externe aux services protégés par le périmètre.  
Bonne pratique : activer les journaux de flux VPC ([https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr](https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr)) pour surveiller le trafic réseau envoyé vers/depuis les instances de VM  
Bonne pratique : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources ([https://cloud.google.com/logging/docs/audit?hl=fr\#admin-activity](https://cloud.google.com/logging/docs/audit?hl=fr#admin-activity))

#### Remarques sur les services

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

Accès privé à Google : composant de Cloud VPC utilisé pour accéder en toute sécurité aux services Google et aux SaaS tiers depuis le site vers le cloud, à l'aide de Cloud Interconnect ou d'un VPN.  
[https://cloud.google.com/vpc/docs/private-access-options?hl=fr](https://cloud.google.com/vpc/docs/private-access-options?hl=fr)

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### SC-7 (5)

**Description du contrôle :** Le système d'information au niveau des interfaces gérées refuse le trafic de communications réseau par défaut et autorise le trafic de communications réseau par exception (c'est-à-dire tout refuser, autoriser par exception).

Conseils supplémentaires : cette amélioration du contrôle s'applique au trafic de communications réseau entrant et sortant. Une politique de trafic de communications réseau de type refus tout et autorisation par exception garantit que seules les connexions essentielles et approuvées sont autorisées.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Le réseau VPC permet des règles de pare-feu entrantes et sortantes pour autoriser ou limiter le flux d'informations en fonction des IP ou des ports de couche 4\.

Le modèle Landing Zone a une posture de refus par défaut pour les règles de pare-feu VPC ; une correspondance de règle doit exister pour permettre au trafic de traverser le VPC. L'entrée/sortie dans l'environnement est restreinte via le projet de périmètre et le VPC. Le trafic est bloqué par défaut et des règles spécifiques doivent être créées pour permettre la communication ([https://cloud.google.com/vpc/docs/vpc?hl=fr\#communications\_and\_access](https://cloud.google.com/vpc/docs/vpc?hl=fr#communications_and_access))

La configuration du réseau et des ressources est définie dans 3 réseaux en étoile. Ce ZA utilise des appareils Fortigate comme périphériques frontaux, ceci est défini dans 7-fortigate. 

Protection des limites assurée par les contrôles de service VPC, l'accès privé à Google et le NGFW 1p ou 3p. 

Reportez-vous à Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env \- définit l'architecture réseau et la configuration du journal de flog réseau  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- définit le refus de sortie par défaut  
* \- 7-fortigate \- définition du périphérique frontal

#### Politiques de l'organisation

* SC-7 computing.restrictVpcPeering : vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP. \- Vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP.  
* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité.  \- Cette autorisation contrôle si une instance de VM peut agir comme un routeur réseau, transmettant des paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité. 

#### Recommandations de mise en œuvre

Les clients sont responsables de la mise en œuvre d’un refus de tout ; autoriser par stratégie d’exception au niveau de leurs interfaces gérées.

Bonne pratique facultative : vérifier et/ou activer la journalisation des règles de pare-feu ([https://cloud.google.com/vpc/docs/firewall-rules-logging?hl=fr](https://cloud.google.com/vpc/docs/firewall-rules-logging?hl=fr)) pour auditer, vérifier et analyser les effets de vos règles de pare-feu.  
Bonne pratique : mettre en œuvre VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr)) pour bloquer l'accès externe aux services protégés par le périmètre.  
Bonne pratique : activer les journaux de flux VPC ([https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr](https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr)) pour surveiller le trafic réseau envoyé vers/depuis les instances de VM \- Fonction App/Propriétaire du projet

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

### SC-7 (7)

**Description du contrôle :** Le système d'information, en conjonction avec un dispositif distant, empêche le dispositif d'établir simultanément des connexions non distantes avec le système et de communiquer via une autre connexion avec des ressources dans des réseaux externes.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Les services Cloud VPN, ainsi que les configurations au niveau des appareils, empêchent le tunneling fractionné pour les appareils distants. Identity Aware Proxy applique des contrôles d'accès granulaires basés sur l'identité et le contexte de l'utilisateur, tels que l'état de sécurité de l'appareil, l'emplacement et le réseau.

Toutes les connexions des appareils aux ressources de la solution sont distantes ; aucune connexion directe (non locale) n'est possible car Google n'autorise pas les connexions directes (locales) à GCP

#### Définitions des ressources

* \- 3-networks-dual-svpc/modules/vpn-ha \- Un exemple de configuration pour VPN est fourni.   
* \- 4-projects/modules/base\_env/example\_peering\_project.tf \- Exemples de règles de pare-feu IAP.  Les ressources IAP ne sont pas créées par défaut. 

#### Politiques de l'organisation

* SC-7 computing.restrictVpcPeering : vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP.   
* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité. 

#### Recommandations de mise en œuvre

Le CLIENT est responsable d'empêcher l'appareil d'établir simultanément des connexions non distantes avec le système et de communiquer via une autre connexion avec des ressources dans des réseaux externes.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

Accès privé à Google : composant de Cloud VPC utilisé pour accéder en toute sécurité aux services Google et aux SaaS tiers depuis le site vers le cloud, à l'aide de Cloud Interconnect ou d'un VPN.  
[https://cloud.google.com/vpc/docs/private-access-options?hl=fr](https://cloud.google.com/vpc/docs/private-access-options?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### SC-7 (8)

**Description du contrôle :** Le système d'information achemine le trafic de communications interne défini par l'organisation vers des réseaux externes définis par l'organisation via des serveurs proxy authentifiés au niveau d'interfaces gérées.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Le réseau VPC permet des règles de pare-feu entrantes et sortantes pour autoriser ou limiter le flux d'informations en fonction des IP ou des ports de couche 4\.

La configuration du réseau et des ressources est définie dans 3 réseaux en étoile. Ce ZA utilise des appareils Fortigate comme périphériques frontaux, ceci est défini dans 7-fortigate. 

Protection des limites assurée par les contrôles de service VPC, l'accès privé à Google et le NGFW 1p ou 3p. 

Reportez-vous à Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env \- définit l'architecture réseau et la configuration du journal de flog réseau  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- définit le refus de sortie par défaut  
* \- 7-fortigate \- définition du périphérique frontal

#### Politiques de l'organisation

* SC-7 computing.restrictVpcPeering : vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP.   
* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité. 

#### Recommandations de mise en œuvre

Les clients sont responsables de la gestion des serveurs proxy authentifiés au niveau des interfaces gérées par le client. Les serveurs proxy doivent être configurés pour acheminer le trafic interne et externe conformément aux exigences de l'Agence.

Les Google Front Ends (GFE) sont distribués à l'échelle mondiale pour le trafic proxy entrant vers les services Google ([https://cloud.google.com/security/encryption-in-transit?hl=fr\#how\_traffic\_gets\_routed](https://cloud.google.com/security/encryption-in-transit?hl=fr#how_traffic_gets_routed)).  
Bonne pratique : configurez Cloud Armor pour protéger davantage vos services contre le déni de service et les attaques Web ([https://cloud.google.com/armor?hl=fr](https://cloud.google.com/armor?hl=fr)). Configurer les stratégies de sécurité Cloud Armor pour filtrer le trafic entrant ([https://cloud.google.com/armor/docs/configure-security-policies?hl=fr](https://cloud.google.com/armor/docs/configure-security-policies?hl=fr)).  
Bonne pratique : configurez les équilibreurs de charge Google pour faciliter l'acheminement et la gestion du trafic mondial, régional, externe et interne ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer?hl=fr](https://cloud.google.com/load-balancing/docs/choosing-load-balancer?hl=fr)).

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

Accès privé à Google : composant de Cloud VPC utilisé pour accéder en toute sécurité aux services Google et aux SaaS tiers depuis le site vers le cloud, à l'aide de Cloud Interconnect ou d'un VPN.  
[https://cloud.google.com/vpc/docs/private-access-options?hl=fr](https://cloud.google.com/vpc/docs/private-access-options?hl=fr)

Cloud Identity Aware Proxy : utilisez l'identité et le contexte pour protéger l'accès à vos applications et VM.  
[https://cloud.google.com/iap/?hl=fr](https://cloud.google.com/iap/?hl=fr)

### SC-7 (18)

**Description du contrôle :** Le système d'information tombe en panne de manière sécurisée en cas de panne opérationnelle d'un dispositif de protection des limites.  
   
Conseils supplémentaires : les défaillances des dispositifs de protection des limites ne peuvent pas conduire ou provoquer l'entrée d'informations externes aux dispositifs, et les défaillances ne peuvent pas non plus permettre la diffusion d'informations non autorisées.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Le réseau VPC permet des règles de pare-feu entrantes et sortantes pour autoriser ou limiter le flux d'informations en fonction des IP ou des ports de couche 4\.

La configuration du réseau et des ressources est définie dans 3 réseaux en étoile. Ce ZA utilise des appareils Fortigate comme périphériques frontaux, ceci est défini dans 7-fortigate. 

Protection des limites assurée par les contrôles de service VPC, l'accès privé à Google et le NGFW 1p ou 3p. 

Reportez-vous à Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env \- définit l'architecture réseau et la configuration du journal de flog réseau  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- définit le refus de sortie par défaut  
* \- 7-fortigate \- définition du périphérique frontal

#### Politiques de l'organisation

* SC-7 computing.restrictVpcPeering : vous permet de mettre en œuvre la segmentation du réseau et de contrôler le flux d'informations au sein de votre environnement GCP.   
* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité. 

#### Recommandations de mise en œuvre

Les clients sont responsables de la configuration de tous les dispositifs de protection des limites gérés par le client pour qu'ils échouent dans un état sécurisé.

Bonne pratique : mettre en œuvre Cloud Interconnect et Cloud Load Balancing pour les capacités de reprise après sinistre réseau et la haute disponibilité ([https://cloud.google.com/solutions/dr-scenarios-building-blocks?hl=fr\#networking\_and\_data\_transfer](https://cloud.google.com/solutions/dr-scenarios-building-blocks?hl=fr#networking_and_data_transfer)). 

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr) 

### SC-8

**Description du contrôle :** Le système d'information protège la confidentialité et l'intégrité des informations transmises.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Toutes les communications vers les ressources Google se font via TLS 1.2 ou supérieur (https est spécifié pour toutes les chaînes de connexion et les consoles Google redirigent toutes automatiquement http vers https), garantissant la confidentialité et l'intégrité des informations en transit. L'accès aux postes de travail gérés par l'organisation est obligatoire et ils sont configurés avec des versions de navigateur et des chiffrements à jour.

Toutes les communications avec Azure DevOps (dépôt) et Entra ID se font via TLS 1.2 ou supérieur.

VPC Service Controls est configuré pour bloquer l'accès externe aux services protégés par le périmètre.  
Les journaux de flux VPC sont configurés pour surveiller le trafic réseau envoyé vers/depuis les instances de VM  
Les journaux d'audit sont configurés pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources.

#### Politiques de l'organisation

* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité.   
* SC-8 computing.restrictLoadBalancerCreationForTypes : cette autorisation vous permet de restreindre les types d'équilibreurs de charge qui peuvent être créés dans votre projet. Cela permet d'éviter la création non autorisée ou accidentelle d'équilibreurs de charge qui pourraient exposer vos services à des risques ou à des attaques inutiles.  
* SC-8 computing.requireTlsForLoadBalancers : cette contrainte impose l'utilisation de Transport Layer Security (TLS) pour la communication avec les équilibreurs de charge dans GCP. Il s'aligne sur plusieurs principes et contrôles clés décrits dans le NIST.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes clients GCP sont connectées aux systèmes réseau externes via des interfaces gérées cohérentes avec l'architecture de sécurité de l'organisation. Tout le trafic des utilisateurs et des applications n'est pas surveillé par Google. Les applications hébergées sur GCP peuvent contourner le GFE si elles utilisent Cloud VPN, Cloud Interconnect ou une VM à instance unique (car elles utilisent une adresse IP publique par défaut). Les clients peuvent segmenter leurs réseaux avec des pare-feu distribués mondiaux pour restreindre l'accès à certaines instances.

Partie B :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes d'information GCP sont connectées aux systèmes de réseau externes uniquement via des interfaces gérées. Les machines virtuelles des clients disposent d'adresses IP publiques et peuvent se connecter à Internet par défaut. Les clients peuvent choisir d'utiliser le cloud privé virtuel situé dans le produit de mise en réseau. Les clients peuvent provisionner des ressources GCP en segmentant leurs réseaux avec un pare-feu distribué mondial pour restreindre l'accès à certaines instances.

Partie C :  
Les clients sont responsables de s'assurer que les ressources de leurs systèmes clients GCP sont connectées aux systèmes réseau externes via des interfaces gérées cohérentes avec l'architecture de sécurité de l'organisation. Tout le trafic des utilisateurs et des applications n'est pas surveillé par Google. Les applications hébergées sur GCP peuvent contourner le GFE si elles utilisent Cloud VPN, Cloud Interconnect ou une VM à instance unique (car elles utilisent une adresse IP publique par défaut). Les clients peuvent segmenter leurs réseaux avec des pare-feu distribués mondiaux pour restreindre l'accès à certaines instances.

Bonne pratique : mettre en œuvre VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=fr)) pour bloquer l'accès externe aux services protégés par le périmètre.  
Bonne pratique : activer les journaux de flux VPC ([https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr](https://cloud.google.com/vpc/docs/using-flow-logs?hl=fr)) pour surveiller le trafic réseau envoyé vers/depuis les instances de VM  
Bonne pratique : il peut être utile d'activer les journaux d'audit d'accès aux données pour les composants système spécifiques gérés par les propriétaires du système, afin de consigner davantage l'accès aux ressources ([https://cloud.google.com/logging/docs/audit?hl=fr\#admin-activity](https://cloud.google.com/logging/docs/audit?hl=fr#admin-activity))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud CDN – Réseau de diffusion de contenu à faible latence et à faible coût. Tire parti des points de présence périphériques distribués à l'échelle mondiale de Google pour accélérer la diffusion de contenu pour les sites Web et les applications servies à partir de Google Compute Engine et de Google Cloud Storage. Sécurise le contenu à l'aide de SSL/TLS.  
[https://cloud.google.com/cdn/?hl=fr](https://cloud.google.com/cdn/?hl=fr)

### SC-8 (1)

**Description du contrôle :** Le système d'information met en œuvre des mécanismes cryptographiques pour empêcher la divulgation non autorisée d'informations et détecter les modifications apportées aux informations pendant la transmission, sauf protection contraire par un système de distribution de protection (PDS) renforcé ou alarmé.

Conseils supplémentaires : Le cryptage des informations à transmettre protège les informations contre toute divulgation et modification non autorisées. Les mécanismes cryptographiques mis en œuvre pour protéger l'intégrité des informations comprennent, par exemple, les fonctions de hachage cryptographique qui ont une application courante dans les signatures numériques, les sommes de contrôle et les codes d'authentification de message. Les mesures alternatives de sécurité physique incluent, par exemple, les systèmes de distribution protégés.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Toutes les communications vers les ressources Google se font via TLS 1.2 ou supérieur (https est spécifié pour toutes les chaînes de connexion et les consoles Google redirigent toutes automatiquement http vers https), garantissant la confidentialité et l'intégrité des informations en transit. L'accès aux postes de travail gérés par l'organisation est obligatoire et ils sont configurés avec des versions de navigateur et des chiffrements à jour.

Toutes les communications avec Azure DevOps (dépôt) et Entra ID se font via TLS 1.2 ou supérieur.

GCP intègre le cryptage L4 par défaut lors du transit entre tous les services Google. Le cryptage L7 est disponible.

#### Politiques de l'organisation

* SC-7, SC-8 Compute.vmCanIpForward : cette autorisation contrôle si une instance de VM peut agir en tant que routeur réseau, transmettant les paquets IP entre différentes interfaces réseau. L'activation du transfert IP sur une machine virtuelle la transforme essentiellement en routeur, ce qui peut avoir des implications importantes en matière de sécurité.   
* SC-8 computing.restrictLoadBalancerCreationForTypes : cette autorisation vous permet de restreindre les types d'équilibreurs de charge qui peuvent être créés dans votre projet. Cela permet d'éviter la création non autorisée ou accidentelle d'équilibreurs de charge qui pourraient exposer vos services à des risques ou à des attaques inutiles.   
* SC-8 computing.requireTlsForLoadBalancers : cette contrainte impose l'utilisation de Transport Layer Security (TLS) pour la communication avec les équilibreurs de charge dans GCP. Il s'aligne sur plusieurs principes et contrôles clés décrits dans le NIST.

#### Recommandations de mise en œuvre

Les clients doivent s'assurer que les machines qui se connectent à GCP sont configurées pour utiliser le cryptage approprié pour les communications entre Google et l'agence. Il est de la responsabilité des clients fédéraux de configurer leurs navigateurs pour répondre aux normes fédérales de cryptage.

Considérations relatives à l'espace de travail :  
Les agences clientes sont responsables de la configuration de leurs navigateurs et connexions côté client sur les postes de travail, serveurs et appareils mobiles applicables pour activer les connexions utilisant le cryptage. Les clients doivent appliquer les paramètres USGCB sur les postes de travail fournis par le gouvernement pour établir des connexions avec des chiffrements approuvés par FIPS.

Google utilise le chiffrement en transit avec TLS ([https://cloud.google.com/security/encryption-in-transit\#encryption\_in\_transit\_by\_default](https://cloud.google.com/security/encryption-in-transit#encryption_in_transit_by_default)) par défaut des utilisateurs finaux (Internet) vers tous les services Google. S'il n'est pas déjà configuré, activez le chiffrement Cloud KMS pour les données gérées par les propriétaires du système (par exemple, les journaux d'audit/buckets GCS).  
Bonne pratique : mettez en œuvre une interconnexion dédiée pour isoler les données et le trafic de votre organisation de l'Internet public ([https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr](https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr))   
Bonne pratique : configurer Cloud VPN pour protéger davantage les informations en transit ([https://cloud.google.com/vpn/docs/concepts/overview?hl=fr](https://cloud.google.com/vpn/docs/concepts/overview?hl=fr))   
Bonne pratique : exploiter Cloud KMS pour chiffrer les données avec des clés de chiffrement symétriques et asymétriques ([https://cloud.google.com/kms/docs/encrypt-decrypt?hl=fr](https://cloud.google.com/kms/docs/encrypt-decrypt?hl=fr))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr) 

Certificats SSL gérés par Google – Une fonctionnalité d'équilibrage de charge cloud ; Les certificats SSL gérés par Google sont fournis, renouvelés et gérés pour vos noms de domaine.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr](https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr)

Certificats SSL gérés par le client : une fonctionnalité d'équilibrage de charge cloud ; Fournissez vos propres certificats SSL pour gérer l'accès sécurisé à vos domaines GCP. Les certificats autogérés peuvent prendre en charge les caractères génériques et plusieurs noms alternatifs de sujet (SAN).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates#working-self-managed)

VM protégées : la VM protégée offre une intégrité vérifiable de vos instances de VM Compute Engine. Vous pouvez donc être sûr que vos instances n'ont pas été compromises par des logiciels malveillants ou des rootkits au niveau du démarrage ou du noyau. L'intégrité vérifiable de la VM protégée est obtenue grâce à l'utilisation du démarrage sécurisé, du démarrage mesuré compatible avec le module de plateforme virtuelle de confiance (vTPM) et de la surveillance de l'intégrité.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr](https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr)

### SC-10

**Description du contrôle :** Le système d'information met fin à la connexion réseau associée à une session de communication à la fin de la session ou après un délai maximum de 30 minutes pour les sessions basées sur RAS ou après un délai maximum de 60 minutes pour les sessions utilisateur non interactives d'inactivité.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Compte tenu de la nature SAML et transactionnelle des appels HTTPS et API, il n'y a pas de « sessions » spécifiques à terminer. La réauthentification du compte est requise toutes les 16 heures ([https://cloud.google.com/blog/products/identity-security/improve-security-posture-with-time-bound-session-length?hl=fr](https://cloud.google.com/blog/products/identity-security/improve-security-posture-with-time-bound-session-length?hl=fr)) qui répond à un objectif similaire et satisfera à ce contrôle.

Hors de portée de la zone d'accueil. Système SSO géré par le client.

#### Recommandations de mise en œuvre

Considérations relatives à Google Workspace :  
Les clients Google Workspace Entreprise et Business peuvent configurer une durée de résiliation de session Google (durée de vie des cookies) aussi courte qu'une (1) heure (https://support.google.com/a/answer/7576830?hl=en). Il convient de noter que pour que ces paramètres prennent effet, les utilisateurs de l'Agence doivent se déconnecter et se reconnecter pour lancer la nouvelle application de la durée de session. Il est également possible pour les administrateurs d'agence de réinitialiser manuellement les cookies de connexion d'un utilisateur pour chaque utilisateur (https://support.google.com/a/answer/178854?hl=en). Les agences qui décident de mettre en œuvre une durée de terminaison de session inférieure à une (1) heure doivent mettre en œuvre le SSO basé sur SAML ainsi que l'USGCB pour les postes de travail/ordinateurs portables de l'agence, qui expirent l'utilisateur au niveau du poste de travail/ordinateur portable après une période d'inactivité spécifiée par le agence.  
Les clients de l'agence doivent se déconnecter de Chrome Sync sur les navigateurs et les appareils qu'ils n'utilisent plus.

Les clients de l'agence sont tenus de se connecter uniquement à Chrome Sync via leur compte d'agence, sur l'appareil fourni par leur agence et d'effectuer le travail d'agence uniquement lorsqu'ils sont connectés à leur compte d'agence afin d'éviter tout flux accidentel d'informations vers d'autres comptes.

GSA a accepté la déclaration de mise en œuvre alternative ci-dessous (voir pièce jointe 14, n° 42) : POA\&M \#39 \- Cette mise en œuvre alternative a été acceptée par GSA.

Les agences doivent mettre en œuvre l'authentification unique basée sur SAML ainsi que l'USGCB pour les postes de travail/ordinateurs portables de l'agence, qui expirent l'utilisateur au niveau du poste de travail/ordinateur portable après une période d'inactivité spécifiée par l'agence.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Drainage de connexion \- Une fonctionnalité d'équilibrage de charge cloud ; Vous pouvez activer le drainage de connexion sur les services backend. Pour activer la vidange de connexion, vous définissez un délai d’expiration de connexion sur le service backend. Ce délai d'attente indique au service backend de migrer progressivement le trafic des instances de VM dans ses backends.  
[https://cloud.google.com/load-balancing/docs/enabling-connection-draining?hl=fr](https://cloud.google.com/load-balancing/docs/enabling-connection-draining?hl=fr)

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Cloud Shell : limitations des sessions : les sessions non interactives se termineront automatiquement après un avertissement. Cloud Shell a également des limites d'utilisation hebdomadaires  
[https://cloud.google.com/shell/docs/limitations?hl=fr](https://cloud.google.com/shell/docs/limitations?hl=fr)

### SC-13

**Description du contrôle :** Le système d'information met en œuvre une cryptographie validée FIPS ou approuvée par la NSA conformément aux lois fédérales, décrets, directives, politiques, réglementations et normes fédéraux applicables.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Toutes les communications vers les ressources Google se font via TLS 1.2 ou supérieur (https est spécifié pour toutes les chaînes de connexion et les consoles Google redirigent toutes automatiquement http vers https), garantissant la confidentialité et l'intégrité des informations en transit. L'accès aux postes de travail gérés par l'organisation est obligatoire et ils sont configurés avec des versions de navigateur et des chiffrements à jour.

Toutes les communications avec Azure DevOps (dépôt) et Entra ID se font via TLS 1.2 ou supérieur.

GCP intègre le cryptage L4 par défaut lors du transit entre tous les services Google. Le cryptage L7 est disponible.

GCP intègre des clés de sécurité gérées par Google avec rotation par défaut pour le cryptage du stockage. Des solutions de clés de sécurité fournies et gérées par le client sont également disponibles.

Ressources:   
\- 2-environments/modules/env\_baseline/kms.tf \- projet de gestion de clés séparé

#### Recommandations de mise en œuvre

Les clients doivent s'assurer que les machines se connectant à Google Cloud sont configurées pour utiliser le cryptage approprié pour les communications entre Google et l'agence.

Considérations relatives à l'espace de travail  
Pour établir une connexion cryptée avec des algorithmes approuvés FIPS 140-2, les agences clientes sont responsables de la configuration de leurs navigateurs et connexions côté client sur les postes de travail, serveurs et appareils mobiles applicables pour activer les connexions utilisant le cryptage. Google applique TLS sur tous les serveurs Workspace pour gérer les connexions client. Les clients qui appliquent les paramètres USGCB sur les postes de travail fournis par le gouvernement obtiendront un cryptage fort avec des algorithmes approuvés FIPS.

Google utilise BoringSSL (une implémentation TLS gérée par Google) avec BoringCrypto validé FIPS 140-2 niveau 1 ([https://cloud.google.com/security/encryption-in-transit\#boringssl](https://cloud.google.com/security/encryption-in-transit#boringssl)).  
Politique de sécurité du module cryptographique BoringCrypto de Google ([https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp2964.pdf](https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp2964.pdf))  
Bonne pratique : exploitez Cloud KMS et/ou Cloud HSM pour créer, appliquer, gérer et protéger les clés cryptographiques dans le cloud conformément à la norme FIPS 140-2 niveau 3 ([https://cloud.google.com/kms/docs/hsm?hl=fr](https://cloud.google.com/kms/docs/hsm?hl=fr))

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr)

### SC-20

**Description du contrôle :** Le système d'information :

 un. Fournit des artefacts supplémentaires d’origine et d’intégrité des données ainsi que les données de résolution de nom faisant autorité que le système renvoie en réponse aux requêtes externes de résolution de nom/adresse ; et

 b. Fournit les moyens d'indiquer l'état de sécurité des zones enfants et (si l'enfant prend en charge les services de résolution sécurisés) de permettre la vérification d'une chaîne de confiance entre les domaines parent et enfant, lorsqu'ils fonctionnent dans le cadre d'un espace de noms distribué et hiérarchique.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de la configuration des navigateurs Web pour exiger des connexions sécurisées lors de l'ouverture de connexions à GCP. De plus, les clients doivent configurer les appareils des utilisateurs finaux pour qu'ils utilisent uniquement des serveurs DNS de confiance pour gérer la résolution des noms de domaine.

Bonne pratique : configurer Cloud DNS avec des zones gérées ([https://cloud.google.com/dns/docs/overview?hl=fr](https://cloud.google.com/dns/docs/overview?hl=fr\\)). Implémenter DNSSEC ([https://cloud.google.com/dns/docs/dnssec?hl=fr](https://cloud.google.com/dns/docs/dnssec?hl=fr)) pour imposer l'authentification des recherches de noms de domaine. Lorsqu'elle est activée, la journalisation Cloud DNS suit les requêtes résolues par les serveurs de noms pour les réseaux VPC ([https://cloud.google.com/dns/docs/monitoring?hl=fr](https://cloud.google.com/dns/docs/monitoring?hl=fr)).  
Bonne pratique : créer des zones DNS privées pour effectuer une résolution DNS interne pour les réseaux GCP privés ([https://cloud.google.com/dns/zones?hl=fr\#create-private-zone](https://cloud.google.com/dns/zones?hl=fr#create-private-zone))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud DNS – Service DNS (Domain Name System) faisant autorité, évolutif, fiable, résilient et géré. Publiez et gérez facilement des millions de zones et d'enregistrements DNS.  
[https://cloud.google.com/dns/?hl=fr](https://cloud.google.com/dns/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

### SC-21

**Description du contrôle :** Le système d'information demande et effectue une authentification de l'origine des données et une vérification de l'intégrité des données sur les réponses de résolution de nom/adresse que le système reçoit de sources faisant autorité.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Les clients sont responsables de la configuration des navigateurs Web pour exiger des connexions sécurisées lors de l'ouverture de connexions à GCP. De plus, les clients doivent configurer les appareils des utilisateurs finaux pour qu'ils utilisent uniquement des serveurs DNS de confiance pour gérer la résolution des noms de domaine.

Considérations relatives à l'espace de travail :  
Google ne fournit pas de DNS dans le cadre de notre offre Workspace, et le DNS utilisé par Google n'entre pas dans le champ d'application des limites d'autorisation GCI et Workspace.  
Les agences doivent effectuer une authentification de l'origine des données et une vérification de l'intégrité des données sur les réponses de résolution de nom/adresse provenant de sources faisant autorité, à la demande des systèmes clients.

Implémentations de sécurité du DNS public de Google ([https://developers.google.com/speed/public-dns/docs/security?hl=fr](https://developers.google.com/speed/public-dns/docs/security?hl=fr)).    
Bonne pratique : configurer Cloud DNS avec des zones gérées ([https://cloud.google.com/dns/docs/overview?hl=fr](https://cloud.google.com/dns/docs/overview?hl=fr)). Implémenter DNSSEC ([https://cloud.google.com/dns/docs/dnssec?hl=fr](https://cloud.google.com/dns/docs/dnssec?hl=fr)) pour imposer l'authentification des recherches de noms de domaine. Lorsqu'elle est activée, la journalisation Cloud DNS suit les requêtes résolues par les serveurs de noms pour les réseaux VPC ([https://cloud.google.com/dns/docs/monitoring?hl=fr](https://cloud.google.com/dns/docs/monitoring?hl=fr)).  
Bonne pratique : créer des zones DNS privées pour effectuer une résolution DNS interne pour les réseaux GCP privés ([https://cloud.google.com/dns/zones?hl=fr\#create-private-zone](https://cloud.google.com/dns/zones?hl=fr#create-private-zone))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud DNS – Service DNS (Domain Name System) faisant autorité, évolutif, fiable, résilient et géré. Publiez et gérez facilement des millions de zones et d'enregistrements DNS.  
[https://cloud.google.com/dns/?hl=fr](https://cloud.google.com/dns/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

VPC Service Controls : une fonctionnalité VPC permettant de protéger les données sensibles dans les services Google Cloud Platform à l'aide de périmètres de sécurité.  
[https://cloud.google.com/vpc-service-controls/?hl=fr](https://cloud.google.com/vpc-service-controls/?hl=fr)

### SC-22

**Description du contrôle :** Les systèmes d'information qui fournissent collectivement un service de résolution de nom/adresse à une organisation sont tolérants aux pannes et mettent en œuvre une séparation des rôles internes/externes.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Dans le cadre de l'infrastructure de la solution, le composant GCP Cloud DNS est implémenté pour être utilisé par les clients pour leurs charges de travail. Cela inclut la tolérance aux pannes par défaut avec une disponibilité de 100 % annoncée par Google ([https://cloud.google.com/dns?hl=fr](https://cloud.google.com/dns?hl=fr))

Le client configurera la résolution DNS dans le cadre du déploiement de son application et abordera ce contrôle dans le cadre de son évaluation de la sécurité.

#### Définitions des ressources

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf pour la définition de base du réseau, des contrôles de service, des politiques et de la journalisation  
* \- 3-networks-hub-and-spoke/envs/shared/dns-hub.tf \- définition DNS

#### Recommandations de mise en œuvre

Le client est responsable de fournir des systèmes qui fournissent collectivement un service de résolution de nom/adresse pour une organisation, sont tolérants aux pannes et mettent en œuvre une séparation des rôles interne/externe.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud DNS – Service DNS (Domain Name System) faisant autorité, évolutif, fiable, résilient et géré. Publiez et gérez facilement des millions de zones et d'enregistrements DNS.  
[https://cloud.google.com/dns/?hl=fr](https://cloud.google.com/dns/?hl=fr)

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr)

### SC-23

**Description du contrôle :** Le système d'information protège l'authenticité des sessions de communication.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Toutes les communications vers les ressources Google se font via TLS 1.2 ou supérieur (https est spécifié pour toutes les chaînes de connexion et les consoles Google redirigent toutes automatiquement http vers https), garantissant la confidentialité et l'intégrité des informations en transit. L'accès aux postes de travail gérés par l'organisation est obligatoire et ils sont configurés avec des versions de navigateur et des chiffrements à jour.

Toutes les communications avec Azure DevOps (dépôt) et Entra ID se font via TLS 1.2 ou supérieur.

TLS 1.2+ fournit l'authenticité nécessaire des sessions de communication (au moyen d'une authentification par certificat), y compris la protection contre les attaques de type man-in-the-middle, le détournement, etc.

#### Recommandations de mise en œuvre

Les clients sont responsables de la configuration des navigateurs Web pour utiliser un protocole de cryptage qui satisfait ou dépasse les exigences de l'Agence. Les clients sont informés que la norme USGCB (United States Government Configuration Baseline) restreint le lancement de la prise de contact TLS côté client du bureau fédéral aux algorithmes approuvés par FIPS.

Considérations relatives à l'espace de travail :  
Les agences clientes sont responsables de la configuration de leurs navigateurs et connexions côté client sur les postes de travail, serveurs et appareils mobiles applicables pour activer les connexions utilisant le cryptage. Les clients doivent appliquer les paramètres USGCB sur les postes de travail fournis par le gouvernement pour établir des connexions avec des chiffrements approuvés par FIPS.

Google utilise un système ALTS (Application Layer Transport Security) personnalisé ([https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security?hl=fr](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security?hl=fr)) protocole d'authentification et de cryptage. ALTS effectue l'authentification principalement par identité plutôt que par hôte, et est similaire au TLS mutuellement authentifié. ALTS n'autorise pas la reprise de session/les poignées de main à temps d'aller-retour nul (0-RTT), s'appuie sur un protocole de prise de contact et un protocole d'enregistrement. ALTS est résistant à la relecture.  
Bonne pratique : mettez en œuvre une interconnexion dédiée pour isoler les données et le trafic de votre organisation de l'Internet public ([https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr](https://cloud.google.com/interconnect/docs/concepts/overview?hl=fr))  
Bonne pratique : configurer Cloud VPN pour protéger davantage les informations en transit ([https://cloud.google.com/vpn/docs/concepts/overview?hl=fr](https://cloud.google.com/vpn/docs/concepts/overview?hl=fr))  
Bonne pratique : exploiter Cloud KMS pour chiffrer les données avec des clés de chiffrement symétriques et asymétriques ([https://cloud.google.com/kms/docs/encrypt-decrypt?hl=fr](https://cloud.google.com/kms/docs/encrypt-decrypt?hl=fr))

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Security : livre blanc couvrant la sécurité des services cloud de Google, y compris la culture de sécurité de Google, la sécurité opérationnelle, la sécurité de la technologie et des centres de données, les contrôles environnementaux des centres de données, la sécurité et la conformité des données.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Sécurité de l'infrastructure de Google : livre blanc qui donne un aperçu de la sécurité de l'infrastructure de Google pour le matériel, les services, l'identité des utilisateurs, le stockage, les communications et les opérations. Remarque : Ce n'est pas un produit GCP  
https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf?utm\_medium=et\&utm\_source=google.com%2Fcloud\&utm\_campaign=multilayered\_security\&utm\_content=download\_the\_whitepaper 

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

### SC-28

**Description du contrôle :** Le système d’information protège la confidentialité et l’intégrité des informations au repos définies par l’organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

GCP intègre des clés de sécurité gérées par Google avec rotation par défaut pour le cryptage du stockage. Des solutions de clés de sécurité fournies et gérées par le client sont également disponibles.

Ressources:   
\- 2-environments/modules/env\_baseline/kms.tf \- projet de gestion de clés séparé

#### Recommandations de mise en œuvre

Les agences doivent évaluer leurs pratiques de stockage d'informations et prendre des mesures pour protéger les informations de l'agence. Les informations stockées dans Google Workspace doivent être limitées à la norme FIPS 199 High ou inférieure. Les agences doivent évaluer et mettre en œuvre des mécanismes cryptographiques appropriés pour toutes les données extraites du service Google Workspace, telles que les journaux d'audit ou d'autres données nécessaires aux rapports. Il n'existe aucune condition préalable pour que les services externes soient autorisés par FedRAMP pour être inclus dans le produit Cloud Identity et les limites de Google Workspace ne s'étendent pas à ces services tiers. Par conséquent, les agences doivent faire preuve de diligence raisonnable en autorisant ces services avant d'établir une authentification tierce via Cloud Identity. Tous les services externes qu'une agence choisit de gérer avec Cloud Identity sortent du champ d'application du système Google Workspace et doivent être sécurisés conformément aux exigences de l'agence.

Pour plus d'informations sur la configuration des relations de provisionnement automatique Cloud Identity, veuillez consulter les articles suivants :

Configurez le SSO avec Google comme fournisseur d'identité : https://support.google.com/cloudidentity/topic/7558768?hl=en\&ref\_topic=7558174

Provisionnement et déprovisionnement automatisés des utilisateurs : [https://support.google.com/cloudidentity/topic/7661972?hl=fr](https://support.google.com/cloudidentity/topic/7661972?hl=fr)

Configurez votre propre application SAML client : [https://support.google.com/cloudidentity/answer/6087519?hl=fr\&ref\_topic=7558947](https://support.google.com/cloudidentity/answer/6087519?hl=fr&ref_topic=7558947)

Les discussions officieuses ne sont pas conservées, le cryptage au repos n'est donc pas applicable. Veuillez consulter [https://support.google.com/chat/answer/29291?hl=fr](https://support.google.com/chat/answer/29291?hl=fr) pour plus d'informations sur les discussions en mode privé dans Hangouts.

Google permet aux clients des agences d'héberger des sites Google des deux manières suivantes :

Sites Google hébergés à partir de domaines personnalisés (veuillez consulter [https://support.google.com/sites/answer/99448?hl=fr](https://support.google.com/sites/answer/99448?hl=fr) pour plus d'informations sur les domaines personnalisés) ; ou,  
Sites Google hébergés à partir d'un domaine Google, tel que sites.google.com ou sites.google.com/site/.  
Les sites Google des clients de l'agence doivent être hébergés sur un domaine Google pour recevoir la mise en œuvre de l'intégrité de la transmission TLS décrite dans le contrôle de l'intégrité de la transmission SSP SC-8 des applications. Les clients d'agence ne doivent pas prendre en compte le protocole SSL de Google Sites lors de la transmission vers et depuis des utilisateurs individuels et le service Google Sites doit être mis en œuvre lorsqu'un client d'agence héberge Google Sites à partir d'un domaine personnalisé.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Security : livre blanc couvrant la sécurité des services cloud de Google, y compris la culture de sécurité de Google, la sécurité opérationnelle, la sécurité de la technologie et des centres de données, les contrôles environnementaux des centres de données, la sécurité et la conformité des données.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Sécurité de l'infrastructure de Google : livre blanc qui donne un aperçu de la sécurité de l'infrastructure de Google pour le matériel, les services, l'identité des utilisateurs, le stockage, les communications et les opérations. Remarque : Ce n'est pas un produit GCP  
[https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf](https://cloud.google.com/security/infrastructure/design/resources/google_infrastructure_whitepaper_fa.pdf) 

Google Cloud Storage – Stockage d'objets avec mise en cache globale en périphérie. Options de stockage d'archives multirégionales, régionales, Nearline \- accès basse fréquence et Coldline \-.   
[https://cloud.google.com/storage/?hl=fr](https://cloud.google.com/storage/?hl=fr)

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr)

VM protégées : la VM protégée offre une intégrité vérifiable de vos instances de VM Compute Engine. Vous pouvez donc être sûr que vos instances n'ont pas été compromises par des logiciels malveillants ou des rootkits au niveau du démarrage ou du noyau. L'intégrité vérifiable de la VM protégée est obtenue grâce à l'utilisation du démarrage sécurisé, du démarrage mesuré compatible avec le module de plateforme virtuelle de confiance (vTPM) et de la surveillance de l'intégrité.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr](https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr)

### SC-28 (1)

**Description du contrôle :** Le système d'information met en œuvre des mécanismes cryptographiques pour empêcher la divulgation et la modification non autorisées d'informations définies par l'organisation sur des composants de système d'information définis par l'organisation.

Conseils supplémentaires : Cette amélioration du contrôle s'applique aux concentrations importantes de médias numériques dans les zones organisationnelles désignées pour le stockage des médias ainsi qu'à des quantités limitées de médias généralement associés aux composants du système d'information dans les environnements opérationnels (par exemple, les périphériques de stockage portables, les appareils mobiles). Les organisations ont la possibilité de chiffrer toutes les informations sur les périphériques de stockage (c'est-à-dire le chiffrement complet du disque) ou de chiffrer des structures de données spécifiques (par exemple des fichiers, des enregistrements ou des champs). Les organisations employant des mécanismes cryptographiques pour protéger les informations au repos envisagent également des solutions de gestion des clés cryptographiques.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La solution est déployée sous forme de configurations d'infrastructure au sein de GCP. L'intégrité de l'équipement, du réseau et des services GCP utilisés dans la solution relève de la responsabilité de Google. L'évaluation de ses capacités à assurer ce contrôle a déjà été examinée par le CCCS dans le cadre de l'approbation délivrée pour héberger la charge de travail PB, et est héritée ici pour aborder partiellement ce contrôle. 

La solution est déployée à l’aide d’une infrastructure en tant que code et déployée à partir d’un référentiel Azure DevOps et d’une plateforme CI/CD.  L’intégrité d’Azure DevOps a été évaluée précédemment.   
   
Le client configurera des mécanismes pour empêcher les divulgations non autorisées, les notifications, etc. dans le cadre du déploiement de son application, et abordera ce contrôle dans le cadre de son évaluation de sécurité.

#### Recommandations de mise en œuvre

Il n'existe aucune condition préalable pour que les services externes soient autorisés par FedRAMP pour être inclus dans le produit Cloud Identity et les limites de Google Workspace ne s'étendent pas à ces services tiers. Par conséquent, les agences doivent faire preuve de diligence raisonnable en autorisant ces services avant d'établir une authentification tierce via Cloud Identity. Tous les services externes qu'une agence choisit de gérer avec Cloud Identity sortent du champ d'application du système Google Workspace et doivent être sécurisés conformément aux exigences de l'agence.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Clé de sécurité Titan – Empêchez le piratage de compte, les attaques de phishing et appliquez MFA/2SV à l'aide des clés de sécurité Titan.  
[https://cloud.google.com/titan-security-key/?hl=fr](https://cloud.google.com/titan-security-key/?hl=fr)

Service de gestion des clés cloud : gérez, générez, utilisez, alternez et détruisez les clés cryptographiques AES256, RSA 2048, RSA 3072, RSA 4096, EC P256 et EC P384 sur Google Cloud.  
[https://cloud.google.com/kms/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud HSM : protégez vos clés de chiffrement dans le cloud à l'aide d'un modèle de sécurité matérielle entièrement hébergé et conforme à la norme FIPS 140-2 niveau 3\.  
[https://cloud.google.com/hsm/?hl=fr](https://cloud.google.com/hsm/?hl=fr)

Certificats SSL gérés par Google – Une fonctionnalité d'équilibrage de charge cloud ; Les certificats SSL gérés par Google sont fournis, renouvelés et gérés pour vos noms de domaine.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr](https://cloud.google.com/load-balancing/docs/ssl-certificates?hl=fr)

Certificats SSL gérés par le client : une fonctionnalité d'équilibrage de charge cloud ; Fournissez vos propres certificats SSL pour gérer l'accès sécurisé à vos domaines GCP. Les certificats autogérés peuvent prendre en charge les caractères génériques et plusieurs noms alternatifs de sujet (SAN).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates#working-self-managed)

### SC-39

**Description du contrôle :** Le système d'information maintient un domaine d'exécution distinct pour chaque processus en cours d'exécution.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable du maintien d'un domaine d'exécution distinct pour chaque processus en cours d'exécution.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Resource Manager : gérez hiérarchiquement les ressources par projet, dossier et organisation. Contrôlez de manière centralisée les politiques d’organisation et d’accès ainsi que les inventaires d’actifs. Étiquetez les ressources pour une meilleure gestion.   
[https://cloud.google.com/resource-manager?hl=fr](https://cloud.google.com/resource-manager?hl=fr)

## Intégrité du système et de l'information (SI)

### SI-3 (2)

**Description du contrôle :** Le système d’information met automatiquement à jour les mécanismes de protection contre les codes malveillants.

Conseils supplémentaires : les mécanismes de protection contre les codes malveillants incluent, par exemple, les définitions de signature.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes. 

SCC s'intègre à Cloud Audit Logs pour capturer les enregistrements d'audit des événements liés à la sécurité. Ces journaux peuvent être utilisés à des fins d’analyse et d’enquête.

#### Politiques de l'organisation

* calculate.trustedImageProjects : cette contrainte permet de renforcer l’intégrité des logiciels et des micrologiciels et la gestion de la configuration. Cette autorisation contrôle quels projets peuvent être utilisés comme sources fiables pour les images de VM. En limitant cela à un ensemble sélectionné de projets, vous réduisez le risque de déployer des machines virtuelles à partir de sources non fiables ou potentiellement compromises.

#### Recommandations de mise en œuvre

Pour plus d'informations sur la configuration des relations de provisionnement automatique Cloud Identity, veuillez consulter les articles suivants :

### SI-3 (7)

**Description du contrôle :** Le système d'information met en œuvre des mécanismes de détection de codes malveillants non basés sur des signatures.

Conseils supplémentaires : les mécanismes de détection non basés sur les signatures incluent, par exemple, l'utilisation d'heuristiques pour détecter, analyser et décrire les caractéristiques ou le comportement d'un code malveillant et pour fournir des protections contre un code malveillant pour lequel les signatures n'existent pas encore ou pour lesquelles des signatures existantes peut ne pas être efficace. Cela inclut le code malveillant polymorphe (c'est-à-dire le code qui modifie les signatures lors de sa réplication). Cette amélioration du contrôle n'exclut pas l'utilisation de mécanismes de détection basés sur les signatures.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes. 

SCC peut vous aider à suivre et à gérer les événements de sécurité planifiés tels que les tests d'intrusion et les analyses de vulnérabilité, en garantissant qu'ils sont correctement autorisés et documentés.

#### Politiques de l'organisation

* calculate.trustedImageProjects : cette contrainte permet de renforcer l’intégrité des logiciels et des micrologiciels et la gestion de la configuration. Cette autorisation contrôle quels projets peuvent être utilisés comme sources fiables pour les images de VM. En limitant cela à un ensemble sélectionné de projets, vous réduisez le risque de déployer des machines virtuelles à partir de sources non fiables ou potentiellement compromises.

#### Recommandations de mise en œuvre

Le client est responsable de la mise en œuvre de mécanismes de détection de codes malveillants non basés sur des signatures.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Workspace Phishing & Malware Protection \- Un élément de Google Workspace qui offre une protection avancée contre le phishing et les logiciels malveillants. Placez les e-mails en quarantaine, protégez-vous contre les pièces jointes anormales, protégez les groupes Google contre l'usurpation d'e-mails entrants.  
[https://support.google.com/a/answer/7577854?hl=fr](https://support.google.com/a/answer/7577854?hl=fr)

### SI-4 (2)

**Description du contrôle :** L'organisation utilise des outils automatisés pour prendre en charge l'analyse des événements en temps quasi réel.

Conseils supplémentaires : les outils automatisés incluent, par exemple, des outils de surveillance des événements basés sur l'hôte, le réseau, le transport ou le stockage, ou les technologies de gestion des informations et des événements de sécurité (SIEM) qui fournissent une analyse en temps réel des alertes et/ou des notifications. générés par les systèmes d’information organisationnels.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes.

#### Recommandations de mise en œuvre

Configurez l'authentification unique avec Google comme fournisseur d'identité : [https://support.google.com/cloudidentity/topic/7558768?hl=fr](https://support.google.com/cloudidentity/topic/7558768?hl=fr)

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Centre de sécurité Google Workspace – Informations de sécurité exploitables pour Google Workspace. Tableau de bord de sécurité unifié. Obtenez des informations sur le partage de fichiers externes, une visibilité sur le spam et les logiciels malveillants ciblant les utilisateurs de votre organisation, ainsi que des mesures pour démontrer l'efficacité de votre sécurité dans un tableau de bord unique et complet.  
[https://workspace.google.com/products/admin/security-center/?hl=fr](https://workspace.google.com/products/admin/security-center/?hl=fr)

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### SI-4 (4)

**Description du contrôle :** Le système d'information surveille en permanence le trafic de communications entrant et sortant pour détecter les activités ou conditions inhabituelles ou non autorisées.

Conseils supplémentaires : Les activités ou conditions inhabituelles/non autorisées liées au trafic de communications entrant et sortant du système d'information incluent, par exemple, le trafic interne qui indique la présence de code malveillant dans les systèmes d'information de l'organisation ou se propageant entre les composants du système, l'exportation non autorisée d'informations ou la signalisation. aux systèmes d’information externes. Les preuves de code malveillant sont utilisées pour identifier les systèmes d’information ou les composants du système d’information potentiellement compromis.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes.

#### Recommandations de mise en œuvre

Le CLIENT est responsable de définir ce qui est considéré comme une fonction privilégiée, d'examiner les informations vérifiables fournies par les différentes éditions de Google Workspace et de déterminer si les fonctionnalités de journalisation d'audit disponibles sont suffisantes pour les besoins d'audit spécifiques à l'organisation.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Télémétrie réseau Google Cloud : la télémétrie réseau fournit à la fois des opérations de réseau et de sécurité avec des journaux de flux VPC détaillés et réactifs pour les services réseau Google Cloud Platform. Identifiez les modèles de trafic et d'accès qui peuvent imposer des risques de sécurité ou opérationnels à votre organisation en temps quasi réel. Les journaux du pare-feu VPC permettent aux utilisateurs de consigner l'accès au pare-feu et de refuser les événements avec la même réactivité que les journaux de flux VPC.  
[https://cloud.google.com/network-telemetry/?hl=fr](https://cloud.google.com/network-telemetry/?hl=fr)

### SI-4 (5)

**Description du contrôle :** Le système d'information alerte le personnel ou les rôles définis par l'organisation lorsque des indicateurs de compromission ou de compromission potentielle définis par l'organisation se produisent.

Conseils supplémentaires : les alertes peuvent être générées à partir de diverses sources, y compris, par exemple, des enregistrements d'audit ou des entrées provenant de mécanismes de protection contre les codes malveillants, de mécanismes de détection ou de prévention des intrusions, ou de dispositifs de protection des limites tels que des pare-feu, des passerelles et des routeurs. Les alertes peuvent être transmises, par exemple, par téléphone, par courrier électronique ou par messagerie texte. Le personnel organisationnel figurant sur la liste de notification peut inclure, par exemple, des administrateurs système, des propriétaires de missions/entreprises, des propriétaires de systèmes ou des responsables de la sécurité des systèmes d'information.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes et les compromissions. Les alertes sont configurées pour avertir le personnel opérationnel lorsque des indicateurs d'utilisation inhabituelle, d'attaque possible ou de compromission potentielle ont été identifiés.

#### Recommandations de mise en œuvre

Provisionnement et déprovisionnement automatisés des utilisateurs : [https://support.google.com/cloudidentity/topic/7661972?hl=fr](https://support.google.com/cloudidentity/topic/7661972?hl=fr)

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

Google Cloud Network Telemetry : Google Cloud Network Telemetry fournit à la fois des opérations de réseau et de sécurité avec des journaux de flux VPC détaillés et réactifs pour les services réseau Google Cloud Platform. Identifiez les modèles de trafic et d'accès qui peuvent imposer des risques de sécurité ou opérationnels à votre organisation en temps quasi réel. Les journaux du pare-feu VPC permettent aux utilisateurs de consigner l'accès au pare-feu et de refuser les événements avec la même réactivité que les journaux de flux VPC.  
[https://cloud.google.com/network-telemetry/?hl=fr](https://cloud.google.com/network-telemetry/?hl=fr)

### SI-4 (16)

**Description du contrôle :** L'organisation corrèle les informations provenant des outils de surveillance utilisés dans l'ensemble du système d'information.

Conseils supplémentaires : la corrélation des informations provenant de différents outils de surveillance peut fournir une vue plus complète de l'activité du système d'information. La corrélation des outils de surveillance qui fonctionnent généralement de manière isolée (par exemple, surveillance des hôtes, surveillance du réseau, logiciel antivirus) peut fournir une vue à l'échelle de l'organisation et, ce faisant, peut révéler des modèles d'attaque autrement invisibles.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable du déploiement des outils de corrélation des informations employés dans l'ensemble du système d'information.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud Identity : gérez facilement les identités des utilisateurs, les appareils et les applications à partir d'une seule console. Appliquez SSO, MFA/2SV et la gestion des appareils mobiles.  
[https://cloud.google.com/identity/?hl=fr](https://cloud.google.com/identity/?hl=fr)

Cloud IAM – Gestion fine des identités et des accès pour les ressources GCP. Gérez les autorisations, les rôles, les comptes de service, les membres et les identités, les politiques de l'organisation, etc.  
[https://cloud.google.com/iam/?hl=fr](https://cloud.google.com/iam/?hl=fr) 

Cloud VPC \- Fonctionnalité de mise en réseau gérée pour vos ressources Cloud Platform. Réseau VPC, routeur cloud, VPN cloud, pare-feu, peering VPC, VPC partagé, routes, journaux de flux VPC.  
[https://cloud.google.com/vpc/?hl=fr](https://cloud.google.com/vpc/?hl=fr)

Google Cloud Network Telemetry : Google Cloud Network Telemetry fournit à la fois des opérations de réseau et de sécurité avec des journaux de flux VPC détaillés et réactifs pour les services réseau Google Cloud Platform. Identifiez les modèles de trafic et d'accès qui peuvent imposer des risques de sécurité ou opérationnels à votre organisation en temps quasi réel. Les journaux du pare-feu VPC permettent aux utilisateurs de consigner l'accès au pare-feu et de refuser les événements avec la même réactivité que les journaux de flux VPC.  
[https://cloud.google.com/network-telemetry/](https://cloud.google.com/network-telemetry/)

### SI-4 (23)

**Description du contrôle :** L'organisation met en œuvre des mécanismes de surveillance basés sur l'hôte définis par l'organisation au niveau des composants du système d'information définis par l'organisation.

Conseils supplémentaires : les composants du système d'information où la surveillance basée sur l'hôte peut être mise en œuvre incluent, par exemple, les serveurs, les postes de travail et les appareils mobiles. Les organisations envisagent d'utiliser des mécanismes de surveillance basés sur l'hôte provenant de plusieurs développeurs de produits informatiques.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Configurez votre propre application SAML client : [https://support.google.com/cloudidentity/answer/6087519?hl=fr](https://support.google.com/cloudidentity/answer/6087519?hl=fr)

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### SI-6

**Description du contrôle :** Le système d'information :

 a. Vérifie le bon fonctionnement des fonctions de sécurité définies par l'organisation ;

 b. Effectue cette vérification : les états de transition du système définis par l'organisation, sur commande d'un utilisateur disposant des privilèges appropriés, à inclure au démarrage et/ou au redémarrage du système et au moins une fois par mois ; et

 c. Informe le personnel ou les rôles définis par l'organisation de l'échec des tests de vérification de sécurité \- pour inclure les administrateurs système et le personnel de sécurité ; et

 d. Arrête le système d'information, redémarre le système d'information et exécute des actions alternatives définies par l'organisation lorsque des anomalies sont découvertes \- y compris la notification des administrateurs système et du personnel de sécurité.

**Exigences:** Profil PBMM 1 : Non, Profil 3 : Non

#### Notes de mise en œuvre

Non requis pour PBMM

#### Recommandations de mise en œuvre

Le CLIENT est responsable de toutes les vérifications des fonctionnalités de sécurité de son infrastructure et de ses charges de travail.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Centre de sécurité Google Workspace – Informations de sécurité exploitables pour Google Workspace. Tableau de bord de sécurité unifié. Obtenez des informations sur le partage de fichiers externes, une visibilité sur le spam et les logiciels malveillants ciblant les utilisateurs de votre organisation, ainsi que des mesures pour démontrer l'efficacité de votre sécurité dans un tableau de bord unique et complet.  
[https://workspace.google.com/products/admin/security-center/?hl=fr](https://workspace.google.com/products/admin/security-center/?hl=fr)

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### SI-7 (1)

**Description du contrôle :** Le système d'information effectue une vérification de l'intégrité des logiciels, micrologiciels et informations définis par l'organisation au démarrage et/ou lors d'événements pertinents pour la sécurité définis par l'organisation, au moins une fois par mois.

Conseils supplémentaires : les événements liés à la sécurité incluent, par exemple, l'identification d'une nouvelle menace à laquelle les systèmes d'information de l'organisation sont sensibles et l'installation de nouveaux matériels, logiciels ou micrologiciels. Les états de transition incluent, par exemple, le démarrage, le redémarrage, l'arrêt et l'abandon du système.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

Security Command Center est configuré pour assurer la surveillance et dispose de renseignements sur les menaces pour détecter les activités malveillantes. 

La solution est déployée sous forme de configurations d'infrastructure au sein de GCP. L'intégrité de l'équipement, du réseau et des services GCP utilisés dans la solution relève de la responsabilité de Google. L'évaluation de ses capacités à assurer ce contrôle a déjà été examinée par le CCCS dans le cadre de l'approbation délivrée pour héberger la charge de travail PB, et est héritée ici pour aborder partiellement ce contrôle. 

La solution est déployée à l'aide d'une infrastructure en tant que code et déployée à partir d'un référentiel distinct et d'une plateforme CI/CD.

#### Recommandations de mise en œuvre

Le CLIENT et les charges de travail prises en charge sont responsables d'effectuer une vérification de l'intégrité des logiciels, micrologiciels et informations définis par l'organisation au démarrage et/ou lors d'événements liés à la sécurité définis par l'organisation, au moins une fois par mois.

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

VM protégées : la VM protégée offre une intégrité vérifiable de vos instances de VM Compute Engine. Vous pouvez donc être sûr que vos instances n'ont pas été compromises par des logiciels malveillants ou des rootkits au niveau du démarrage ou du noyau. L'intégrité vérifiable de la VM protégée est obtenue grâce à l'utilisation du démarrage sécurisé, du démarrage mesuré compatible avec le module de plateforme virtuelle de confiance (vTPM) et de la surveillance de l'intégrité.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr](https://cloud.google.com/security/shielded-cloud/shielded-vm?hl=fr)

Cloud Security Scanner : analyse automatiquement les applications App Engine, Compute Engine et Kubernetes Engine à la recherche de vulnérabilités courantes telles que XXS, l'injection Flash, le contenu HTTP(S) mixte, les bibliothèques obsolètes et non sécurisées.  
[https://cloud.google.com/security-scanner/?hl=fr](https://cloud.google.com/security-scanner/?hl=fr)

Artifact Analysis \- Artifact Analysis est une famille de services qui fournissent l'analyse de la composition des logiciels, le stockage et la récupération des métadonnées. Ses points de détection sont intégrés à un certain nombre de produits Google Cloud tels que Artifact Registry et Google Kubernetes Engine (GKE) pour une activation rapide. Le service fonctionne à la fois avec les produits propriétaires de Google Cloud et vous permet également de stocker des informations provenant de sources tierces. Les services d'analyse exploitent un magasin de vulnérabilités commun pour faire correspondre les fichiers aux vulnérabilités connues.  
[https://cloud.google.com/artifact-analysis/docs/artifact-analysis?hl=fr](https://cloud.google.com/artifact-analysis/docs/artifact-analysis?hl=fr)

### SI-10

**Description du contrôle :** Le système d'information vérifie la validité des entrées d'informations définies par l'organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

L'infrastructure de la solution comporte les points d'entrée suivants :  
\* Uis administratifs : ils sont développés et maintenus par Google, qui est responsable de la validation des entrées.  
\* Infrastructure as Code \- Tous les fichiers de configuration validés par plusieurs examinateurs (y compris l'examen de toute entrée anormale) avant d'être acceptés dans le référentiel. Linting est également configuré sur le dépôt pour garantir l'exactitude syntaxique.

Les charges de travail client qui n'ont pas encore été déployées peuvent contenir du code qui accepte les entrées de l'utilisateur ; le client serait responsable de répondre à ce contrôle dans le cadre de ses activités d'évaluation.

#### Recommandations de mise en œuvre

Le CLIENT et les charges de travail de support sont responsables de la mise en œuvre des contrôles du système pour vérifier la validité des entrées d'informations définies par l'organisation.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Cloud Security Scanner : analyse automatiquement les applications App Engine, Compute Engine et Kubernetes Engine à la recherche de vulnérabilités courantes telles que XXS, l'injection Flash, le contenu HTTP(S) mixte, les bibliothèques obsolètes et non sécurisées.  
[https://cloud.google.com/security-scanner/?hl=fr](https://cloud.google.com/security-scanner/?hl=fr)

Artifact Analysis \- Artifact Analysis est une famille de services qui fournissent l'analyse de la composition des logiciels, le stockage et la récupération des métadonnées. Ses points de détection sont intégrés à un certain nombre de produits Google Cloud tels que Artifact Registry et Google Kubernetes Engine (GKE) pour une activation rapide. Le service fonctionne à la fois avec les produits propriétaires de Google Cloud et vous permet également de stocker des informations provenant de sources tierces. Les services d'analyse exploitent un magasin de vulnérabilités commun pour faire correspondre les fichiers aux vulnérabilités connues.  
[https://cloud.google.com/artifact-analysis/docs/artifact-analysis?hl=fr](https://cloud.google.com/artifact-analysis/docs/artifact-analysis?hl=fr)

### SI-11 \- INTÉGRITÉ DU SYSTÈME ET DE L'INFORMATION

**Description du contrôle :** Le système d'information :

 un. Génère des messages d'erreur qui fournissent les informations nécessaires aux actions correctives sans révéler d'informations qui pourraient être exploitées par des adversaires ; et

 b. Révèle les messages d’erreur uniquement au personnel ou aux rôles définis par l’organisation.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

L'infrastructure de la solution s'appuie sur les messages d'erreur générés par GCP et les services associés ; il n'est pas possible de remplacer/modifier/supprimer des messages d'erreur. L'évaluation du niveau d'information contenue a déjà été examinée par le CCCS dans le cadre de l'approbation délivrée pour héberger la charge de travail PB, et est héritée ici pour aborder en partie ce contrôle. 

Seuls les utilisateurs privilégiés ont accès aux interfaces d'administration et sont exposés à ces messages d'erreur. De la même manière, les erreurs incluses dans les journaux sont limitées aux seuls privilèges utilisés via le contrôle d'accès sur les compartiments de journalisation (hérités du projet de journalisation).

Les charges de travail client qui n'ont pas encore été déployées peuvent générer des messages d'erreur spécifiques à l'application. Le client serait responsable de répondre à ce contrôle dans le cadre de ses activités d'évaluation.

#### Recommandations de mise en œuvre

Partie A :  
Les clients sont responsables de s'assurer que les applications construites sur GCP génèrent des messages d'erreur qui fournissent les informations nécessaires aux actions correctives sans révéler d'informations potentielles pouvant être utilisées à mauvais escient par des adversaires. Les clients peuvent utiliser le produit Cloud Error Reporting situé dans Operations Tools pour identifier et signaler les erreurs. Cloud Error Reporting est une interface centralisée de gestion des erreurs qui affiche les résultats avec des fonctionnalités de tri et de filtrage. Les clients peuvent utiliser la vue dédiée pour afficher les détails des erreurs tels que les graphiques temporels, les occurrences, le nombre d'utilisateurs concernés, les dates de première et de dernière visite et une trace de pile d'exceptions nettoyée.

Partie B :  
Les clients sont responsables de s'assurer que les applications construites sur GCP génèrent des messages d'erreur qui fournissent les informations nécessaires aux actions correctives sans révéler d'informations potentielles pouvant être utilisées à mauvais escient par des adversaires. Les clients peuvent utiliser le produit Cloud Error Reporting situé dans les outils de gestion pour identifier et signaler les erreurs. Cloud Error Reporting est une interface centralisée de gestion des erreurs qui affiche les résultats avec des fonctionnalités de tri et de filtrage. Les clients peuvent utiliser la vue dédiée pour afficher les détails des erreurs tels que les graphiques temporels, les occurrences, le nombre d'utilisateurs concernés, les dates de première et de dernière visite et une trace de pile d'exceptions nettoyée.

Google Cloud utilise un petit ensemble d'erreurs standards avec un grand nombre de ressources pour communiquer les problèmes. L'espace d'état plus petit réduit la complexité de la documentation, permet de meilleurs mappages idiomatiques dans les bibliothèques clientes et réduit la complexité logique du client sans restreindre l'inclusion d'informations exploitables. Les API Google doivent utiliser les codes d'erreur canoniques définis par google.rpc.Code. Ces messages d'erreur aident les utilisateurs à comprendre et à résoudre l'erreur API facilement et rapidement ([https://cloud.google.com/apis/design/errors?hl=fr](https://cloud.google.com/apis/design/errors?hl=fr)).  
Notez que ces erreurs ne sont révélées qu'au personnel privilégié ayant accès aux API Google.   
Bonne pratique : encouragez les développeurs de serveurs à développer des erreurs conformes à google.rpc.Code ([https://cloud.google.com/apis/design/errors\#generating\_errors?hl=fr](https://cloud.google.com/apis/design/errors#generating_errors?hl=fr))

#### Remarques sur les services

Les politiques, procédures et configurations pour ce contrôle doivent être déterminées par l'organisation interne, les équipes de sécurité et d'administration du client. Toutefois, ces outils et services Google Cloud peuvent être utiles.

Cloud Operations Suite : suite d'observabilité intégrée de Google conçue pour surveiller, dépanner et améliorer les performances de l'infrastructure, des logiciels et des applications cloud. Les composants compatibles FedRAMP de Cloud Operations Suite incluent : la journalisation, le rapport d'erreurs, le débogueur, le profileur et la trace.  
[https://cloud.google.com/products/operations/?hl=fr](https://cloud.google.com/products/operations/?hl=fr)

### SI-16

**Description du contrôle :** Le système d'information met en œuvre des mesures de sécurité définies par l'organisation pour protéger sa mémoire contre l'exécution de code non autorisée.

**Exigences:** Profil PBMM 1 : Oui, Profil 3 : Oui

#### Notes de mise en œuvre

La solution est déployée sous forme de configurations d'infrastructure au sein de GCP à l'aide de ses services. L'intégrité des protections de mémoire visant à empêcher l'exécution de code non autorisée relève de la responsabilité de Google. L'évaluation de ses capacités à assurer ce contrôle a déjà été examinée par le CCCS dans le cadre de l'approbation délivrée pour héberger la charge de travail PB, et est héritée ici pour aborder partiellement ce contrôle. 

Les charges de travail client qui doivent encore être déployées peuvent impliquer des composants développés par le client pour lesquels une protection de la mémoire est nécessaire. Le client serait responsable de répondre à ce contrôle dans le cadre de ses activités d'évaluation.

#### Recommandations de mise en œuvre

Le CLIENT est responsable de la configuration et du déploiement des mesures de sécurité définies par l'organisation pour protéger sa mémoire contre l'exécution de code non autorisée au sein de ses charges de travail GCP.

#### Remarques sur les services

Les clients et les organisations peuvent exploiter ou référencer les outils suivants pour répondre à cette exigence pour leur(s) système(s) informatique(s) sur Google Cloud.

Google Cloud Security : livre blanc couvrant la sécurité des services cloud de Google, y compris la culture de sécurité de Google, la sécurité opérationnelle, la sécurité de la technologie et des centres de données, les contrôles environnementaux des centres de données, la sécurité et la conformité des données.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Sécurité de l'infrastructure de Google : livre blanc qui donne un aperçu de la sécurité de l'infrastructure de Google pour le matériel, les services, l'identité des utilisateurs, le stockage, les communications et les opérations. Remarque : Ce n'est pas un produit GCP  
[https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf](https://cloud.google.com/security/infrastructure/design/resources/google_infrastructure_whitepaper_fa.pdf)

Cloud Memorystore : service de stockage de données en mémoire entièrement géré pour Redis, basé sur une infrastructure évolutive, sécurisée et hautement disponible. Utilisez Cloud Memorystore pour créer des caches d'applications qui fournissent un accès aux données en moins d'une milliseconde. Les instances Cloud Memorystore sont isolées et protégées d'Internet à l'aide d'adresses IP privées et sont davantage sécurisées à l'aide du contrôle d'accès basé sur les rôles IAM.  
[https://cloud.google.com/memorystore/?hl=fr](https://cloud.google.com/memorystore/?hl=fr)

# Annexe 3 : Documents de référence <a name="annexe-3"></a>

* [Plan de base de l'entreprise \- Documentation](https://cloud.google.com/architecture/security-foundations?hl=fr)  
* [Vérifications GC Cloud Guardrails pour Google Cloud Platform](https://github.com/canada-ca/cloud-guardrails-gcp)  
* [Organisation Google Workspace et GCP](https://cloud.google.com/resource-manager/docs/creating-managing-organization?hl=fr)  
* [Hiérarchie des ressources, Google Cloud Platform](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=fr)  
* [Hiérarchie IAM, Google Cloud Platform](https://cloud.google.com/iam/docs/resource-hierarchy-access-control?hl=fr)  
* [Meilleures pratiques pour les organisations d'entreprise](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations?hl=fr)  
* [Membres d'authentification GCP acceptés](https://cloud.google.com/iam/docs/overview?hl=fr#google_account)  
* [Rôles IAM GCP](https://cloud.google.com/iam/docs/understanding-roles?hl=fr)  
* [Accès privé à Google](https://cloud.google.com/vpc/docs/configure-private-google-access?hl=fr)  
* [Routage dynamique dans VPC](https://cloud.google.com/vpc/docs/vpc?hl=fr#routing_for_hybrid_networks)  
* [Accès aux API Google](https://cloud.google.com/vpc/docs/configure-private-google-access?hl=fr#config-routing)  
* [Règles de pare-feu VPC](https://cloud.google.com/vpc/docs/firewalls?hl=fr)  
* [Proxy prenant en compte l'identité](https://cloud.google.com/iap/docs/concepts-overview?hl=fr)  
* [Président de la Sécurité](https://forsetisecurity.org/)  
* [Garde-fous GCP Cloud](https://github.com/canada-ca/cloud-guardrails-gcp)  
* [Centre de commandement de sécurité](https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview?hl=fr)  
* [Contrôle des services VPC](https://cloud.google.com/vpc-service-controls/docs/overview?hl=fr)  
* [Gestionnaire de secrets](https://cloud.google.com/secret-manager/docs/overview?hl=fr)  
* [Secrets Manager \- Clés de chiffrement gérées par le client](https://cloud.google.com/secret-manager/docs/cmek?hl=fr)  
* [Journalisation dans le cloud](https://cloud.google.com/logging/docs?hl=fr)  
* [Surveillance du cloud](https://cloud.google.com/monitoring/docs/monitoring-overview?hl=fr)  
* [Présentation du DNS](https://cloud.google.com/dns/docs/overview?hl=fr)


[image1]: ./images/efb-key-decisions.svg

[image2]: ./images/architecture-with-appliance.svg

[image3]: ./images/example-org-structure.svg

[image4]: ./images/example-identity-structure.svg

[image5]: ./images/traffic-flow-appliance.svg

[image6]: ./images/example-hub-spoke.svg

[image7]: ./images/example-dns-setup.svg

[image8]: ./images/example-logging-structure.svg

[image9]: ./images/example-deployment-branching.svg


