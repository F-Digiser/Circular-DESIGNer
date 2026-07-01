# Circular-DESIGNer

## Overview

Circular-DESIGNer is a prototype desktop and Python-based tool for working with circular-design data. It supports STEP-based assembly processing, material-data handling, and calculation-oriented workflows such as volume and mass calculation.
 
 Catena-X-related functionality is an unvalidated design for possible future integration. The software is intended for research, demonstrations and further development by project partners and technical users. It is not presented as a production-ready or conformant Catena-X integration.

## Quick start

### Run the Windows package

Requirements:
* Operating system: Windows 11
* Other operating systems are not supported by this Windows executable.
* Python: No Python installation is required. The application is packaged with its required Python components.

This release has been built and tested on Windows 11. Compatibility with other Windows versions is not guaranteed unless explicitly stated.

1. Download the package from https://zenodo.org/records/21030411.
2. If it is distributed as a ZIP archive, extract the complete archive before starting it.
3. Start `circular_designer.exe`, e.g. by double-clicking.

No Python installation is required for the packaged application.

The application reads and writes JSON files from the folder app_data. So, the file circular_designer.exe must be run next to the folder app_data, which contains the JSON files. Since the JSON files are also appended to and overwritten, the exe file must be run from a user-writable directory, not from a protected location.

### Run from source
**Tested environment:** Python 3.12 on Windows 11. Other operating systems have not been tested.

Requirements:
* Python 3.12
* A supported operating system (just tested with Windows).
* Git, if cloning the repository

Clone the repository and enter its directory:

git clone https://github.com/F-Digiser/Circular-DESIGNer
cd Circular-DESIGNer

Create and activate a virtual environment.

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-lock.txt
python -m pip check

requirements-lock.txt records the dependency versions used for this release. The project has not been validated on all operating systems or hardware configurations.

Run the application from the repository root:

python tool.py

## Mock mode

Mock mode uses synthetic supplier, material, identifier and Chemical Material Passport-style data. It is intended for local development, demonstrations and basic workflow testing.

Mock mode does not connect to Catena-X, BPDM, BPN Discovery, a Digital Twin Registry, a connector, or a partner-operated service. Outputs generated in mock mode must not be interpreted as validated supplier information, regulatory declarations, production data, or proof of interoperability.

## CAD and mass-calculation limitations

The CAD import functionality is intended to read STEP/XDE assembly and shape information and derive geometric volumes. Where mass is calculated, it is derived from geometric volume and a density value configured in the materials_validation.json file.

CAD import, shape traversal, volume conversion and mass calculations have not been validated against a representative external STEP/XDE test corpus.

## Implementation status and design references

This software is an **unvalidated prototype integration design** for retrieving and transforming material-related data using Catena-X, Asset Administration Shell (AAS), Digital Twin Registry (DTR), BPDM and BPN Discovery concepts.

At the time of this release:

* No member of the development team had been onboarded to a Catena-X dataspace.
* No live connection to a Catena-X connector, Digital Twin Registry, BPDM Pool, BPN Discovery service, or partner endpoint was established.
* No end-to-end interoperability, authentication, policy, access-control, semantic-model, security, performance, or data-quality testing was performed against a real Catena-X environment.
* No claim of Catena-X, Tractus-X, AAS, BPDM, BPN Discovery, DSP, or provider-specific API conformance is made.

### Design references

The source code references externally defined concepts, identifiers and interface patterns as intended design targets for future integration work:

* Catena-X semantic-model identifiers for Secondary Material Content, Chemical Material Passport and Part Type Information;
* AAS shell-descriptor and submodel-access patterns;
* Digital Twin Registry asset-link search;
* BPDM business-partner concepts for legal entities, sites and addresses;
* BPN Discovery concepts;
* Tractus-X SDK-based connector and dataspace access patterns.

These references do not demonstrate that a specific external API, semantic-model version, connector implementation, Digital Twin Registry, BPDM Pool, BPN Discovery service, or dataspace profile was available, deployed, supported or successfully tested.

### Intended configuration defaults

The implementation contains configurable defaults intended to support future integration work. They are design-time assumptions only.

| Integration area              | Configuration or source-code assumption                        | Validation status                                                                     |
| ----------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Dataspace / connector profile | `CX_DATASPACE_VERSION=saturn`                                  | Not tested against a live connector                                                   |
| BPDM Pool                     | API path default `/pool/v6`                                    | No live endpoint or API version validated                                             |
| BPN Discovery                 | API path default `/api/v1.0/search`; key type `materialNumber` | No live endpoint or API version validated                                             |
| Digital Twin Registry         | Asset-link path default `/lookup/shells`                       | No live DTR tested                                                                    |
| AAS submodel access           | Handles `SUBMODEL-VALUE-3.1` where advertised by a descriptor  | No live descriptor or interface tested                                                |
| Tractus-X SDK                 | Referenced by the implementation when real mode is enabled     | Version recorded as 0.7.1; no real-mode runtime or interoperability testing performed |

