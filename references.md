# References

## app_data/materials_validation.json

The values in app_data/materials_validation.json are screening-level model inputs intended for illustrative and comparative use only.

They are based on publicly available sources, calculations, and assumptions. No confidential, proprietary, non-public, or supplier-provided information obtained under confidentiality was used.

Unless an individual entry explicitly states otherwise, values in this file are not official manufacturer specifications, product declarations, certificates, test results, or verified current product data. They may not apply to every grade, configuration, thickness, manufacturing location, production period, or end-of-life route.

Material and trade names are used solely to identify the relevant materials or products. This repository is not affiliated with, sponsored by, or endorsed by any manufacturer or supplier.

The data should not be used as the sole basis for procurement, product certification, regulatory compliance, safety decisions, or engineering design.

### Litecor

This entry is a public-source screening model for LITECOR®, not a current supplier
specification, product declaration, procurement specification, or engineering approval.

LITECOR® is used only as a product/trademark identifier. This repository is independent
and is not affiliated with, endorsed by, or based on confidential information from
thyssenkrupp or any supplier.

Values explicitly identified as “estimated”, “assumed”, or “screening inputs” are model
assumptions selected by the repository maintainers. They are not verified LITECOR®
product data and should not be interpreted as applying to every grade, thickness, region,
or end-of-life route.

#### density 

**Public-source-derived apparent density for one historical configuration.**

Reference [45] reports a `0.2 + 0.4 + 0.2 = 0.80 mm` LITECOR® configuration with a
mass per unit area of `3.50 kg/m²`.

Dataset value:
`3.50 kg/m² ÷ 0.00080 m = 4,375 kg/m³`

This is a derived apparent density for that nominal configuration, not a universal
supplier-stated density. Other Litecor configurations may have different values.

[45] ThyssenKrupp Steel Europe, compact steel: The ThyssenKrupp Steel Europe Customer Magazine, no. 01/2014, 2014. https://www.thyssenkrupp-steel.com/media/content_1/publikationen/compact_steel_2014_1_de.pdf

#### recycling_percentage & recyclate_content

**Illustrative screening-model inputs; not verified LITECOR® product data.**

| Material stream | Assumed mass fraction | Assumed end-of-life recycling rate | Assumed recycled input content |
|---|---:|---:|---:|
| Steel-containing layers | 90% | 90% | 25% |
| Polymer core | 10% | 41% | 0% |

Under these assumptions:
- Estimated end-of-life recycling rate: `0.90 × 0.90 + 0.10 × 0.41 = 85%`
- Estimated recycled input content: `0.90 × 0.25 + 0.10 × 0 = 22.5%`

These values are scenario assumptions, not measured Litecor recycling performance.
For externally sourced benchmarks, specify the geography, reporting year, recycling
definition, and source for each input.

#### recycling_criticality

**Screening-level engineering assessment; not a measured end-of-life result.**

Public literature describes a layered construction comprising steel faces, zinc corrosion
protection, and a PA6/PE/additive polymer core. Relative to monolithic steel, this
construction may require additional separation and material-quality-management steps at
end of life. Actual recycling outcomes depend on the dismantling, shredding, separation,
and recycling route available in the relevant region.

#### additives_or_fillers
Public literature reports, for a tested configuration, a polymer core comprising
52 wt.% PA6, 36 wt.% PE, and 12 wt.% unspecified other additives. The sources do not
identify those additives or establish that they are fillers. This composition is reported
for the studied material/configuration and should not be treated as universal.

[46] T. Trzepieciński, A. Kubit, and J. Slota, “Assessment of the tribological properties of the steel/polymer/steel sandwich material LITECOR,” Lubricants, vol. 10, no. 5, Art. no. 99, 2022, doi: 10.3390/lubricants10050099.

#### surface_coatings
Public literature reports galvanized steel cover layers and zinc corrosion protection for
tested Litecor configurations. This should not be read as confirmation that every Litecor
grade, thickness, or production period uses the same coating system, coating mass, or
surface finish.

[46] T. Trzepieciński, A. Kubit, and J. Slota, “Assessment of the tribological properties of the steel/polymer/steel sandwich material LITECOR,” Lubricants, vol. 10, no. 5, Art. no. 99, 2022, doi: 10.3390/lubricants10050099.

