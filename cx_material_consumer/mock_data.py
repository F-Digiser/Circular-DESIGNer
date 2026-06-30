""""    
    Copyright (C) 2026  Digiser

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

MOCK_BPN_DISCOVERY: dict[str, list[str]] = {
    "MAT-4711": ["BPNL000000000001"],
    "MAT-AMBIG": ["BPNL000000000001", "BPNL000000000002"],
    "MAT-NOCMP": ["BPNL000000000001"],
}

MOCK_SUPPLIERS: dict[str, dict] = {
    "BPNL000000000001": {
        "supplier_name": "PolyChem Materials GmbH",
        "city_name": "Stuttgart",
        "country_alpha2": "DE",
        "address_bpna": "BPNA000000000001",
        "sites": {
            "BPNS000000000111": {
                "bpns": "BPNS000000000111",
                "name": "PolyChem Stuttgart Plant",
                "mainAddress": {"bpna": "BPNA000000000001"},
                "legalEntity": "BPNL000000000001",
            }
        },
        "addresses": {
            "BPNA000000000001": {
                "bpna": "BPNA000000000001",
                "name": "PolyChem Materials GmbH",
                "physicalPostalAddress": {
                    "streetName": "Industriestrasse",
                    "houseNumber": "7",
                    "zipCode": "70173",
                    "cityName": "Stuttgart",
                    "countryAlpha2": "DE",
                },
            }
        },
        "legal_entity": {
            "bpnl": "BPNL000000000001",
            "legalName": "PolyChem Materials GmbH",
        },
        "materials": {
            "MAT-4711": {
                "shell_id": "aas-polychem-mat-4711",
                "part_type_information": {
                    "manufacturerPartId": "MAT-4711",
                    "partTypeInformation": {
                        "manufacturerPartId": "MAT-4711",
                        "nameAtManufacturer": "PA6 GF30",
                    },
                    "partSitesInformationAsPlanned": [
                        {"function": "Production", "catenaXsiteId": "BPNS000000000111"}
                    ],
                },
                "smc": {
                    "secondaryMaterialContent": [
                        {"secondaryMaterialContentPercentage": 32.5, "materialName": "Recycled polymer share"}
                    ]
                },
                "cmp": {
                    "hazardAssessment": {"overallAssessment": "Contains substances hazardous to aquatic environment"},
                    "transport": {"transportClass": "notRegulated"},
                    "disposal": {"disposalRecommendation": "Follow local regulations"},
                    "safety": {"ppe": "gloves"},
                    "compliance": {"reach": "declared"},
                    "substanceOfConcern": [
                        {
                            "name": "Additive X",
                            "location": "matrix",
                            "concentration": 0.8,
                            "hazardClassification": {
                                "category": "Aquatic Chronic 2",
                                "remarks": "Toxic to aquatic life with long lasting effects"
                            },
                        }
                    ],
                },
            },
            "MAT-AMBIG": {
                "shell_id": "aas-polychem-mat-ambig",
                "part_type_information": {
                    "manufacturerPartId": "MAT-AMBIG",
                    "partTypeInformation": {
                        "manufacturerPartId": "MAT-AMBIG",
                        "nameAtManufacturer": "POM Natural",
                    },
                    "partSitesInformationAsPlanned": [
                        {"function": "Production", "catenaXsiteId": "BPNS000000000111"}
                    ],
                },
                "smc": {
                    "secondaryMaterialContent": [
                        {"secondaryMaterialContentPercentage": 10.0, "materialName": "Recycled polymer share"}
                    ]
                },
                "cmp": None,
            },
            "MAT-NOCMP": {
                "shell_id": "aas-polychem-mat-nocmp",
                "part_type_information": {
                    "manufacturerPartId": "MAT-NOCMP",
                    "partTypeInformation": {
                        "manufacturerPartId": "MAT-NOCMP",
                        "nameAtManufacturer": "ABS Flame Retardant",
                    },
                    "partSitesInformationAsPlanned": [
                        {"function": "Production", "catenaXsiteId": "BPNS000000000111"}
                    ],
                },
                "smc": {
                    "secondaryMaterialContent": [
                        {"secondaryMaterialContentPercentage": 5.5, "materialName": "Recycled polymer share"}
                    ]
                },
                "cmp": None,
            },
        },
    },
    "BPNL000000000002": {
        "supplier_name": "Global Resins AG",
        "city_name": "Ludwigshafen",
        "country_alpha2": "DE",
        "address_bpna": "BPNA000000000002",
        "sites": {
            "BPNS000000000222": {
                "bpns": "BPNS000000000222",
                "name": "Global Resins Ludwigshafen Plant",
                "mainAddress": {"bpna": "BPNA000000000002"},
                "legalEntity": "BPNL000000000002",
            }
        },
        "addresses": {
            "BPNA000000000002": {
                "bpna": "BPNA000000000002",
                "name": "Global Resins AG",
                "physicalPostalAddress": {
                    "streetName": "Chemiepark",
                    "houseNumber": "12",
                    "zipCode": "67059",
                    "cityName": "Ludwigshafen",
                    "countryAlpha2": "DE",
                },
            }
        },
        "legal_entity": {
            "bpnl": "BPNL000000000002",
            "legalName": "Global Resins AG",
        },
        "materials": {
            "MAT-AMBIG": {
                "shell_id": "aas-globalresins-mat-ambig",
                "part_type_information": {
                    "manufacturerPartId": "MAT-AMBIG",
                    "partTypeInformation": {
                        "manufacturerPartId": "MAT-AMBIG",
                        "nameAtManufacturer": "POM Natural Premium",
                    },
                    "partSitesInformationAsPlanned": [
                        {"function": "Production", "catenaXsiteId": "BPNS000000000222"}
                    ],
                },
                "smc": {
                    "secondaryMaterialContent": [
                        {"secondaryMaterialContentPercentage": 18.0, "materialName": "Recycled polymer share"}
                    ]
                },
                "cmp": {
                    "hazardAssessment": {"overallAssessment": "Contains acute tox classification"},
                    "transport": {"transportClass": "notRegulated"},
                    "disposal": {"disposalRecommendation": "Follow SDS"},
                    "safety": {"ppe": "gloves,goggles"},
                    "compliance": {"reach": "declared"},
                    "substanceOfConcern": [
                        {
                            "name": "Additive Y",
                            "location": "matrix",
                            "concentration": 0.4,
                            "hazardClassification": {
                                "category": "Acute Tox 4",
                                "remarks": "Acute tox skin corr signal"
                            },
                        }
                    ],
                },
            }
        },
    },
}