Future work must establish a controlled Catena-X test environment, confirm the relevant service contracts and versions, validate authentication and access policies, test representative lookup scenarios, and document interoperability evidence before making compatibility or conformance claims.

### Third-party software

This software is implemented in Python 3.12 and uses Python standard-library modules, including facilities for JSON processing, logging, typing, data classes, file paths and abstract-syntax-tree handling.

External third-party dependencies are listed in requirements-lock.txt. The release documentation currently identifies the following dependencies:

* CadQuery 2.6.0 (parametric CAD modelling library)
* cadquery-ocp / OCP 7.8.1.1.post1 (Python bindings for the OpenCascade CAD kernel)
* Open CASCADE Technology (OCCT) (the native CAD kernel used through OCP/CadQuery)
* Matplotlib 3.10.1
* FastAPI 0.120.4
* Pydantic 2.12.5
* Requests 2.32.5
* Uvicorn 0.34.3
* PyQt5 5.15.11 (desktop user interface)
* Qt runtime libraries 5.15.2 (used underneath PyQt5)
* Eclipse Tractus-X SDK 0.7.1 (when real Catena-X dataspace connectivity is enabled)
* PyInstaller 6.19.0 (Just used for application packaging and splash-screen support. Not needed for running the application.)

The Python standard library is not listed module-by-module. CadQuery and OCP are licensed under Apache License 2.0. Exact versions and licence information for external dependencies must be maintained in `requirements-lock.txt` and `THIRD_PARTY_NOTICES.md`.

Users distributing modified or packaged versions of this software are responsible for complying with the licence terms of all dependencies, particularly PyQt5 and the installed Tractus-X SDK version. The presence of a dependency in the source code does not establish that it was installed, configured or tested in a real Catena-X environment.

### Data transformation and methodological limitations

The software contains project-specific logic intended to normalise material-related payloads into a local material-output structure. The implemented logic is designed to extract, where corresponding data are available:

* supplier and site information;
* material names;
* secondary-material or recyclate-content values;
* selected material-related flags from Chemical Material Passport-style payloads.

The implementation includes tolerant handling for several anticipated JSON envelope and field-name variants. Because no live Catena-X, BPDM, BPN Discovery, Digital Twin Registry or partner-service payloads were available for testing, this handling has not been validated against external provider responses or semantic-model implementations.

The environmental- and health-harmfulness outputs are **rule-based screening indicators** derived from terms found in Chemical Material Passport-style payloads. They are not a legal, regulatory, laboratory, or expert classification of a substance or material. In particular, they must not be presented as a formal classification under the EU Classification, Labelling and Packaging (CLP) Regulation without an appropriate validated assessment.

### Mock data

Mock mode is provided exclusively for local development, demonstrations and testing. Example BPNs, supplier names, addresses, material numbers, Chemical Material Passport values and related records in the mock-data module are synthetic unless explicitly identified otherwise.

Mock data and mock-mode outputs do not demonstrate real connectivity, interoperability, semantic conformance, data validity or compatibility with a live Catena-X environment.

### Security and confidentiality

Do not commit `.env` files, credentials, access tokens, client secrets, confidential partner data, personal data or unpublished project results to source control.

Before future use of external AI services, hosted development tools or live Catena-X services, ensure that code, configuration, data and prompts comply with applicable confidentiality, data-protection, intellectual-property and consortium obligations.

### AI-assisted development disclosure

Generative AI tools were used during development for code drafting, refactoring, documentation and/or test generation. All AI-assisted code was reviewed, tested and edited by the project team. The authors remain responsible for the correctness, security, licensing and compliance of the software.

### Licence

Unless stated otherwise, the source code authored for this repository is licensed under the GNU General Public License, version 3 only (GPL-3.0-only).

Third-party components remain subject to their respective licence terms. Exact dependency versions are recorded in requirements-lock.txt, and applicable third-party notices are provided in THIRD_PARTY_NOTICES.md.

This licence statement applies only after all relevant copyright holders, including project beneficiaries, employers, contractors and contributors, have approved publication under GPL-3.0-only.

### Citation

When referencing this software in a report, deliverable or publication, use:

> `Digiser, Riech & Nebel` (2026). *Circular DESIGNer*. Version `1.0.0`. Repository: `10.5281/zenodo.21030411`.

Please also cite the applicable Catena-X semantic-model, AAS API, BPDM, BPN Discovery and Tractus-X SDK documentation used for the specific deployment or release.

### Acknowledgement
This work was funded by the European Union's Horizon
Europe research and innovation programme, under
No. 101138034 as part of the project Zero Emission electric
Vehicles enabled by haRmonised circularity (ZEvRA).
Views and opinions expressed are however those of the
authors only and do not necessarily reflect those of the
European Union or the European Climate, Infrastructure and
Environment Executive Agency (CINEA). Neither the
European Union nor the CINEA can be held responsible for
them.