[47] A. Kubit, M. Korzeniowski, M. Bobusia, K. Ochałek, and J. Slota, “Analysis of the possibility of forming stiffening ribs in Litecor metal-plastic composite using the single point incremental forming method,” Key Engineering Materials, vol. 926, pp. 802–814, 2022, doi: 10.4028/p-i92gl3.

## joining_connections.json

### 4

[1] *Fertigungsverfahren Fügen – Teil 0: Allgemeines; Einordnung, Unterteilung, Begriffe*, DIN 8593-0:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500684.

#### 4.1

[2] *Fertigungsverfahren Fügen – Teil 1: Zusammensetzen; Einordnung, Unterteilung, Begriffe*, DIN 8593-1:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500685.

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

#### 4.2

[3] *Fertigungsverfahren Fügen – Teil 2: Füllen; Einordnung, Unterteilung, Begriffe*, DIN 8593-2:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500686.

##### 4.2.1

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

##### 4.2.2

[25] Godfrey & Wing, “What Is Continuous Flow Vacuum Impregnation?” blog post, May 29, 2014. https://www.godfreywing.com/blog/what-is-continuous-flow-vacuum-impregnation/

[26] Ceedee Vacuum, Vacuum Impregnation, product catalog, n.d. https://www.ceedeevacuum.in/download/Catalouge.pdf

#### 4.3

[4] *Fertigungsverfahren Fügen – Teil 3: Anpressen, Einpressen; Einordnung, Unterteilung, Begriffe*, DIN 8593-3:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500687.

##### 4.3.1, 4.3.2, 4.3.3, 4.3.5, 4.3.6 and 4.3.7

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

##### 4.3.4

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

###### 4.3.4.1

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

###### 4.3.4.1#Verstiften

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

###### 4.3.4.2

[19] HAIMER, POWER CLAMP, user manual, Doc. 917000-0020_EN, Index B.1, n.d. https://www.haimer.com/HAIMER%20WEBSITE%20IMAGES%20AND%20CONTENT/HAIMER%20WEBSITE%20IMAGES%20AND%20VIDEOS/News%20%26%20Media/Mediacenter/manuals/power-clamp-b/917000-0020_EN__B__.pdf

[14] Ultraflex Power Technologies, Induction Gets Me Hot: Induction Heating Application Viewbook, n.d. https://ultraflexpower.com/wp-content/uploads/2017/10/Induction-Gets-Me-Hot-Application-Viewbook.pdf

[20] CTI EvoSet, EasyShrink® Evo User Instructions, n.d. https://www.cti-evoset.com/wp-content/uploads/EasyShrink_Evo_GB.pdf

###### 4.3.4.3

[21] N. Harvey, “Liquid Nitrogen Shrink-Fitting Process,” J. Purdue Undergraduate Research, vol. 13, Art. 24, 2023, doi: 10.7771/2158-4052.1654.

[22] W. J. Grant, “Shrink fitting,” Cryogenics, vol. 12, pp. 328–333, Aug. 1972, doi: 10.1016/0011-2275(72)90059-8.

#### 4.4.

[5] *Fertigungsverfahren Fügen – Teil 4: Fügen durch Urformen; Einordnung, Unterteilung, Begriffe*, DIN 8593-4:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500688.

##### 4.4.1

[17] Avient, GLS™ TPE Overmolding Guide, n.d. https://www.avient.com/sites/default/files/2020-10/tpe-overmold-design-guide.pdf

[18] E. I. du Pont de Nemours and Company, Hytrel® Injection Molding Guide, 2000. https://dupont.materialdatacenter.com/links/processing/Hytrel.pdf

[28] Multicomp Pro, Epoxy Resin, data sheet, ver. 1.1, 2022. https://www.farnell.com/datasheets/3792666.pdf

##### 4.4.2 and 4.4.2.1

[17] Avient, GLS™ TPE Overmolding Guide, n.d. https://www.avient.com/sites/default/files/2020-10/tpe-overmold-design-guide.pdf

[18] E. I. du Pont de Nemours and Company, Hytrel® Injection Molding Guide, 2000. https://dupont.materialdatacenter.com/links/processing/Hytrel.pdf

###### 4.4.2.2

[17] Avient, GLS™ TPE Overmolding Guide, n.d. https://www.avient.com/sites/default/files/2020-10/tpe-overmold-design-guide.pdf

[18] E. I. du Pont de Nemours and Company, Hytrel® Injection Molding Guide, 2000. https://dupont.materialdatacenter.com/links/processing/Hytrel.pdf

