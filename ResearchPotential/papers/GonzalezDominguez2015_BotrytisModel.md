# A Mechanistic Model of Botrytis cinerea on Grapevines That Includes Weather, Vine Growth Stage, and the Main Infection Pathways

- **Authors:** Elisa Gonzalez-Dominguez, Tito Caffi, Nicola Ciliberti, Vittorio Rossi
- **Year:** 2015
- **Journal:** PLoS ONE, 10(10), e0140444
- **DOI:** 10.1371/journal.pone.0140444
- **Access:** Open access at [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0140444)
- **Status:** FULL TEXT AVAILABLE

## Abstract

This paper presents a mechanistic disease prediction model for gray mould (Botrytis cinerea) affecting grapevines. The model integrates weather data, vine phenological stages, and multiple infection pathways to predict epidemic severity.

## Key Model Components

### Two Infection Periods
1. **First period (flowering through early fruit development):** Models conidial infection of inflorescences and young clusters, producing severity value SEV1
2. **Second period (veraison through harvest):** Models conidial infection of ripening berries (SEV2) and berry-to-berry mycelial spread (SEV3)

### Main Variables
- Sporulation rates based on temperature, moisture availability, mycelial colonization
- Infection rates depend on environmental conditions (temperature, wetness duration) and host susceptibility
- Three severity outputs: SEV1, SEV2, SEV3

## Validation

- Tested against 21 vineyard epidemics (2009-2014) across Italy and France
- No fungicide applications in test plots
- Disease assessed at harvest as incidence and severity percentages
- Three epidemic categories: Mild (<24% incidence), Intermediate (25-74%), Severe (>=75%)
- **Correctly classified 17 of 21 epidemics (81% accuracy)**
- Cross-validation: 71.4% correct classification

## Key Results

- SEV1 primarily distinguishes mild from intermediate epidemics
- SEV2 and SEV3 separate intermediate from severe cases
- Model provides mechanistic basis for timing fungicide applications

## Relevance to Tokaj Research

This is the key Botrytis model for Manuscript 2. **The Botrytis angle is uniquely important for Tokaj** because B. cinerea as noble rot (aszu) is the region's defining product. Spatial mapping of conditions favoring noble rot vs. destructive grey rot across Tokaj's 50-station network would be economically significant and scientifically novel.
