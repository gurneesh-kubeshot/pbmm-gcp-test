# Documentation du pipeline ADO

In English: [ADO Pipeline Documentation](./ado-pipeline-documentation.md)

## Zone d'accueil PBMM (Protégé B, Intégrité moyenne/Disponibilité moyenne)

#### Contenu

* [Aperçu](#aperçu)
* [Architecture](#architecture)
* [Organigramme de déploiement du pipeline ADO](#organigramme-de-déploiement-du-pipeline-ado)
  * [Décisions de conception d’infrastructure](#décisions-de-conception-d’infrastructure)
* [Préparation au déploiement](#préparation-au-déploiement)
  * [Clonage du référentiel Azure](#clonage-du-référentiel-azure)
  * [Créer un projet GCP](#créer-un-projet-gcp)
  * [Groupes](#groupes)
  * [Conditions préalables IAM du compte de service](#conditions-préalables-iam-du-compte-de-service)
  * [Bibliothèque Azure](#bibliothèque-azure)
* [Les scripts Yaml et d'automatisation du pipeline Azure](#les-scripts-yaml-et-d'automatisation-du-pipeline-azure)
  * [0-Bootstrap Yaml et exécution de scripts](#0-bootstrap-yaml-et-exécution-de-scripts)
  * [Yaml 1-Org et exécution de scripts](#yaml-1-org-et-exécution-de-scripts)
  * [2-Environnements Yaml et exécution de scripts](#2-environnements-yaml-et-exécution-de-scripts)
  * [Yaml et exécution de scripts à 3 réseaux hub-and-spoke](#yaml-et-exécution-de-scripts-à-3-réseaux-hub-and-spoke)
  * [4-projets Yaml et exécution de scripts](#4-projets-yaml-et-exécution-de-scripts)
  * [6-org-policies Yaml et exécution de scripts](#6-org-policies-yaml-et-exécution-de-scripts)
  * [7-fortifier Yaml et l'exécution de scripts](#7-fortifier-yaml-et-l'exécution-de-scripts)
  * [Détection d'erreurs dans les scripts Bash](#erreur-détection-dans-les-scripts-bash)
  * [Fichiers README de référence](#fichiers-readme-de-référence)
* [Étapes d’exécution du pipeline ADO](#étapes-d’exécution-du-pipeline-ado)
  * [Temps d’exécution du pipeline ADO](#temps-d’exécution-du-pipeline-ado)
  * [Résultat : Structure des dossiers GCP](#résultat)
  * [Étapes pour réexécuter les tâches ayant échoué](#étapes-pour-réexécuter-les-tâches-ayant-échoué)
  * [Réexécutez le nouveau pipeline en cas d'erreurs intermittentes](#réexécutez-le-nouveau-pipeline-en-cas-d'erreurs-intermittentes)



# Aperçu <a name="aperçu"></a>

Ce processus déploiera une zone d'atterrissage comme indiqué dans le document de conception technique pour la zone d'atterrissage du Canada PBMM.  La Landing Zone est une zone d'atterrissage Google Cloud hébergée sur GitHub, basée sur Terraform et conforme à PBMM.  N'importe quel ministère ou organisme du GC peut cloner dans son propre référentiel, définir des variables et déployer.  La méthodologie suivante guidera les utilisateurs tout au long du processus de bout en bout.

La documentation décrit de manière exhaustive l’option de déploiement basée sur le pipeline Azure DevOps, depuis sa base architecturale jusqu’à l’exécution et le dépannage. Il approfondit la structure, la configuration et la séquence des étapes impliquées dans le provisionnement des ressources. Les composants clés tels que la bibliothèque Azure et les scripts d'automatisation sont expliqués, ainsi que des détails sur la gestion des erreurs et les mesures de performances. Le document vise à guider les utilisateurs à travers la configuration, l'exécution et les problèmes intermittents du pipeline.

# Architecture <a name="architecture"></a>

![][image1]

Pour un schéma architectural complet, veuillez consulter la ressource PDF suivante :  
[Aperçu architectural PDF](https://drive.google.com/file/d/1xRK9DDHIgynEz2fM-2fs9Kkbj9Z-gmzf/view)

# 

# Organigramme de déploiement du pipeline ADO <a name="organigramme-de-déploiement-du-pipeline-ado"></a>

L'organigramme suivant décrit les ressources à déployer dans chacune des différentes étapes.  
![][image2]

## Décisions de conception d’infrastructure <a name="décisions-de-conception-d’infrastructure"></a>

Certaines décisions doivent être prises dès le début du projet et mises en configuration.

1. Charge de travail   
   1. Des modifications peuvent être apportées aux dossiers aux étapes 4 et 5 qui seront reflétées dans les noms des projets créés.   
   2. Les ressources de l'étape 5 sont un ensemble de machines virtuelles à titre d'exemple.  Les définitions de ressources doivent être modifiées pour correspondre à votre charge de travail réelle.   
   3. Veuillez vous référer au TDD pour plus d’informations et plus de ressources.  
2. Configuration du VPC   
   1. Le vpc\_config.yaml est le point consolidé pour la configuration. 

# Préparation au déploiement <a name="préparation-au-déploiement"></a>

Voici les conditions préalables requises pour le déploiement du pipeline Ado

## Clonage du référentiel Azure <a name="clonage-du-référentiel-azure"></a>

Il existe deux façons de cloner le référentiel Azure.

1\. Copiez le HTTPS URL et utilisez la commande git clone dans votre Terminal.

```bash
git clone <repo_url> 
git checkout <branch>
```

2\. Cliquez sur le bouton « Cloner dans VS Code ». Sélectionnez le dossier de destination et collez les informations d'identification git générées.

**![][image3]**

## Créer un projet GCP <a name="créer-un-projet-gcp"></a>

Service suivant à créer dans le projet gcp

* Le compte de service (super administrateur)  
* Et la clé JSON du compte de service utilisé pour l'authentification gcp d'ADO vers l'environnement GCP.   
* API à activer dans le projet de configuration gcp.

```
accesscontextmanager.googleapis.com
analyticshub.googleapis.com
artifactregistry.googleapis.com
bigquery.googleapis.com
bigqueryconnection.googleapis.com
bigquerydatapolicy.googleapis.com
bigquerymigration.googleapis.com
bigqueryreservation.googleapis.com
bigquerystorage.googleapis.com
billingbudgets.googleapis.com
cloudapis.googleapis.com
cloudasset.googleapis.com
cloudbilling.googleapis.com
cloudbuild.googleapis.com
cloudfunctions.googleapis.com
cloudkms.googleapis.com
cloudresourcemanager.googleapis.com
cloudtrace.googleapis.com
compute.googleapis.com
containerregistry.googleapis.com
dataform.googleapis.com
dataplex.googleapis.com
datastore.googleapis.com
essentialcontacts.googleapis.com
iam.googleapis.com
iamcredentials.googleapis.com
iap.googleapis.com
logging.googleapis.com
monitoring.googleapis.com
oslogin.googleapis.com
policysimulator.googleapis.com
pubsub.googleapis.com
secretmanager.googleapis.com
securitycenter.googleapis.com
securitycentermanagement.googleapis.com
servicemanagement.googleapis.com
servicenetworking.googleapis.com
serviceusage.googleapis.com
source.googleapis.com
sourcerepo.googleapis.com
sql-component.googleapis.com
storage-api.googleapis.com
storage-component.googleapis.com
storage.googleapis.com

```


## Groupes <a name="groupes"></a>

Voici les groupes à créer au niveau IAM de l’organisation.
```
gcp-organization-admins@example.com
gcp-billing-admins@example.com 
gcp-billing-data@example.com 
gcp-audit-data@example.com 
gcp-monitoring-workspace@example.com
```


## Conditions préalables IAM du compte de service <a name="conditions-préalables-iam-du-compte-de-service"></a>

| Compte de services  | Autorisation IAM  | Niveau  |
| :---- | :---- | :---- |
| E-mail du super-administrateur (Le compte de service d'installation pour exécuter le pipeline ADO) | Accéder à l'éditeur du gestionnaire de contexte | Organisation |
|  | Utilisateur du compte de facturation | Organisation |
|  | Administrateur de calcul | Organisation |
|  | Visionneuse de réseau de calcul | Organisation |
|  | Créer des comptes de service | Organisation |
|  | Créateur de dossier | Organisation |
|  | Visionneuse de dossiers | Organisation |
|  | Administrateur de l'organisation | Organisation |
|  | Administrateur des règles d'organisation | Organisation |
|  | Visionneuse d'organisation | Organisation |
|  | Administrateur de quotas | Organisation |
|  | Éditeur de configurations de notification Security Center | Organisation |
|  | Créateur de jeton de compte de service | Organisation |
|  | Administrateur de l'utilisation des services | Organisation |
|  | Consommateur d'utilisation du service | Organisation |
|  | Administrateur de stockage | Organisation |
|  | Créateur de projet | Organisation |
|  | Propriétaire | Projet |
|  | Créateur de jeton de compte de service | Projet |
|  | Utilisateur du compte de service | Projet |
|  | Administrateur de facturation | Compte de facturation |

## Bibliothèque Azure   <a name="bibliothèque-azure"></a>

### **1\. Groupe de variables** <a name="1.-groupe-de-variables"></a>

La bibliothèque Azure stocke les variables d'environnement utilisées comme entrées pour le pipeline ADO. Ces variables incluent Billing\_ID, Org\_id, région, root\_folder\_id, super\_admin\_email, domaine et utilisateur du périmètre vpc-sc. Ils sont référencés dans le pipeline YAML.

| Nom de la variable  | Description |
| :---- | :---- |
| BILLING\_ID  | L'ID du compte de facturation est une valeur alphanumérique de 18 caractères attribuée à votre compte de facturation GCP Cloud. |
| DOMAINE | Le nom de domaine de l'organisation par exemple : google.com |
| GCP\_SA\_KEY | Le fichier Json du compte de service GCP (super administrateur) qui est utilisé pour la configuration du pipeline ado.  |
| ORG\_ID | L'ID de ressource d'organisation est un identifiant unique pour une ressource d'organisation. |
| UTILISATEUR DU PÉRIMÈTRE  | Il s'agit de l'utilisateur administrateur à ajouter dans le périmètre VPC-SC (niveau d'accès). Au moins un utilisateur à ajouter. |
| RÉGION | C'est à la région de déployer toutes les ressources en son sein. |
| ROOT\_FOLDER\_ID | L'identifiant du dossier gcp parent où toutes les ressources telles que les dossiers et les projets, etc. doivent être déployées. (Il doit déjà être créé) |
| SUPER\_ADMIN\_EMAIL | L'e-mail du compte de service administrateur requis pour la configuration du pipeline Ado. |

![][image4]

### **2\. Fichier sécurisé** <a name="2.-fichier-sécurisé"></a>

Téléchargez le fichier Json du compte de service dans le fichier Azure-\>Bibliothèque-\>Secure. Le fichier sécurisé est en outre utilisé pour l'authentification GCP.

# Les scripts Yaml et d'automatisation du pipeline Azure <a name="les-scripts-yaml-et-d'automatisation-du-pipeline-azure"></a>

Azure Pipeline YAML définit un workflow séquentiel composé de plusieurs étapes. Chaque étape s'appuie sur des fichiers modèles YAML pour exécuter des scripts Bash, qui à leur tour orchestrent les opérations Terraform (initialisation, planification, application). Ces modèles de fichiers YAML intègrent la bibliothèque Azure en tant que groupe de variables pour accéder aux variables d'environnement nécessaires et également installer Terraform et divers outils. De plus, les fichiers YAML gèrent l'installation des outils, la configuration des informations d'identification GCP et exportent les variables d'environnement nécessaires à l'exécution du pipeline.

Chemin Yaml : azure-pipelines  
Chemin des scripts : automation-scripts


```yaml

trigger: none


variables:
 - group: 'GCP_ZA_ADO-baseline-stages'


stages:
 - stage: Setup
   displayName: 'Setup Tools'
   jobs:
     - job: Access_GCP_environment
       displayName: 'Access to GCP'
       pool:
         vmImage: 'ubuntu-latest'
       steps:
         - template: templates/securefile-template.yaml
     - job: InstallTools
       displayName: 'Install Terraform'
       dependsOn: Access_GCP_environment
       pool:
         vmImage: 'ubuntu-latest'
       steps:
         - script: |
             curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
             sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com              $(lsb_release -cs) main"
             sudo apt-get install -y wget unzip
             wget  https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
             unzip terraform_1.6.0_linux_amd64.zip
             sudo mv terraform /usr/local/bin/
             sudo chmod +x /usr/local/bin/terraform
             terraform version
             sudo apt-get update && sudo apt-get install dos2unix
             sudo apt-get update && sudo apt-get install google-cloud-sdk
             sudo apt-get install google-cloud-cli-terraform-tools -y
             sudo apt-get install jq -y
             sudo apt update && sudo apt install python3  
             ls -l
             python3 ./fix_tfvars_symlinks.py .
             find . -type f -name "*.sh" | xargs chmod a+x
             find . -type f -name "*.sh" | xargs dos2unix


           displayName: 'Install Terraform'
           continueOnError: false


 - template: bootstrap_stage/bootstrap.yaml
   parameters:
     stageName: bootstrap_stage
     continueOnError: false
 - template: org_stage/org.yaml
   parameters:
     stageName: org_stage
     continueOnError: false


 - template: environments_stage/environments.yaml
   parameters:
     stageName: environments_stage
     continueOnError: false


 - template: network_hub_spoke_stage/network_hub_spoke.yaml
   parameters:
     stageName: network_hub_spoke_stage
     continueOnError: false


 - template: projects_stage/projects.yaml
   parameters:
     stageName: projects_stage
     continueOnError: false


 - template: orgpolicies_stage/orgpolicies.yaml
   parameters:
     stageName: orgpolicies_stage
     continueOnError: false


 - template: fortigate_stage/fortigate.yaml
   parameters:
     stageName: fortigate_stage
     continueOnError: false

```


## 0-Bootstrap Yaml et exécution de scripts <a name="0-bootstrap-yaml-et-exécution-de-scripts"></a>

Le fichier Bootstrap YAML initialise le pipeline en exportant les variables d'environnement essentielles, en configurant les informations d'identification GCP et en déployant le script d'amorçage. Pour optimiser l'efficacité et éviter les problèmes de liens symboliques, l'artefact d'amorçage est publié à la fin de cette étape et téléchargé dans les étapes suivantes. Cette approche isole chaque étape dans son propre environnement, garantissant une exécution propre et des résultats fiables. Le script d'amorçage exploite Terraform pour provisionner les ressources définies dans le répertoire 0-bootstrap.

| Scène  | Description |
| :---- | :---- |
| 0-bootstrap | Bootstrap est une organisation Google Cloud. Cette étape configure également un pipeline CI/CD pour le code Blueprint dans les étapes suivantes. Le projet CICD contient le pipeline de base Cloud Build pour le déploiement de ressources. Le projet de départ inclut les buckets Cloud Storage qui contiennent l'état Terraform de l'infrastructure de base et inclut les comptes de service hautement privilégiés qui sont utilisés par le pipeline de base pour créer des ressources. L'état Terraform est protégé par le contrôle de version des objets de stockage. Lorsque le pipeline CI/CD s'exécute, il fait office de comptes de service gérés dans le projet initial. |

## Yaml 1-Org et exécution de scripts <a name="yaml-1-org-et-exécution-de-scripts"></a>

Le pipeline de déploiement utilise un fichier Org YAML pour télécharger un artefact 0-Bootstrap. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Après le téléchargement, le pipeline exécute le script shell 1-org. Ce script est responsable du déploiement des ressources définies dans le répertoire 1-org.

Pour garantir la cohérence et éviter les conflits après l'achèvement de chaque script, une archive tar est créée, capturant essentiellement son état. Cette archive est ensuite extraite au début du script suivant. Cette approche garantit l’intégrité des fichiers tout au long du pipeline de déploiement. Enfin, le processus se termine par la publication de l'artefact 1-org.

| Scène  | Description |
| :---- | :---- |
| 1-org | Configure les dossiers partagés de niveau supérieur, les projets pour les services partagés, la journalisation au niveau de l'organisation et les paramètres de sécurité de base via les stratégies d'organisation. |

## 2-Environnements Yaml et exécution de scripts <a name="2-environnements-yaml-et-exécution-de-scripts"></a>

Le pipeline de déploiement utilise un fichier YAML d'environnement pour télécharger un artefact 1-Org. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Après le téléchargement, le pipeline exécute le script shell à 2 environnements. Ce script est responsable du déploiement des ressources définies dans le répertoire 2-environnements. Enfin, le processus se termine par la publication de l'artefact 2-environnements.

| Scène | Description |
| :---- | :---- |
| 2-environnements | Configure les environnements de développement, de non-production et de production au sein de l'organisation Google Cloud que vous avez créée. |

## YAML de configuration VPC

Ce fichier YAML définit la configuration réseau du LZ et est utilisé par la section réseaux dans 3-networks-hub-and-spoke. Il décrit la structure des régions, des rayons (pour les environnements de charge de travail), des ressources communes et des connexions réseau sur site. 

Consultez le document de conception technique pour obtenir des informations relatives à la conception. 

### **Notes d'utilisation**

* Remplissez ce fichier YAML avec vos exigences réseau spécifiques  
* Assurez-vous de comprendre les implications de chaque option de configuration et ajustez-les en fonction de vos besoins en matière de sécurité et de connectivité.

### **Régions**

Une liste de configurations pour chacune des 2 régions prises en charge

* name : (obligatoire) le nom de la région, par ex.  
* activé : (facultatif) par défaut "true" pour la région1 et "false" pour la région2. Définir sur true pour déployer dans une région

### **Rayons de production, de non-production et de développement**

Les sections de rayons contiennent une section de configuration commune pour les « rayons » et des configurations similaires pour chacun des « rayons ». Par défaut, cette section contient 3 environnements « spoke » (développement, non-production et production). Vous pouvez ajouter ou supprimer des rayons si nécessaire. 

Les éléments de configuration sont :

* al\_env\_ip\_range : un CIDR résumé pour les plages d'adresses "en rayons"  
* spoke\_common\_routes : Contient (le cas échéant) le routage commun pour tous les "spokes", par défaut 2 routes facultatives  
  * rt\_nat\_to\_internet : route vers Internet via la passerelle NAT  
  * rt\_windows\_activation : route vers les serveurs d'activation Windows fournis par Google

Ces routes peuvent être complétées ou remplacées par des routes définies au niveau de l'environnement « rayon » ou même inférieures au niveau du sous-environnement (« de base » ou « restreint ») en utilisant une priorité plus élevée.

### **Configuration des rayons**

Pour chacun des environnements « en rayons », il existe une partie de configuration commune et des configurations distinctes pour chacun des sous-environnements (par défaut « de base » et « restreint »).

La différence entre « de base » et « restreint » réside dans le niveau de sécurité. Les sous-environnements « restreints » utilisent des contrôles de service de type périmètre qui sécurisent les charges de travail.

### **Configuration commune**

Les paramètres suivants sont communs aux sous-environnements « de base » et « restreint »

* env\_code : (obligatoire) un code à une lettre pour l'environnement, trouvé dans les noms de ressources. Par défaut, il s'agit de "d" pour développement, "n" pour non-production et "p" pour production.  
* env\_enabled : (facultatif) par défaut false, défini sur true pour provisionner l'environnement « spoke »  
* nat\_igw\_enabled : (facultatif) contrôle le provisionnement de la fonction NAT, par défaut false, définie sur true pour configurer les passerelles NAT. Conditionne également implicitement la fourniture de la route NAT vers Internet et les ressources « cloud router » associées  
* windows\_activation\_enabled : (facultatif) contrôle le provisionnement de la route rt\_windows\_activation. Par défaut faux.  
* Enable\_hub\_and\_spoke\_transitivity : (facultatif) contrôle le déploiement de machines virtuelles dans des VPC partagés pour permettre le routage entre rayons. Par défaut faux.  
* router\_ha\_enabled : (facultatif) contrôle le déploiement de la deuxième ressource « routeur cloud » dans chaque zone de disponibilité. Le « routeur cloud » est gratuit mais pas le trafic BGP qui le traverse. Par défaut faux.  
* mode : (facultatif) 2 valeurs possibles définies "spoke" ou "hub", ceci est utilisé dans le code. Par défaut "parlé" à ce niveau.

### **Paramètres de configuration pour « base » et « restreint »**

La configuration des 2 sous-environnements est la même, les routes et adressages peuvent varier.

Les paramètres suivants sont courants :

* env\_type : (facultatif) Il s'agit d'un composant des noms de ressources. Par défaut "shared-base" pour "base" et "shared-restricted" pour "restricted".  
* activé : (facultatif) Par défaut, false. Si c'est vrai, le sous-environnement est déployé.  
* private\_service\_cidr : (facultatif) Il s'agit d'une plage d'adresses au format CIDR qui, si configurée, permet la fourniture de la connectivité "Private Service Access", nécessaire pour accéder à des services tels que Cloud SQL ou Cloud Filestore (partage de fichiers).  
* private\_service\_connect\_ip : (obligatoire) c'est l'adresse qui sera attribuée à un point de connexion privé, utilisé pour accéder aux services API Google en mode privé.  
* subnets : (obligatoire) la configuration des sous-réseaux. Par défaut, les ensembles de sous-réseaux configurés sont les suivants :  
  * id=primary : (facultatif) utilisé pour les charges de travail, avec des plages d'adresses pour chaque région. Il est facultatif de provisionner un sous-réseau au niveau de la région.  
    * secondaires\_ranges : (facultatif) plusieurs plages d'adresses secondaires peuvent être configurées, là encore facultativement dans une ou les deux régions, associées au sous-réseau principal. Les seuls paramètres fournis (par région) sont  
      * range\_suffix : (obligatoire) une chaîne arbitraire utilisée pour générer les noms des sous-réseaux secondaires  
      * ip\_cidr\_ranges : (obligatoire) la plage d'adresses du sous-réseau secondaire au format CIDR, pour chaque région dans laquelle vous souhaitez provisionner un sous-réseau secondaire.  
    * id : (obligatoire) un identifiant unique pour le sous-réseau, qui apparaît dans le nom généré de la ressource créée. Nous pouvons fournir  
    * description : (facultatif) une description de la fonction du sous-réseau  
    * ip\_ranges : (obligatoire) un espace d'adressage de sous-réseau par région au format CIDR. Pour chaque région pour laquelle une plage CIDR est spécifiée, un sous-réseau distinct sera mis à disposition.  
    * subnet\_suffix : (facultatif) une chaîne qui sera ajoutée à la fin du nom de sous-réseau généré  
    * flow\_logs : (facultatif) paramètres "flow-log" personnalisés par rapport aux valeurs par défaut. Les champs suivants peuvent être spécifiés :  
      * activer : (facultatif) "false" par défaut. Si c'est vrai, les flow\_logs sont activés pour le sous-réseau  
      * intervalle : (facultatif) par défaut 5 secondes  
      * métadonnées : (facultatif) INCLUDE\_ALL\_METADATA par défaut  
      * metadata\_fields (facultatif) vide par défaut  
    * private\_access : (facultatif) false par défaut. Contrôle si Google Private Access (PGA) est activé au niveau du sous-réseau. Comme il s'agit de provisionner une ressource de type "forwarding-rule", l'activation entraîne des coûts.  
  * id=proxy : (facultatif) utilisé pour les ressources qui utilisent le proxy Envoy déployé dans un VPC. Exemples : équilibreur de charge applicatif ou « proxy TCP » interne, API Gateway. Il y a des paramètres  
    * id : (obligatoire) un identifiant unique pour le sous-réseau, qui apparaît dans le nom généré de la ressource créée. Nous pouvons fournir  
    * description : (facultatif) une description de la fonction du sous-réseau  
    * ip\_ranges : (obligatoire) un espace d'adressage de sous-réseau par région au format CIDR. Pour chaque région pour laquelle une plage CIDR est spécifiée, un sous-réseau distinct sera mis à disposition.  
    * subnet\_suffix : (facultatif) une chaîne qui sera ajoutée à la fin du nom de sous-réseau généré  
    * flow\_logs : (facultatif) paramètres "flow-log" personnalisés par rapport aux valeurs par défaut. Les champs suivants peuvent être spécifiés :  
      * activer : (facultatif) "false" par défaut. Si c'est vrai, les flow\_logs sont activés pour le sous-réseau  
      * intervalle : (facultatif) par défaut 5 secondes  
      * métadonnées : (facultatif) INCLUDE\_ALL\_METADATA par défaut  
      * metadata\_fields (facultatif) vide par défaut  
    * le rôle et le but sont requis et spécifiques aux sous-réseaux de type « proxy ». Laissez les valeurs par défaut (role \= ACTIVE et goal \= REGIONAL\_MANAGED\_PROXY)

### **La configuration des ressources partagées (section commune)**

Par défaut l'environnement "commun" contient 2 sous-environnements :

* dns-hub : (obligatoire) héberge les zones DNS partagées avec le "DNS peering" ainsi que pour la résolution DNS entre le cloud et le "on-site"  
* net-hub : (obligatoire) héberge les VPC partagés de type "hub", un par environnement (production, non-production et développement) et sous-environnement (de base et restreint)

Pour le sous-environnement "net-hub", il existe des configurations spécifiques, voir la configuration yaml pour plus de détails.

### **Exemple vpc\_config.yaml**

## Yaml et exécution de scripts à 3 réseaux hub-and-spoke  <a name="yaml-et-exécution-de-scripts-à-3-réseaux-hub-and-spoke"></a>

Le pipeline de déploiement utilise un fichier YAML d'environnement pour télécharger un artefact à 2 environnements. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Après le téléchargement, le pipeline exécute le script shell 3-networks-hub-and-spoke. Ce script est responsable du déploiement des ressources définies dans le répertoire 3-networks-hub-and-spoke. Enfin, le processus se termine par la publication de l'artefact 3-networks-hub-and-spoke.

| Scène | Description |
| :---- | :---- |
| 3 réseaux en étoile | Configure les VPC partagés dans la topologie choisie et les ressources réseau associées. |

## 4-projets Yaml et exécution de scripts <a name="4-projets-yaml-et-exécution-de-scripts"></a>

Le pipeline de déploiement utilise un fichier YAML d'environnement pour télécharger un artefact en étoile à 3 réseaux. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Suite au téléchargement, le pipeline exécute le script shell 4-projects. Ce script est responsable du déploiement des ressources définies dans le répertoire 4-projects. Enfin, le processus se termine par la publication de l'artefact 4-projects.

| Scène | Description |
| :---- | :---- |
| 4-projets | Met en place une structure de dossiers pour les différentes unités commerciales, les projets de service dans chacun des environnements. |

##### 

## Yaml et exécution de scripts 5-app-infra 

Le but de cette étape est de déployer une instance Compute Engine simple dans l'un des projets de l'unité commerciale à l'aide du pipeline infra configuré dans 4-projets.  Ces ressources ne sont pas créées dans le cadre de l’automatisation complète du pipeline de Landing Zone. Le pipeline n'exécute aucune automatisation pour l'étape 5\. 

## 6-org-policies Yaml et exécution de scripts <a name="6-org-policies-yaml-et-exécution-de-scripts"></a>

Le pipeline de déploiement utilise un fichier YAML d'environnement pour télécharger un artefact à 4 projets. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Après le téléchargement, le pipeline exécute le script shell 6-org-policies. Ce script est responsable du déploiement des ressources définies dans le répertoire 6-org-policies. Enfin, le processus se termine par la publication de l’artefact 6-org-politics.

| Scène  | Description |
| :---- | :---- |
| Politiques de 6 organisations | Une fois les politiques mises en œuvre au niveau d'une organisation, les développeurs peuvent utiliser le package « 6-org-policies » pour personnaliser les politiques, qu'elles soient nécessaires ou qu'elles doivent être remplacées au niveau spécifique de l'environnement.  C’est là que de nombreuses politiques spécifiques Protégé B sont mises en place. |

## 7-fortifier Yaml et l'exécution de scripts <a name="7-fortifier-yaml-et-l'exécution-de-scripts"></a>

Le pipeline de déploiement utilise un fichier YAML d'environnement pour télécharger un artefact de stratégies à six organisations. Cet artefact agit comme un conteneur contenant tous les fichiers précédemment exécutés. Après le téléchargement, le pipeline exécute le script shell 7-fortigate. Ce script est responsable du déploiement des ressources définies dans le répertoire 7-fortigate. Enfin, le processus se termine par la publication de l'artefact 7-fortigate.

| Scène | Description |
| :---- | :---- |
| 7-fortifier |   Installe une paire redondante d'appliances de sécurité Fortigate dans prj-net-hub-base, le VPC de transit de la zone d'atterrissage.  |

## Erreur Détection dans les scripts Bash <a name="erreur-détection-dans-les-scripts-bash"></a>

Le jeu de commandes \-xe est utilisé pour la détection des erreurs dans tous les fichiers de script Shell :

\-x (commandes d'impression et leurs arguments)

* Fait écho à chaque commande avant son exécution, ainsi que ses arguments.  
* Aide à comprendre le déroulement du script et à identifier les comportements inattendus.  
* La sortie est préfixée par \+ pour la différencier de la sortie de script standard.

\-e (Quitter en cas d'erreur)

* Provoque la fermeture immédiate du script si une commande renvoie un état de sortie différent de zéro.  
* Aide à détecter les erreurs tôt et à prévenir les comportements inattendus.

Le jeu de commandes \+e est utilisé pour désactiver l'option \-e là où certaines erreurs sont attendues.

* Définition : il demande au shell Bash de poursuivre l'exécution même si une commande échoue avec un statut de sortie différent de zéro.  
* Comportement : Essentiellement, il rétablit le comportement par défaut du shell, où les erreurs sont ignorées.  
* Objectif : Il est utilisé pour permettre l'échec de commandes ou de sections spécifiques d'un script sans entraîner la fin du script dans son intégralité.

## Fichiers README de référence : <a name="fichiers-readme-de-référence"></a>

1. TEF-GCP-LZ-HS/LISEZMOI.md

**Fichiers README pour chaque étape :**

1. /TEF-GCP-LZ-HS/0-bootstrap/LISEZMOI.md  
2. /TEF-GCP-LZ-HS/1-org/LISEZMOI.md  
3. /TEF-GCP-LZ-HS/2-environnements/README.md  
4. /TEF-GCP-LZ-HS/3-réseaux-hub-and-spoke/README.md  
5. /TEF-GCP-LZ-HS/4-projets/README.md  
6. /TEF-GCP-LZ-HS/6-org-policies/readme.md  
7. /TEF-GCP-LZ-HS/7-fortigate/README.md


# Étapes d’exécution du pipeline ADO <a name="étapes-d’exécution-du-pipeline-ado"></a>

Lors du lancement du pipeline ADO, précisez la branche souhaitée selon les critères suivants :

![][image6]


Sélectionnez les étapes à exécuter, de bout en bout exécution de l'ensemble du pipeline, toutes les étapes doivent être sélectionnées et cliquez sur le bouton Exécuter. 

![][image8]


## Temps d’exécution du pipeline ADO : <a name="temps-d’exécution-du-pipeline-ado"></a>

Voici le temps d'exécution approximatif des tâches/étapes du pipeline ADO. La durée totale approximative est d'environ 1 heure 45 minutes.   
![][image10]

## Résultat : Structure des dossiers GCP  <a name="résultat"></a>

Voici un exemple de sortie d’un pipeline ADO exécuté, présentant les différentes ressources organisées dans leurs répertoires correspondants.  
![][image11]

## Étapes pour réexécuter les tâches ayant échoué : <a name="étapes-pour-réexécuter-les-tâches-ayant-échoué"></a>

Voici deux manières d'exécuter/réexécuter les tâches ayant échoué : 

1. **Réexécuter une tâche unique**:Pour réexécuter le travail ayant échoué, cliquez sur « Réexécuter les travaux ayant échoué ».  
2. **Réexécuter les tâches ayant échoué restantes**:Pour réexécuter tous les travaux ayant échoué, cliquez sur « Réexécuter tous les travaux », par exemple, comme dans l'exemple ci-dessous, il réexécutera l'étape réseau suivante, puis les projets, etc. 


## Réexécutez le nouveau pipeline en cas d'erreurs intermittentes <a name="réexécutez-le-nouveau-pipeline-en-cas-d'erreurs-intermittentes"></a>

Le pipeline ADO peut provoquer des erreurs intermittentes, en particulier des problèmes de fournisseur survenant au cours des premières étapes 0-bootstrap ou 1-org. Dans de tels cas, une réexécution complète du pipeline est nécessaire pour garantir l’intégrité des données et éviter des pannes ultérieures. De plus, si une tâche dans le pipeline rencontre une erreur « la ressource existe déjà », cela indique un conflit sous-jacent qui nécessite une nouvelle exécution du pipeline depuis le début pour éviter des résultats inattendus et maintenir la stabilité du déploiement. 


[image1]: ./images/architecture-with-appliance.svg

[image2]: ./images/deployment-flowchart.svg

[image3]: ./images/ado-clone.png

[image4]: ./images/ado-library.png

[image6]: ./images/ado-run.png

[image8]: ./images/ado-run-stages.png

[image10]: ./images/ado-jobs.png

[image11]: ./images/resource-structure.png