[28] Multicomp Pro, Epoxy Resin, data sheet, ver. 1.1, 2022. https://www.farnell.com/datasheets/3792666.pdf

###### 4.4.2.3

[29] M. N. Alam, V. Kumar, S. U. Jeong, and S.-S. Park, “Enhancing Rubber Vulcanization Cure Kinetics: Lowering Vulcanization Temperature by Addition of MgO as Co-Cure Activator in ZnO-Based Cure Activator Systems,” Polymers, vol. 16, no. 7, Art. no. 876, 2024, doi: 10.3390/polym16070876.

[30] NOCIL Limited, Vulcanization & Accelerators, technical note, Dec. 2010. https://lusida.com/wp-content/uploads/2018/11/DTechnicalNote-Vulcanization-Dec10.pdf

##### 4.4.3

[27] MacDermid Alpha Electronics Solutions, Electrolube® ER2218: Epoxy Resin, technical data sheet, Feb. 2, 2022. https://www.macdermidalpha.com/sites/default/files/2025-06/Electrolube-ER2218-PTC-TDS-GL-EN-02Feb2022.pdf

[28] Multicomp Pro, Epoxy Resin, data sheet, ver. 1.1, 2022. https://www.farnell.com/datasheets/3792666.pdf

##### 4.4.4

[31] Nickel Institute, Nickel Plating Handbook, 2nd ed., 2023. https://nickelinstitute.org/media/lxxh1zwr/2023-nickelplatinghandbooka5_printablepdf.pdf

##### 4.4.5

[17] Avient, GLS™ TPE Overmolding Guide, n.d. https://www.avient.com/sites/default/files/2020-10/tpe-overmold-design-guide.pdf

[18] E. I. du Pont de Nemours and Company, Hytrel® Injection Molding Guide, 2000. https://dupont.materialdatacenter.com/links/processing/Hytrel.pdf

##### 4.4.6

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

#### 4.5

[6] *Fertigungsverfahren Fügen – Teil 5: Fügen durch Umformen; Einordnung, Unterteilung, Begriffe*, DIN 8593-5:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500689.

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

#### 4.6

[7] *Fertigungsverfahren Fügen – Teil 6: Fügen durch Schweißen; Einordnung, Unterteilung, Begriffe*, DIN 8593-6:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500690.

##### 4.6.1

[13] AMADA WELD TECH, Fundamentals of Small Parts Resistance Welding, n.d. https://amadaweldtech.com/wp-content/uploads/2023/04/Resistance-Welding-Fundamentals.pdf

##### 4.6.2

[12] TRUMPF, Laser Welding, white paper, n.d. https://www.apricon.fi/wp-content/uploads/trumpf_whitepaper_laser_welding_en.pdf

#### 4.7

[8] *Fertigungsverfahren Fügen – Teil 7: Fügen durch Löten; Einordnung, Unterteilung, Begriffe*, DIN 8593-7:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500691.

##### 4.7.1, 4.7.1.1, 4.7.1.2, 4.7.1.3, 4.7.1.4, 4.7.1.5 and 4.7.1.7

[14] Ultraflex Power Technologies, Induction Gets Me Hot: Induction Heating Application Viewbook, n.d. https://ultraflexpower.com/wp-content/uploads/2017/10/Induction-Gets-Me-Hot-Application-Viewbook.pdf

[15] Metcal, Hand Soldering with Lead-Free Alloys, white paper, 2019. https://metcal.com/wp-content/uploads/2021/02/White-Paper-Hand-Soldering-with-Lead-Free-Alloys.pdf

[16] R. Sharma, “Solder Reflow Recommendation,” Microchip Technology Inc., Appl. Note AN233, DS00233D, 2004. https://ww1.microchip.com/downloads/en/Appnotes/00233D.pdf

###### 4.7.1.8

[16] R. Sharma, “Solder Reflow Recommendation,” Microchip Technology Inc., Appl. Note AN233, DS00233D, 2004. https://ww1.microchip.com/downloads/en/Appnotes/00233D.pdf

##### 4.7.2, 4.7.2.2, 4.7.2.3, 4.7.2.4, 4.7.2.5 and 4.7.2.7

[23] THESSCO, Hand Torch or Flame Brazing Principles, n.d. https://www.thesscogroup.com/wp-content/uploads/2024/09/THESSCO_handtorchv1feb2018.pdf

[24] Höganäs AB, Induction Brazing, data sheet 2312HOG, Aug. 2018. https://www.hoganas.com/globalassets/downloads/libary/brazing_induction-brazing_2312hog.pdf

###### 4.7.2.8

[24] Höganäs AB, Induction Brazing, data sheet 2312HOG, Aug. 2018. https://www.hoganas.com/globalassets/downloads/libary/brazing_induction-brazing_2312hog.pdf

[32] Euro Superabrasives, High Speed Vacuum Brazing Machine, product brochure, n.d. https://eurosuperabrasives.com/wp-content/uploads/2019/07/PP-S_eBrochure_EN.pdf

[33] GH Induction Group, Heat Treatment and Brazing in Vacuum & High Temperature: Vacuum Furnace, brochure GHCOM014006, n.d. https://ghinduction.com/wp-content/uploads/2023/01/GHCOM014006-Vacuum-furnaces.pdf 

#### 4.8

[9] *Fertigungsverfahren Fügen – Teil 8: Kleben; Einordnung, Unterteilung, Begriffe*, DIN 8593-8:2003-09, Deutsches Institut für Normung e.V., Berlin, Germany, Sep. 2003, doi: 10.31030/9500692.

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

#### 4.9

[10] J. R. Peeters, P. Tecchio, F. Ardente, P. Vanegas, D. Coughlan, and J. R. Duflou, eDIM: Further Development of the Method to Assess the Ease of Disassembly and Reassembly of Products—Application to Notebook Computers, EUR 28758 EN, JRC107773. Luxembourg: Publications Office of the European Union, 2018, doi: 10.2760/864982.

[11] P. Vanegas, J. R. Peeters, D. Cattrysse, J. R. Duflou, P. Tecchio, F. Mathieux, and F. Ardente, Study for a Method to Assess the Ease of Disassembly of Electrical and Electronic Equipment: Method Development and Application in a Flat Panel Display Case Study, EUR 27921 EN, JRC101479. Luxembourg: Publications Office of the European Union, 2016, doi: 10.2788/130925.

## cx_material_consumer

### Design references

The following references were identified after development as relevant design inputs for the prototype. They document concepts, semantic identifiers, application programming interfaces (APIs), and reference implementations reflected in the source code.

They do **not** demonstrate that the referenced standards, services, APIs, or implementations were available, deployed, consulted during development, validated, tested, or implemented conformantly by this project.

#### Semantic models and AAS interfaces

1. **Eclipse Tractus-X, *sldt-semantic-models* repository** [34]. Relevant versioned semantic-model artifacts referenced by the prototype include:

   * `urn:samm:io.catenax.secondary_material_content_calculated:1.0.0#SecondaryMaterialContentCalculated`
   * `urn:samm:io.catenax.secondary_material_content_verifiable:1.0.0#SecondaryMaterialContentVerifiable`
   * `urn:samm:io.catenax.material.chemical_material_passport:1.0.0#ChemicalMaterialPassport`
   * `urn:samm:io.catenax.part_type_information:1.0.0#PartTypeInformation`

   **Role:** Design reference for semantic identifiers and anticipated material-related payload structures.

2. **Industrial Digital Twin Association (IDTA), *Specification of the Asset Administration Shell—Part 2: Application Programming Interfaces*, IDTA-01002, ver. 3.1.1, Jul. 2025** [35].

   **Role:** Design reference for Asset Administration Shell (AAS) shell and submodel descriptors, endpoint metadata, and the `SUBMODEL-VALUE-3.1` interface naming pattern.

3. **Catena-X Automotive Network e.V., *CX-0126 Industry Core: Part Type*, ver. 2.1.1** [36].

   **Role:** Contextual reference for the `PartTypeInformation` semantic-model family. The prototype contains the earlier `PartTypeInformation` 1.0.0 semantic identifier; compatibility between that identifier and later standard releases has not been validated.

#### Digital twins and dataspace concepts

4. **Catena-X Automotive Network e.V., *CX-0002 Digital Twins in Catena-X*, ver. 2.4.0** [37].

   **Role:** Conceptual reference for digital-twin and Digital Twin Registry patterns.

5. **Eclipse Tractus-X, *sldt-digital-twin-registry* reference implementation and changelog** [38].

   **Role:** Implementation-specific design context for Digital Twin Registry lookup behaviour. This does not assert that the prototype implements, targets, or interoperates with a particular Digital Twin Registry release or endpoint.

6. **Catena-X Automotive Network e.V., *CX-0018 Dataspace Connectivity*, ver. 4.2.1** [39].

   **Role:** Conceptual reference for intended dataspace and connector interaction patterns.

7. **Eclipse Tractus-X, *tractusx-sdk* project** [40].

   **Role:** Third-party software and design context for optional connector, discovery, and Digital Twin Registry access code paths. The project dependency version is recorded separately in `requirements-lock.txt`.

#### Business-partner and discovery concepts

8. **Catena-X Automotive Network e.V., *CX-0010 Business Partner Number*, ver. 3.1.0** [41].

   **Role:** Conceptual reference for BPNL, BPNS, and BPNA identifiers.

9. **Catena-X Automotive Network e.V., *CX-0012 Business Partner Data Pool API*, ver. 5.1.1** [42].

   **Role:** Design reference for Business Partner Data Management Pool concepts, including business-partner, legal-entity, site, and address records. The configured `/pool/v6` path in this prototype has not been validated against this or another BPDM API release.

10. **Catena-X Automotive Network e.V., *CX-0053 Discovery Finder and BPN Discovery Service APIs*, ver. 1.1.1** [43].

    **Role:** Design reference for resolving Business Partner Numbers from other identifiers. The configured `/api/v1.0/search` path and `materialNumber` lookup key have not been validated against a live BPN Discovery service.

11. **Catena-X Automotive Network e.V., *CX-0131 Circularity Core*, ver. 1.1.1** [44].

    **Role:** Contextual reference for circularity and secondary-material-content concepts. It does not validate the project’s extraction logic, calculations, or material-related screening indicators.

### Reference-status statement

These materials are included as design references for an unvalidated prototype. Their inclusion must not be interpreted as evidence of Catena-X onboarding, service access, semantic interoperability, standards conformance, certification, or successful integration testing.

### References

[34] Eclipse Tractus-X, “sldt-semantic-models,” GitHub software repository, `eclipse-tractusx/sldt-semantic-models`, including versioned SAMM semantic-model artifacts. [Online]. Accessed: Jun. 30, 2026.

[35] Industrial Digital Twin Association e.V., *Specification of the Asset Administration Shell—Part 2: Application Programming Interfaces*, IDTA-01002, ver. 3.1.1, Jul. 2025, doi: 10.62628/IDTA.01002-3-1-1.

[36] Catena-X Automotive Network e.V., *CX-0126 Industry Core: Part Type*, ver. 2.1.1, online standard. [Online]. Accessed: Jun. 30, 2026.

[37] Catena-X Automotive Network e.V., *CX-0002 Digital Twins in Catena-X*, ver. 2.4.0, online standard. [Online]. Accessed: Jun. 30, 2026.

[38] Eclipse Tractus-X, “sldt-digital-twin-registry,” GitHub software repository and changelog, `eclipse-tractusx/sldt-digital-twin-registry`. [Online]. Accessed: Jun. 30, 2026.

[39] Catena-X Automotive Network e.V., *CX-0018 Dataspace Connectivity*, ver. 4.2.1, online standard. [Online]. Accessed: Jun. 30, 2026.

[40] Eclipse Tractus-X, “tractusx-sdk: Eclipse Tractus-X Software Development Kit—The Dataspace & Industry Foundation Libraries,” GitHub software repository, `eclipse-tractusx/tractusx-sdk`. [Online]. Accessed: Jun. 30, 2026.

[41] Catena-X Automotive Network e.V., *CX-0010 Business Partner Number*, ver. 3.1.0, online standard. [Online]. Accessed: Jun. 30, 2026.

[42] Catena-X Automotive Network e.V., *CX-0012 Business Partner Data Pool API*, ver. 5.1.1, online standard. [Online]. Accessed: Jun. 30, 2026.

[43] Catena-X Automotive Network e.V., *CX-0053 Discovery Finder and BPN Discovery Service APIs*, ver. 1.1.1, online standard. [Online]. Accessed: Jun. 30, 2026.

[44] Catena-X Automotive Network e.V., *CX-0131 Circularity Core*, ver. 1.1.1, online standard. [Online]. Accessed: Jun. 30, 2026.

## tool.py

[45] CadQuery contributors, “CadQuery”. Zenodo, Oct. 28, 2025. doi: 10.5281/zenodo.14590990.

