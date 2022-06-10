import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.models import Account, VerificationCode, UserProfilePicture
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from verification.random_code_gen import rand_num_gen
from verification.email_threadings import EmailThreading
from django.utils import timezone
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from product.models import *
from game.models import *
import uuid
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import json
import asyncio
import threading
from product.models import *
from advertisement.models import *
from core.models import *
from config.activate_deactivate_status import activate_status, deactivate_status
from config.custom_functions import delete_obj

# woocomerce to connect with woocommerce store
from woocommerce import API
import asyncio
import requests



wcapi = API(
    url="https://www.ddmcustomz.ca",
    consumer_key="ck_d7b8e625408c67fc0351b88ea84e04b6f2657ce1",
    consumer_secret="cs_ba22b43fc833f3dc319f5385c027e6d79b73aaab",
    version="wc/v3",
    # timeout=100,
)

def authorizationAPI(request):
    import requests

    url = "https://apis-sandbox.fedex.com/oauth/token"

    payload = "grant_type=client_credentials&client_id=l7a4f692dd1a4b400589fdaf6f417cc8e2&client_secret=3941c778053749089b74b942b40ee601"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return render(request, 'test.html')


def checkAPI(request):

    payload = {
        "mergeLabelDocOption": "LABELS_AND_DOCS",
        "requestedShipment": {
            "shipDatestamp": "2019-10-14",
            "totalDeclaredValue": {
                "amount": 12.45,
                "currency": "USD"
            },
            "shipper": {
                "address": {
                    "streetLines": [
                        "10 FedEx Parkway",
                        "Suite 302"
                    ],
                    "city": "Beverly Hills",
                    "stateOrProvinceCode": "CA",
                    "postalCode": "90210",
                    "countryCode": "US",
                    "residential": 'false'
                },
                "contact": {
                    "personName": "John Taylor",
                    "emailAddress": "sample@company.com",
                    "phoneExtension": "91",
                    "phoneNumber": "XXXX567890",
                    "companyName": "Fedex"
                },
                "tins": [
                    {
                        "number": "XXX567",
                        "tinType": "FEDERAL",
                        "usage": "usage",
                        "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                        "expirationDate": "2000-01-23T04:56:07.000+00:00"
                    }
                ]
            },
            "soldTo": {
                "address": {
                    "streetLines": [
                        "10 FedEx Parkway",
                        "Suite 302"
                    ],
                    "city": "Beverly Hills",
                    "stateOrProvinceCode": "CA",
                    "postalCode": "90210",
                    "countryCode": "US",
                    "residential": 'false'
                },
                "contact": {
                    "personName": "John Taylor",
                    "emailAddress": "sample@company.com",
                    "phoneExtension": "91",
                    "phoneNumber": "1234567890",
                    "companyName": "Fedex"
                },
                "tins": [
                    {
                        "number": "123567",
                        "tinType": "FEDERAL",
                        "usage": "usage",
                        "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                        "expirationDate": "2000-01-23T04:56:07.000+00:00"
                    }
                ],
                "accountNumber": {
                    "value": "745379540"
                }
            },
            "recipients": [
                {
                    "address": {
                        "streetLines": [
                            "10 FedEx Parkway",
                            "Suite 302"
                        ],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "90210",
                        "countryCode": "US",
                        "residential": 'false'
                    },
                    "contact": {
                        "personName": "John Taylor",
                        "emailAddress": "sample@company.com",
                        "phoneExtension": "000",
                        "phoneNumber": "XXXX345671",
                        "companyName": "FedEx"
                    },
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00"
                        }
                    ],
                    "deliveryInstructions": "Delivery Instructions"
                }
            ],
            "recipientLocationNumber": "1234567",
            "pickupType": "USE_SCHEDULED_PICKUP",
            "serviceType": "PRIORITY_OVERNIGHT",
            "packagingType": "YOUR_PACKAGING",
            "totalWeight": 20.6,
            "origin": {
                "address": {
                    "streetLines": [
                        "10 FedEx Parkway",
                        "Suite 302"
                    ],
                    "city": "Beverly Hills",
                    "stateOrProvinceCode": "CA",
                    "postalCode": "38127",
                    "countryCode": "US",
                    "residential": 'false'
                },
                "contact": {
                    "personName": "person name",
                    "emailAddress": "email address",
                    "phoneNumber": "phone number",
                    "phoneExtension": "phone extension",
                    "companyName": "company name",
                    "faxNumber": "fax number"
                }
            },
            "shippingChargesPayment": {
                "paymentType": "SENDER",
                "payor": {
                    "responsibleParty": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": 'false'
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneNumber": "XXXX567890",
                            "phoneExtension": "phone extension",
                            "companyName": "Fedex",
                            "faxNumber": "fax number"
                        },
                        "accountNumber": {
                            "value": "745379540"
                        }
                    }
                }
            },
            "shipmentSpecialServices": {
                "specialServiceTypes": [
                    "THIRD_PARTY_CONSIGNEE",
                    "PROTECTION_FROM_FREEZING"
                ],
                "etdDetail": {
                    "attributes": [
                        "POST_SHIPMENT_UPLOAD_REQUESTED"
                    ],
                    "attachedDocuments": [
                        {
                            "documentType": "PRO_FORMA_INVOICE",
                            "documentReference": "DocumentReference",
                            "description": "PRO FORMA INVOICE",
                            "documentId": "090927d680038c61"
                        }
                    ],
                    "requestedDocumentTypes": [
                        "VICS_BILL_OF_LADING",
                        "GENERAL_AGENCY_AGREEMENT"
                    ]
                },
                "returnShipmentDetail": {
                    "returnEmailDetail": {
                        "merchantPhoneNumber": "19012635656",
                        "allowedSpecialService": [
                            "SATURDAY_DELIVERY"
                        ]
                    },
                    "rma": {
                        "reason": "Wrong Size or Color"
                    },
                    "returnAssociationDetail": {
                        "shipDatestamp": "2019-10-01",
                        "trackingNumber": "123456789"
                    },
                    "returnType": "PRINT_RETURN_LABEL"
                },
                "deliveryOnInvoiceAcceptanceDetail": {
                    "recipient": {
                        "address": {
                            "streetLines": [
                                "23, RUE JOSEPH-DE MA",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": 'false'
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneExtension": "000",
                            "phoneNumber": "1234567890",
                            "companyName": "Fedex"
                        },
                        "tins": [
                            {
                                "number": "123567",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00"
                            }
                        ],
                        "deliveryInstructions": "Delivery Instructions"
                    }
                },
                "internationalTrafficInArmsRegulationsDetail": {
                    "licenseOrExemptionNumber": "9871234"
                },
                "pendingShipmentDetail": {
                    "pendingShipmentType": "EMAIL",
                    "processingOptions": {
                        "options": [
                            "ALLOW_MODIFICATIONS"
                        ]
                    },
                    "recommendedDocumentSpecification": {
                        "types": "ANTIQUE_STATEMENT_EUROPEAN_UNION"
                    },
                    "emailLabelDetail": {
                        "recipients": [
                            {
                                "emailAddress": "neena@fedex.com",
                                "optionsRequested": {
                                    "options": [
                                        "PRODUCE_PAPERLESS_SHIPPING_FORMAT",
                                        "SUPPRESS_ACCESS_EMAILS"
                                    ]
                                },
                                "role": "SHIPMENT_COMPLETOR",
                                "locale": "en_US"
                            }
                        ],
                        "message": "your optional message"
                    },
                    "attachedDocuments": [
                        {
                            "documentType": "PRO_FORMA_INVOICE",
                            "documentReference": "DocumentReference",
                            "description": "PRO FORMA INVOICE",
                            "documentId": "090927d680038c61"
                        }
                    ],
                    "expirationTimeStamp": "2020-01-01"
                },
                "holdAtLocationDetail": {
                    "locationId": "YBZA",
                    "locationContactAndAddress": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "38127",
                            "countryCode": "US",
                            "residential": 'false'
                        },
                        "contact": {
                            "personName": "person name",
                            "emailAddress": "email address",
                            "phoneNumber": "phone number",
                            "phoneExtension": "phone extension",
                            "companyName": "company name",
                            "faxNumber": "fax number"
                        }
                    },
                    "locationType": "FEDEX_ONSITE"
                },
                "shipmentCODDetail": {
                    "addTransportationChargesDetail": {
                        "rateType": "ACCOUNT",
                        "rateLevelType": "BUNDLED_RATE",
                        "chargeLevelType": "CURRENT_PACKAGE",
                        "chargeType": "COD_SURCHARGE"
                    },
                    "codRecipient": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": 'false'
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneExtension": "000",
                            "phoneNumber": "XXXX345671",
                            "companyName": "Fedex"
                        },
                        "accountNumber": {
                            "value": "Your account number"
                        },
                        "tins": [
                            {
                                "number": "123567",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00"
                            }
                        ]
                    },
                    "remitToName": "remitToName",
                    "codCollectionType": "ANY",
                    "financialInstitutionContactAndAddress": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "38127",
                            "countryCode": "US",
                            "residential": 'false'
                        },
                        "contact": {
                            "personName": "person name",
                            "emailAddress": "email address",
                            "phoneNumber": "phone number",
                            "phoneExtension": "phone extension",
                            "companyName": "company name",
                            "faxNumber": "fax number"
                        }
                    },
                    "codCollectionAmount": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "returnReferenceIndicatorType": "INVOICE",
                    "shipmentCodAmount": {
                        "amount": 12.45,
                        "currency": "USD"
                    }
                },
                "shipmentDryIceDetail": {
                    "totalWeight": {
                        "units": "LB",
                        "value": 10
                    },
                    "packageCount": 12
                },
                "internationalControlledExportDetail": {
                    "licenseOrPermitExpirationDate": "2019-12-03",
                    "licenseOrPermitNumber": "11",
                    "entryNumber": "125",
                    "foreignTradeZoneCode": "US",
                    "type": "WAREHOUSE_WITHDRAWAL"
                },
                "homeDeliveryPremiumDetail": {
                    "phoneNumber": {
                        "areaCode": "901",
                        "localNumber": "3575012",
                        "extension": "200",
                        "personalIdentificationNumber": "98712345"
                    },
                    "deliveryDate": "2019-06-26",
                    "homedeliveryPremiumType": "APPOINTMENT"
                }
            },
            "emailNotificationDetail": {
                "aggregationType": "PER_PACKAGE",
                "emailNotificationRecipients": [
                    {
                        "name": "Joe Smith",
                        "emailNotificationRecipientType": "SHIPPER",
                        "emailAddress": "jsmith3@aol.com",
                        "notificationFormatType": "TEXT",
                        "notificationType": "EMAIL",
                        "locale": "en_US",
                        "notificationEventType": [
                            "ON_PICKUP_DRIVER_ARRIVED",
                            "ON_SHIPMENT"
                        ]
                    }
                ],
                "personalMessage": "your personal message here"
            },
            "expressFreightDetail": {
                "bookingConfirmationNumber": "123456789812",
                "shippersLoadAndCount": 123,
                "packingListEnclosed": 'true'
            },
            "variableHandlingChargeDetail": {
                "rateType": "PREFERRED_CURRENCY",
                "percentValue": 12.45,
                "rateLevelType": "INDIVIDUAL_PACKAGE_RATE",
                "fixedValue": {
                    "amount": 24.45,
                    "currency": "USD"
                },
                "rateElementBasis": "NET_CHARGE_EXCLUDING_TAXES"
            },
            "customsClearanceDetail": {
                "regulatoryControls": "NOT_IN_FREE_CIRCULATION",
                "brokers": [
                    {
                        "broker": {
                            "address": {
                                "streetLines": [
                                    "10 FedEx Parkway",
                                    "Suite 302"
                                ],
                                "city": "Beverly Hills",
                                "stateOrProvinceCode": "CA",
                                "postalCode": "90210",
                                "countryCode": "US",
                                "residential": 'false'
                            },
                            "contact": {
                                "personName": "John Taylor",
                                "emailAddress": "sample@company.com",
                                "phoneNumber": "1234567890",
                                "phoneExtension": 91,
                                "companyName": "Fedex",
                                "faxNumber": 1234567
                            },
                            "accountNumber": {
                                "value": "Your account number"
                            },
                            "tins": [
                                {
                                    "number": "number",
                                    "tinType": "FEDERAL",
                                    "usage": "usage",
                                    "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                    "expirationDate": "2000-01-23T04:56:07.000+00:00"
                                }
                            ],
                            "deliveryInstructions": "deliveryInstructions"
                        },
                        "type": "IMPORT"
                    }
                ],
                "commercialInvoice": {
                    "originatorName": "originator Name",
                    "comments": [
                        "optional comments for the commercial invoice"
                    ],
                    "customerReferences": [
                        {
                            "customerReferenceType": "INVOICE_NUMBER",
                            "value": "3686"
                        }
                    ],
                    "taxesOrMiscellaneousCharge": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "taxesOrMiscellaneousChargeType": "COMMISSIONS",
                    "freightCharge": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "packingCosts": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "handlingCosts": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "declarationStatement": "declarationStatement",
                    "termsOfSale": "FCA",
                    "specialInstructions": "specialInstructions\"",
                    "shipmentPurpose": "REPAIR_AND_RETURN",
                    "emailNotificationDetail": {
                        "emailAddress": "neena@fedex.com",
                        "type": "EMAILED",
                        "recipientType": "SHIPPER"
                    }
                },
                "freightOnValue": "OWN_RISK",
                "dutiesPayment": {
                    "payor": {
                        "responsibleParty": {
                            "address": {
                                "streetLines": [
                                    "10 FedEx Parkway",
                                    "Suite 302"
                                ],
                                "city": "Beverly Hills",
                                "stateOrProvinceCode": "CA",
                                "postalCode": "38127",
                                "countryCode": "US",
                                "residential": 'false'
                            },
                            "contact": {
                                "personName": "John Taylor",
                                "emailAddress": "sample@company.com",
                                "phoneNumber": "1234567890",
                                "phoneExtension": "phone extension",
                                "companyName": "Fedex",
                                "faxNumber": "fax number"
                            },
                            "accountNumber": {
                                "value": "Your account number"
                            },
                            "tins": [
                                {
                                    "number": "number",
                                    "tinType": "FEDERAL",
                                    "usage": "usage",
                                    "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                    "expirationDate": "2000-01-23T04:56:07.000+00:00"
                                },
                                {
                                    "number": "number",
                                    "tinType": "FEDERAL",
                                    "usage": "usage",
                                    "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                    "expirationDate": "2000-01-23T04:56:07.000+00:00"
                                }
                            ]
                        }
                    },
                    "billingDetails": {
                        "billingCode": "billingCode",
                        "billingType": "billingType",
                        "aliasId": "aliasId",
                        "accountNickname": "accountNickname",
                        "accountNumber": "Your account number",
                        "accountNumberCountryCode": "US"
                    },
                    "paymentType": "SENDER"
                },
                "commodities": [
                    {
                        "unitPrice": {
                            "amount": 12.45,
                            "currency": "USD"
                        },
                        "additionalMeasures": [
                            {
                                "quantity": 12.45,
                                "units": "KG"
                            }
                        ],
                        "numberOfPieces": 12,
                        "quantity": 125,
                        "quantityUnits": "Ea",
                        "customsValue": {
                            "amount": 12.45,
                            "currency": "USD"
                        },
                        "countryOfManufacture": "US",
                        "cIMarksAndNumbers": "87123",
                        "harmonizedCode": "0613",
                        "description": "description",
                        "name": "non-threaded rivets",
                        "weight": {
                            "units": "KG",
                            "value": 68
                        },
                        "exportLicenseNumber": "26456",
                        "exportLicenseExpirationDate": "2022-05-24T09:12:35Z",
                        "partNumber": "167",
                        "purpose": "BUSINESS",
                        "usmcaDetail": {
                            "originCriterion": "A"
                        }
                    }
                ],
                "isDocumentOnly": 'true',
                "recipientCustomsId": {
                    "type": "PASSPORT",
                    "value": "123"
                },
                "customsOption": {
                    "description": "Description",
                    "type": "COURTESY_RETURN_LABEL"
                },
                "importerOfRecord": {
                    "address": {
                        "streetLines": [
                            "10 FedEx Parkway",
                            "Suite 302"
                        ],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "90210",
                        "countryCode": "US",
                        "residential": 'false'
                    },
                    "contact": {
                        "personName": "John Taylor",
                        "emailAddress": "sample@company.com",
                        "phoneExtension": "000",
                        "phoneNumber": "XXXX345671",
                        "companyName": "Fedex"
                    },
                    "accountNumber": {
                        "value": "Your account number"
                    },
                    "tins": [
                        {
                            "number": "123567",
                            "tinType": "FEDERAL",
                            "usage": "usage",
                            "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                            "expirationDate": "2000-01-23T04:56:07.000+00:00"
                        }
                    ]
                },
                "generatedDocumentLocale": "en_US",
                "exportDetail": {
                    "destinationControlDetail": {
                        "endUser": "dest country user",
                        "statementTypes": "DEPARTMENT_OF_COMMERCE",
                        "destinationCountries": [
                            "USA",
                            "India"
                        ]
                    },
                    "b13AFilingOption": "NOT_REQUIRED",
                    "exportComplianceStatement": "export Compliance Statement",
                    "permitNumber": "12345"
                },
                "totalCustomsValue": {
                    "amount": 12.45,
                    "currency": "USD"
                },
                "partiesToTransactionAreRelated": 'true',
                "declarationStatementDetail": {
                    "usmcaLowValueStatementDetail": {
                        "countryOfOriginLowValueDocumentRequested": 'true',
                        "customsRole": "EXPORTER"
                    }
                },
                "insuranceCharge": {
                    "amount": 12.45,
                    "currency": "USD"
                }
            },
            "smartPostInfoDetail": {
                "ancillaryEndorsement": "RETURN_SERVICE",
                "hubId": "5015",
                "indicia": "PRESORTED_STANDARD",
                "specialServices": "USPS_DELIVERY_CONFIRMATION"
            },
            "blockInsightVisibility": 'true',
            "labelSpecification": {
                "labelFormatType": "COMMON2D",
                "labelOrder": "SHIPPING_LABEL_FIRST",
                "customerSpecifiedDetail": {
                    "maskedData": [
                        "CUSTOMS_VALUE",
                        "TOTAL_WEIGHT"
                    ],
                    "regulatoryLabels": [
                        {
                            "generationOptions": "CONTENT_ON_SHIPPING_LABEL_ONLY",
                            "type": "ALCOHOL_SHIPMENT_LABEL"
                        }
                    ],
                    "additionalLabels": [
                        {
                            "type": "CONSIGNEE",
                            "count": 1
                        }
                    ],
                    "docTabContent": {
                        "docTabContentType": "BARCODED",
                        "zone001": {
                            "docTabZoneSpecifications": [
                                {
                                    "zoneNumber": 0,
                                    "header": "string",
                                    "dataField": "string",
                                    "literalValue": "string",
                                    "justification": "RIGHT"
                                }
                            ]
                        },
                        "barcoded": {
                            "symbology": "UCC128",
                            "specification": {
                                "zoneNumber": 0,
                                "header": "string",
                                "dataField": "string",
                                "literalValue": "string",
                                "justification": "RIGHT"
                            }
                        }
                    }
                },
                "printedLabelOrigin": {
                    "address": {
                        "streetLines": [
                            "10 FedEx Parkway",
                            "Suite 302"
                        ],
                        "city": "Beverly Hills",
                        "stateOrProvinceCode": "CA",
                        "postalCode": "38127",
                        "countryCode": "US",
                        "residential": 'false'
                    },
                    "contact": {
                        "personName": "person name",
                        "emailAddress": "email address",
                        "phoneNumber": "phone number",
                        "phoneExtension": "phone extension",
                        "companyName": "company name",
                        "faxNumber": "fax number"
                    }
                },
                "labelStockType": "PAPER_85X11_TOP_HALF_LABEL",
                "labelRotation": "UPSIDE_DOWN",
                "imageType": "PDF",
                "labelPrintingOrientation": "TOP_EDGE_OF_TEXT_FIRST",
                "returnedDispositionDetail": 'true'
            },
            "shippingDocumentSpecification": {
                "generalAgencyAgreementDetail": {
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    }
                },
                "returnInstructionsDetail": {
                    "customText": "This is additional text printed on Return instr",
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US\"",
                        "docType": "PNG"
                    }
                },
                "op900Detail": {
                    "customerImageUsages": [
                        {
                            "id": "IMAGE_5",
                            "type": "SIGNATURE",
                            "providedImageType": "LETTER_HEAD"
                        }
                    ],
                    "signatureName": "Signature Name",
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    }
                },
                "usmcaCertificationOfOriginDetail": {
                    "customerImageUsages": [
                        {
                            "id": "IMAGE_5",
                            "type": "SIGNATURE",
                            "providedImageType": "LETTER_HEAD"
                        }
                    ],
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    },
                    "certifierSpecification": "EXPORTER",
                    "importerSpecification": "UNKNOWN",
                    "producerSpecification": "SAME_AS_EXPORTER",
                    "producer": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": 'False'
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneExtension": "000",
                            "phoneNumber": "XXXX345671",
                            "companyName": "Fedex"
                        },
                        "accountNumber": {
                            "value": "Your account number"
                        },
                        "tins": [
                            {
                                "number": "123567",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00"
                            }
                        ]
                    },
                    "blanketPeriod": {
                        "begins": "22-01-2020",
                        "ends": "2-01-2020"
                    },
                    "certifierJobTitle": "Manager"
                },
                "usmcaCommercialInvoiceCertificationOfOriginDetail": {
                    "customerImageUsages": [
                        {
                            "id": "IMAGE_5",
                            "type": "SIGNATURE",
                            "providedImageType": "LETTER_HEAD"
                        }
                    ],
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    },
                    "certifierSpecification": "EXPORTER",
                    "importerSpecification": "UNKNOWN",
                    "producerSpecification": "SAME_AS_EXPORTER",
                    "producer": {
                        "address": {
                            "streetLines": [
                                "10 FedEx Parkway",
                                "Suite 302"
                            ],
                            "city": "Beverly Hills",
                            "stateOrProvinceCode": "CA",
                            "postalCode": "90210",
                            "countryCode": "US",
                            "residential": 'False'
                        },
                        "contact": {
                            "personName": "John Taylor",
                            "emailAddress": "sample@company.com",
                            "phoneExtension": "000",
                            "phoneNumber": "XXXX345671",
                            "companyName": "Fedex"
                        },
                        "accountNumber": {
                            "value": "Your account number"
                        },
                        "tins": [
                            {
                                "number": "123567",
                                "tinType": "FEDERAL",
                                "usage": "usage",
                                "effectiveDate": "2000-01-23T04:56:07.000+00:00",
                                "expirationDate": "2000-01-23T04:56:07.000+00:00"
                            }
                        ]
                    },
                    "certifierJobTitle": "Manager"
                },
                "shippingDocumentTypes": [
                    "RETURN_INSTRUCTIONS",
                    "DANGEROUS_GOODS_SHIPPERS_DECLARATION"
                ],
                "certificateOfOrigin": {
                    "customerImageUsages": [
                        {
                            "id": "IMAGE_5",
                            "type": "SIGNATURE",
                            "providedImageType": "LETTER_HEAD"
                        }
                    ],
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    }
                },
                "commercialInvoiceDetail": {
                    "customerImageUsages": [
                        {
                            "id": "IMAGE_5",
                            "type": "SIGNATURE",
                            "providedImageType": "LETTER_HEAD"
                        }
                    ],
                    "documentFormat": {
                        "provideInstructions": 'true',
                        "optionsRequested": {
                            "options": [
                                "SUPPRESS_ADDITIONAL_LANGUAGES",
                                "SHIPPING_LABEL_LAST"
                            ]
                        },
                        "stockType": "PAPER_LETTER",
                        "dispositions": [
                            {
                                "eMailDetail": {
                                    "eMailRecipients": [
                                        {
                                            "emailAddress": "email@fedex.com",
                                            "recipientType": "THIRD_PARTY"
                                        }
                                    ],
                                    "locale": "en_US",
                                    "grouping": "NONE"
                                },
                                "dispositionType": "CONFIRMED"
                            }
                        ],
                        "locale": "en_US",
                        "docType": "PDF"
                    }
                }
            },
            "rateRequestType": [
                "LIST",
                "PREFERRED"
            ],
            "preferredCurrency": "USD",
            "totalPackageCount": 25,
            "masterTrackingId": {
                "formId": "0201",
                "trackingIdType": "EXPRESS",
                "uspsApplicationId": "92",
                "trackingNumber": "49092000070120032835"
            },
            "requestedPackageLineItems": [
                {
                    "sequenceNumber": "1",
                    "subPackagingType": "BUCKET",
                    "customerReferences": [
                        {
                            "customerReferenceType": "INVOICE_NUMBER",
                            "value": "3686"
                        }
                    ],
                    "declaredValue": {
                        "amount": 12.45,
                        "currency": "USD"
                    },
                    "weight": {
                        "units": "KG",
                        "value": 68
                    },
                    "dimensions": {
                        "length": 100,
                        "width": 50,
                        "height": 30,
                        "units": "CM"
                    },
                    "groupPackageCount": 2,
                    "itemDescriptionForClearance": "description",
                    "contentRecord": [
                        {
                            "itemNumber": "2876",
                            "receivedQuantity": 256,
                            "description": "Description",
                            "partNumber": "456"
                        }
                    ],
                    "itemDescription": "item description for the package",
                    "variableHandlingChargeDetail": {
                        "rateType": "PREFERRED_CURRENCY",
                        "percentValue": 12.45,
                        "rateLevelType": "INDIVIDUAL_PACKAGE_RATE",
                        "fixedValue": {
                            "amount": 24.45,
                            "currency": "USD"
                        },
                        "rateElementBasis": "NET_CHARGE_EXCLUDING_TAXES"
                    },
                    "packageSpecialServices": {
                        "specialServiceTypes": [
                            "ALCOHOL",
                            "NON_STANDARD_CONTAINER"
                        ],
                        "signatureOptionType": "SERVICE_DEFAULT",
                        "priorityAlertDetail": {
                            "enhancementTypes": [
                                "PRIORITY_ALERT_PLUS"
                            ],
                            "content": [
                                "string"
                            ]
                        },
                        "signatureOptionDetail": {
                            "signatureReleaseNumber": "23456"
                        },
                        "alcoholDetail": {
                            "alcoholRecipientType": "string",
                            "shipperAgreementType": "Retailer"
                        },
                        "dangerousGoodsDetail": {
                            "cargoAircraftOnly": 'False',
                            "accessibility": "INACCESSIBLE",
                            "options": [
                                "LIMITED_QUANTITIES_COMMODITIES",
                                "ORM_D"
                            ]
                        },
                        "packageCODDetail": {
                            "codCollectionAmount": {
                                "amount": 12.45,
                                "currency": "USD"
                            }
                        },
                        "pieceCountVerificationBoxCount": 0,
                        "batteryDetails": [
                            {
                                "batteryPackingType": "CONTAINED_IN_EQUIPMENT",
                                "batteryRegulatoryType": "IATA_SECTION_II",
                                "batteryMaterialType": "LITHIUM_METAL"
                            }
                        ],
                        "dryIceWeight": {
                            "units": "KG",
                            "value": 68
                        }
                    }
                }
            ]
        },
        "labelResponseOptions": "LABEL",
        "accountNumber": {
            "value": "745379540"
        },
        "shipAction": "CONFIRM",
        "processingOptionType": "ALLOW_ASYNCHRONOUS",
        "oneLabelAtATime": 'true'
    }
    url = "https://apis-sandbox.fedex.com/ship/v1/shipments"

    # payload = input  # 'input' refers to JSON Payload
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_US",
        'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJDWFMiXSwiUGF5bG9hZCI6eyJjbGllbnRJZGVudGl0eSI6eyJjbGllbnRLZXkiOiJsN2E0ZjY5MmRkMWE0YjQwMDU4OWZkYWY2ZjQxN2NjOGUyIn0sImF1dGhlbnRpY2F0aW9uUmVhbG0iOiJDTUFDIiwiYWRkaXRpb25hbElkZW50aXR5Ijp7InRpbWVTdGFtcCI6IjI0LU1heS0yMDIyIDA4OjM1OjI0IEVTVCIsImFwaW1vZGUiOiJTYW5kYm94In0sInBlcnNvbmFUeXBlIjoiRGlyZWN0SW50ZWdyYXRvcl9CMkIifSwiZXhwIjoxNjUzNDAyOTI0LCJqdGkiOiJkNWM2NmEzZC1kYzQ3LTQ2YTktYTg0OC04ZTcxN2Q2NzAxMmIiLCJjbGllbnRfaWQiOiJsN2E0ZjY5MmRkMWE0YjQwMDU4OWZkYWY2ZjQxN2NjOGUyIn0.f5NslRPKsykbupWCoiv6vQzQqooFsNV7pj92A096i7tHyfYZdE09tBCx2-S6jgzuvF69eMvLZGTrwXHYwJdy16J8aIeYFU9VuI-bSc5YOBws5Z9CVEAHy5fRa6waOzJ7OofUiXshOftFZTbHC68PsE9tKY_wI_4CZAdfSPrdZsFIEuM-wyDRc-B-Ss2e7wbzhPIyHfdCvTUTOkkdT-Xo-v6W4mnt4M4neVleKQ3Pcv9rdtrLAwR8QOr2Ytc8L6jXz0z4E9aJonOQYvxH6TrDZSrUWk6Eq12MgV9ib0EJB0_tBPiB_SYAkMkvLXuz-nRo1W2Yb64ahvtM_1_yfFqaS0JDw1oshik2o52iOWi7rf5WNamwCnl1rZIwhlgGGUEyCwRRM2NVsVdigVaFIycHsDkALb0wS9e2Ec4gezSQX2SGBqhz7CCamUoyAFSFI9LCUaf23BYVKZJp3ojLolS7OuU01hvHDXXzKyxWhTdN2JHP9NQoCvLOJOXdOwhldhkq-SWTpGooAZuxkjJPVD2QgIZ1_sWzfMrEBv7ZHgcpGekBBn2zOKz-wjZkRdV3L2H3FN9lMbsSdm02uXUYFAUZs0Yr-bz1RmQCqpeP1ISVbVg-p2j6km9SIKb2DdzM4UWs66LXxWIqpGQvO5yRu6W7DZUd1XRYC9axMHJECe-bSK4",
        'api_key': 'l7a4f692dd1a4b400589fdaf6f417cc8e2',
        'secret_key': '3941c778053749089b74b942b40ee601',
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    return render(request, 'test.html')

# function for sending order to woocommerce
def create_orderToWcmrceStore(order_data):
    order = wcapi.post("orders", order_data).json()
    return True


# ###################### woocommerce store section starts ***********************
@login_required(login_url='/ap/register/updated')
def ap_fetch_woocommerce_store_prdct(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # updated new section *****************************

    page = 1  # The first page number to loop is page 1
    try:
        while True:
            prods = wcapi.get('products', params={"per_page": 50, "page": page})
            page += 1
            if prods.text:
                p = json.loads(prods.text)

                try:
                    for x in p:

                        # combining multiple categories of one product
                        cats = ''
                        for cat in x['categories']:
                            cats = cats + cat['name'] + ' ,'
                        # print(float(x['weight']))
                        # print(float(x['dimensions']['length']))
                        # print(float(x['dimensions']['width']))
                        # print(float(x['dimensions']['height']))
                        # print(cats)
                        if len(ProductList.objects.filter(product_id=x['id'])) <= 0:
                            product_list_model = ProductList.objects.create(
                                user=request.user,
                                product_id=x['id'],
                                product_type='wsp',
                                title=x['name'],
                                slug=x['slug'],
                                details=x['description'],
                                regular_price=x['regular_price'],
                                price=x['price'],
                                total_sold=x['total_sales'],
                                in_stock=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=cats,
                                product_weight=float(x['weight']),
                                product_length=x['dimensions']['length'],
                                product_width=x['dimensions']['width'],
                                product_height=x['dimensions']['height'],
                                subcat_id='1',
                                subcat_name='subcat_name',
                                security_policy='apcp',
                                return_policy='apcp',
                                delivery_policy='apcp'
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])
                                product_list_model.productImg.add(product_img_model)
                                product_list_model.save()

                        if len(WoocommerceProductList.objects.filter(product_id=x['id'])) <= 0:

                            woocomrc_prdct_list_model = WoocommerceProductList.objects.create(
                                product_id=x['id'],
                                name=x['name'],
                                slug=x['slug'],
                                description=x['description'],
                                price=x['price'],
                                regular_price=x['regular_price'],
                                total_sales=x['total_sales'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=x['categories'][0]['name'],
                                subcat_id='1',
                                subcat_name='subcat',
                                stock_status=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count'],
                                product_weight=x['weight'],
                                product_length=x['dimensions']['length'],
                                product_width=x['dimensions']['width'],
                                product_height=x['dimensions']['height']
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])

                                woocomrc_prdct_list_model.product_img.add(product_img_model)
                                woocomrc_prdct_list_model.save()

                except:

                    messages.warning(request, "Can't import products or server error! Try again!")
                    return redirect('apWoocommerceStoreList')
            if len(json.loads(prods.text)) <= 0:
                break
    except:
        return redirect('apWoocommerceStoreList')

    # ends new section *********************************

    return redirect('apWoocommerceStoreList')

@login_required(login_url='/ap/register/updated')
def ap_update_wocommerce_store_prdct(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    page = 1  # The first page number to loop is page 1
    while True:

        prods = wcapi.get('products', params={"per_page": 20, "page": page})
        page += 1
        if prods.text:
            products = json.loads(prods.text)
            try:
                for x in products:

                    # combining multiple categories of one product
                    cats = ''
                    for cat in x['categories']:
                        cats = cats + cat['name'] + ' ,'

                    if len(ProductList.objects.filter(product_id=x['id'])) > 0:
                        product_list_model = ProductList.objects.filter(product_id=x['id']).first()
                        if product_list_model.product_weight == '':
                            product_list_model.user = request.user
                            product_list_model.product_id = x['id']
                            product_list_model.product_type = 'wsp'
                            product_list_model.title = x['name']
                            product_list_model.slug = x['slug']
                            product_list_model.details = x['description']
                            product_list_model.regular_price = x['regular_price']
                            product_list_model.price = x['price']
                            product_list_model.total_sold = x['total_sales']
                            product_list_model.in_stock = x['stock_status']
                            product_list_model.avrg_rating = x['average_rating']
                            product_list_model.rating_count = x['rating_count']
                            product_list_model.cat_id = x['categories'][0]['id']
                            product_list_model.cat_name = cats
                            product_list_model.subcat_id = '1'
                            product_list_model.subcat_name = 'subcat_name'
                            product_list_model.security_policy = 'apcp'
                            product_list_model.return_policy = 'apcp'
                            product_list_model.delivery_policy = 'apcp'

                            product_list_model.product_weight = float(x['weight'])
                            product_list_model.product_length = float(x['dimensions']['length'])
                            product_list_model.product_width = float(x['dimensions']['width'])
                            product_list_model.product_height = float(x['dimensions']['height'])
                            product_list_model.save()

                        # for img in x['images']:
                        #     old_product_imgs = ProductImg.objects.filter(product_id=x['id'])
                        #     if old_product_imgs:
                        #         for img in old_product_imgs:
                        #             if img.img:
                        #                 fs = FileSystemStorage()
                        #                 fs.delete(img.img.name)
                        #             img.delete()
                        #     product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp', img_link=img['src'])
                        #     product_list_model.productImg.add(product_img_model)
                        #     product_list_model.save()

                    if len(WoocommerceProductList.objects.filter(product_id=x['id'])) > 0:
                        woocomrc_prdct_list_model = WoocommerceProductList.objects.filter(
                            product_id=x['id']).first()

                        woocomrc_prdct_list_model.product_id = x['id']
                        woocomrc_prdct_list_model.name = x['name']
                        woocomrc_prdct_list_model.slug = x['slug']
                        woocomrc_prdct_list_model.description = x['description']
                        woocomrc_prdct_list_model.price = x['price']
                        woocomrc_prdct_list_model.regular_price = x['regular_price']
                        woocomrc_prdct_list_model.total_sales = x['total_sales']
                        woocomrc_prdct_list_model.cat_id = x['categories'][0]['id']
                        woocomrc_prdct_list_model.cat_name = x['categories'][0]['name']
                        woocomrc_prdct_list_model.subcat_id = '1'
                        woocomrc_prdct_list_model.subcat_name = 'subcat'
                        woocomrc_prdct_list_model.stock_status = x['stock_status']
                        woocomrc_prdct_list_model.avrg_rating = x['average_rating']
                        woocomrc_prdct_list_model.rating_count = x['rating_count']

                        woocomrc_prdct_list_model.product_weight = float(x['weight'])
                        woocomrc_prdct_list_model.product_length = float(x['dimensions']['length'])
                        woocomrc_prdct_list_model.product_width = float(x['dimensions']['width'])
                        woocomrc_prdct_list_model.product_height = float(x['dimensions']['height'])
                        woocomrc_prdct_list_model.save()
            except:
                messages.success(request, "Product has been updated!")
                return redirect('apWoocommerceStoreList')
        if len(json.loads(prods.text)) <= 0:
            break

    return redirect('apWoocommerceStoreList')

@login_required(login_url='/ap/register/updated')
def ap_wcmrce_prdct_details(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()
        current_obj = WoocommerceProductList.objects.get(pk=pk)

        context = {
            'profile_pic' : profile_pic,
            'current_obj' : current_obj,
            'current_pk' : pk,
        }
        return render(request, 'backEnd_superAdmin/woocommerce_store/product_details.html', context)
    except:
        messages.warning(request, "Can't view the details! Try again!")
        return redirect('apWoocommerceStoreList')

    return render(request, 'backEnd_superAdmin/woocommerce_store/product_details.html')

@login_required(login_url='/ap/register/updated')
def ap_del_woocmmrce_prdct(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = WoocommerceProductList.objects.get(pk=pk)
        related_img_of_crnt_obj = ProductImg.objects.filter(product_id=current_obj.product_id)

        for obj in related_img_of_crnt_obj:
            obj.delete()
        current_obj.delete()
        messages.success(request, "Product has been deleted!")
        return redirect('apWoocommerceStoreList')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apWoocommerceStoreList')


    return redirect('apWoocommerceStoreList')

@login_required(login_url='/ap/register/updated')
def ap_woocommerce_store_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    woocomrce_product_list = WoocommerceProductList.objects.all()


    context = {
        'woocomrce_product_list' : woocomrce_product_list,
        'profile_pic' : profile_pic,
    }

    return render(request, "backEnd_superAdmin/woocommerce_store/woocommerce_store_prodct_list.html", context)

#*********************** Woocommerce section ends ***********************************************


# #######################order section ################################################
@login_required(login_url='/ap/register/updated')
def ap_current_orders(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_order_list = OrderList.objects.filter(Q(delivery_status=False) & Q(order_status='a') & Q(shipping_status=False))


    context = {
        'current_order_list' : current_order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/current_order.html', context)

@login_required(login_url='/ap/register/updated')
def ap_current_order_details(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_order = OrderList.objects.get(order_id=order_id)


    context = {
        'current_order' : current_order,
    }

    return render(request, 'backEnd_superAdmin/orders/current_order_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_set_crrnt_order_to_on_the_way(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # current order
    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        if current_order.order_status == 'a':
            current_order.shipping_status = True
            current_order.shipping_date = datetime.datetime.now()
            current_order.save()
            messages.success(request, 'Order status has been changed to "On The Way"!')
            return redirect('apCurrentOrderList')
        else:
            messages.warning(request, "Order is not approved yet!")
            return redirect('apCurrentOrderList')

    except:
        messages.warning(request, "Order status can't be changed! Try again!")
        return redirect('apCurrentOrderList')

    return redirect('apCurrentOrderList')


@login_required(login_url='/ap/register/updated')
def ap_cancel_order(request, order_id):


    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        current_order.order_status = 'c'
        current_order.shipping_status = False
        current_order.delivery_status= False
        current_order.save()
        messages.success(request, 'Order has been cancelled!')
        return redirect('apCurrentOrderList')
    except:
        messages.success(request, "Order status can't be cancelled! Try again!")
        return redirect('apCurrentOrderList')

    return redirect('apCurrentOrderList')


@login_required(login_url='/ap/register/updated')
def ap_add_couponCode(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        discount_amount = request.POST.get('discount_amount')
        banner = request.FILES['coupon_banner']
        terms_conditions = request.POST.get('terms_conditions')

        if code and discount_amount and banner and terms_conditions and CouponCode.objects.filter(coupon_code=code).count() <= 0:
            coupon_code_model = CouponCode.objects.create(
                user=request.user,
                coupon_code=code,
                discount_amnt=int(discount_amount),
                coupon_banner=banner,
                terms_conditions=terms_conditions
            )
            messages.success(request, "Successfully added!")
            return redirect('apAddCouponoCode')
        else:
            messages.warning(request, "This coupon code already exists! Try with new one!")
            return redirect('apAddCouponoCode')

    return render(request, 'backEnd_superAdmin/coupon_code/add_coupon.html')


@login_required(login_url='/ap/register/updated')
def ap_update_couponCode(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # current obj
    current_obj = CouponCode.objects.filter(pk=pk).first()

    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        discount_amount = request.POST.get('discount_amount')
        terms_conditions = request.POST.get('terms_conditions')

        if code and discount_amount and terms_conditions:
            try:
                fs = FileSystemStorage()

                banner = request.FILES['coupon_banner']

                if banner:
                    # delete previous banner
                    fs.delete(current_obj.coupon_banner.name)

                    # update new informations
                    crnt_obj = CouponCode.objects.filter(pk=pk).first()
                    crnt_obj.coupon_code = code
                    crnt_obj.discount_amnt = discount_amount
                    crnt_obj.terms_conditions = terms_conditions
                    crnt_obj.coupon_banner = banner
                    crnt_obj.save()
                    messages.success(request, "Successfully updated!")
                    return redirect('apCouponCodeList')
            except:
                crnt_obj = CouponCode.objects.filter(pk=pk).first()
                crnt_obj.coupon_code = code
                crnt_obj.discount_amnt = discount_amount
                crnt_obj.terms_conditions = terms_conditions
                crnt_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apCouponCodeList')
        else:
            messages.warning(request, "Can't be updated!")
            return redirect('apCouponCodeList')

    context = {
        'current_obj': current_obj,
        'current_pk': pk,
    }
    return render(request, 'backEnd_superAdmin/coupon_code/update_coupon.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_couponCode(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()

        crnt_obj = CouponCode.objects.filter(pk=pk).first()
        fs.delete(crnt_obj.coupon_banner.name)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apCouponCodeList')

    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apCouponCodeList')

    return redirect('apCouponCodeList')

@login_required(login_url='/ap/register/updated')
def ap_couponCode_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # coupon code list
    coupon_code_list = CouponCode.objects.all()

    context = {
        'coupon_code_list': coupon_code_list,
    }

    return render(request, 'backEnd_superAdmin/coupon_code/coupon_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_activate_orDeactivate_couponCode(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        currnt_obj = CouponCode.objects.filter(pk=pk).first()

        if currnt_obj.status:
            currnt_obj.status = False
            currnt_obj.save()
        else:
            currnt_obj.status = True
            currnt_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apCouponCodeList')
    except:
        messages.warning(request, "Can't be activated!")
        return redirect('apCouponCodeList')

    return redirect('apCouponCodeList')

# on the way ******************
@login_required(login_url='/ap/register/updated')
def ap_on_the_way_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # order list which already shipped for delivery

    order_list = OrderList.objects.filter(Q(order_status='a') & Q(delivery_status=False) & Q(shipping_status=True))

    context = {
        'order_list' : order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/on_the_way.html', context)

@login_required(login_url='/ap/register/updated')
def ap_set_to_delivered(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        if current_order.order_status == 'a' and current_order.delivery_status == False and current_order.shipping_status == True:
            current_order.delivery_status = True
            current_order.delivery_date = datetime.datetime.now()
            current_order.save()
            messages.success(request, "Order status has been changed to 'Delivered' !")
            return redirect('apOnTheWayOrderList')
        else:
            messages.warning(request, "Order status can't be changed! Check 'Order Status/Delivery Status/Shipping Status'!")
            return redirect('apOnTheWayOrderList')
    except:
        messages.warning(request,"Order not found! Try again!")
        return redirect('apOnTheWayOrderList')

    return redirect('apOnTheWayOrderList')


@login_required(login_url='/ap/register/updated')
def ap_delivered_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    order_list = OrderList.objects.filter(Q(delivery_status=True) & Q(shipping_status=True) & Q(order_status='a'))

    context = {
        'delivered_ordered_list' : order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/delivered.html', context)


@login_required(login_url='/ap/register/updated')
def ap_cancelled_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    cancelled_order_list = OrderList.objects.filter(order_status='c')

    context = {
        'cancelled_order_list': cancelled_order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/cancelled.html', context)

# *********************************** ends order section *********************************************

# user profile setting section *****************************************************************
@login_required(login_url='/ap/register/updated')
def ap_update_user_profile_picture(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        profile_picture = request.FILES['profile_pic']

        if profile_picture:
            fs = FileSystemStorage()
            try:
                # checking existing profile picture
                user_profile_pic = UserProfilePicture.objects.get(user=request.user)
                if user_profile_pic:
                    fs.delete(user_profile_pic.pic.name)
                user_profile_pic.pic = profile_picture
                user_profile_pic.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)
            except:
                user_profile_pic = UserProfilePicture(user=request.user, pic=profile_picture)
                user_profile_pic.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_user_full_name(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        if fname and lname:
            try:
                user = Account.objects.get(email=request.user.email)
                user.fname = fname
                user.laname = lname
                user.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)
            except:
                messages.warning(request, "Can't be updated!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html')

@login_required(login_url='/ap/register/updated')
def ap_update_user_password(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')

        if email and username and old_pass:
            try:
                user = Account.objects.get(email=email)
                auth_user = authenticate(request, email=email, password=old_pass)

                if auth_user is not None:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, "Successfully updated!")
                    return redirect("apSuperAdminRegister")
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html')

# user profile setting section ends*****************************************************************

def ap_RegisterSuperUser(request):


    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmpass = request.POST['con_pass']


        if name and email and username and phone and password and confirmpass:
            if  len(Account.objects.filter(email=email)) <= 0 and len(Account.objects.filter(username=username)) <= 0 and len(Account.objects.filter(phone_no=phone)) <= 0:
                if password == confirmpass:
                    try:
                        user_account = Account.objects.create_superuser(email=email, username=username, phone_no=phone, password=password)
                        user_account.fname = name
                        user_account.status = '0'
                        user_account.is_active = False
                        user_account.save()

                        # # sending verification email with code*********************************
                        # verification__code = rand_num_gen(3)
                        #
                        # # save to verification code model by user
                        # verification_code_model = VerificationCode(user_email=email, code=verification__code)
                        # verification_code_model.save()

                        # request.session.flush()
                        # request.session['v_email'] = email
                        # request.session['v_code'] = verification__code
                        # request.session.set_expiry(300)

                        subject = f"Verification Link"
                        verification_url = f"Click to verify account: http://127.0.0.1:8000/user/account/veirfication/{username}/{phone}/"
                        html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                                                        context={'verification_url': verification_url})
                        email = EmailMessage(subject, html_content, to=[email])
                        email.content_subtype = 'html'
                        EmailThreading(email).start()
                        messages.success(request, "Verification link sent to your email!")
                        return redirect('apSuperAdminRegister')
                    except:
                        messages.warning(request, "Can't create account! Try again!")
                        return redirect('apSuperAdminRegister')
                    # ends sending verification email with code*************************

                else:
                    messages.warning(request, "Password didn't match! Try again!")
                    return redirect('apSuperAdminRegister')

    return render(request, 'backEnd_superAdmin/register.html')

def ap_loginSuperUser(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if email and username and password:
            try:
                user = Account.objects.get(email=email)
                try:
                    if user.status == '1' and user.is_active == True:
                        authenticate_user = authenticate(request, email=email, password=password)
                        if authenticate_user is not None:
                            login(request, authenticate_user)
                            return redirect('apHome')
                        else:
                            messages.warning(request, "You are not authenticated yet!")
                            return redirect('apSuperAdminRegister')
                    else:
                        messages.warning(request, "Please verify your account to acccess!")
                        return redirect('apSuperAdminRegister')
                except:
                    messages.warning(request, "User not found!")
                    return redirect('apSuperAdminRegister')
            except:
                messages.warning(request, 'Wrong username or email')
                return redirect('apSuperAdminRegister')

    return render(request, 'backEnd_superAdmin/log_in.html')


@login_required(login_url='/ap/register/updated')
def logoutSuperUser(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        logout(request)
        return redirect('apSuperAdminRegister')
    except:
        pass
    redirect('apSuperAdminRegister')


@login_required(login_url='/ap/register/updated')
def index(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    context = {
        'profile_pic': profile_pic
    }

    return render(request, 'backEnd_superAdmin/index.html', context)

@login_required(login_url='/ap/register/updated')
def home(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    user_list = Account.objects.all()

    # total orders
    total_number_of_orders = OrderList.objects.all().count()

    # total number of registered user
    total_registered_usr = Account.objects.all().count()

    # total number of products
    total_number_of_products = ProductList.objects.all().count()

    # unique visitors
    unique_visitors = VisitorInfo.objects.count()


    context = {
        'user_list' : user_list,
        'profile_pic' : profile_pic,
        'total_number_of_orders': total_number_of_orders,
        'total_registered_usr': total_registered_usr,
        'total_number_of_products': total_number_of_products,
        'unique_visitors': unique_visitors,
    }

    return render(request, 'backEnd_superAdmin/home.html', context)

@login_required(login_url='/ap/register/updated')
def deactivateUser(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.is_active = False
        current_user.save()
        messages.success(request, "User account has been deactivated!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')

@login_required(login_url='/ap/register/updated')
def activateUser(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.is_active = True
        current_user.save()
        messages.success(request, "User account has been activated!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')

@login_required(login_url='/ap/register/updated')
def removeUser(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.delete()
        messages.success(request, "User account has been removed!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')


@login_required(login_url='/ap/register/updated')
def ap_add_product_category(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        name = request.POST['cat__name']

        if name and len(ProductCategory.objects.filter(name=name)) <= 0:
            product_cat_model = ProductCategory(name=name)
            product_cat_model.save()
            messages.success(request, 'Successfully added!')
            return redirect('apAddProductCategory')
        else:
            messages.success(request, 'Category name already exists!')
            return redirect('apAddProductCategory')

    # product category list
    product_cats_list = ProductCategory.objects.all()

    context = {
        'product_cats_list' : product_cats_list,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product_cat/add_product_category.html', context)


# product cateory section*******************************************************

@login_required(login_url='/ap/register/updated')
def ap_edit_product_category(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST['name']
        if name and len(ProductCategory.objects.filter(name=name)) <= 0:
            product_cat_model = ProductCategory.objects.get(pk=pk)
            product_cat_model.name = name
            product_cat_model.save()
            messages.success(request, 'Successfully updated!')
            return redirect('apAddProductCategory')
        else:
            messages.success(request, 'Category name already exists!')
            return redirect('apAddProductCategory')

    return redirect('apAddProductCategory')

@login_required(login_url='/ap/register/updated')
def ap_del_product_category(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        category = ProductCategory.objects.get(pk=pk)
        category.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddProductCategory')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddProductCategory')

    return redirect('apAddProductCategory')


# product sub-category section*******************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_product_subcat(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        name = request.POST['subcat__name']
        if name and len(ProductSubCategory.objects.filter(name=name)) <= 0:

            product_cat_model = ProductCategory.objects.get(pk=pk)
            product_subcat_model = ProductSubCategory(category=product_cat_model, name=name)
            product_subcat_model.save()

            messages.success(request, 'Successfully added!')
            return redirect('apAddSubcategory', pk=pk)
        else:
            messages.warning(request, 'Category name already exists!')
            return redirect('apAddSubcategory', pk=pk)

    # product sub-category list
    product_subcat_list = ProductSubCategory.objects.filter(category=pk)

    context = {
        'cat_pk': pk,
        'product_subcat_list' : product_subcat_list,
        'profile_pic' : profile_pic,
    }
    return render(request, 'backEnd_superAdmin/product_cat/product_subcategory.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_product_subcat(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_obj = ProductSubCategory.objects.get(pk=pk)

    try:
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddSubcategory', pk=current_obj.category.pk)
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddSubcategory', pk=current_obj.category.pk)

    return redirect('apAddSubcategory', pk=current_obj.category.pk)

# add custom product section updated************************************************
@login_required(login_url='/ap/register/updated')
def ap_all_products(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # product list
    product_list = ProductList.objects.all()

    context = {
        'product_list' : product_list,
    }

    return render(request, 'backEnd_superAdmin/product/all_products.html', context)


# package section starts ****************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_new_packageName(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST.get('new_package_name')

        if name and PackageNameList.objects.filter(name=name).count() <= 0:
            package_name_list_model = PackageNameList.objects.create(name=name.capitalize())
            messages.success(request, "Successfully added new package name!")
            return redirect('apAddNewPackageName')
        else:
            messages.warning(request, "Can't be added new package! Try again!")
            return redirect('apAddNewPackageName')

    # package name list
    package_name_list = PackageNameList.objects.all()

    context = {
        'package_name_list': package_name_list,
    }

    return render(request, 'backEnd_superAdmin/membership_package/add_package_name.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_new_packageName(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    curnt_package_name = get_object_or_404(PackageNameList, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('new_package_name')

        if name:
            curnt_package_name.name = name
            curnt_package_name.save()
            messages.success(request, "Package name successfully updated!")
            return redirect('apAddNewPackageName')
        else:
            messages.warning(request, "Package name Can't be updated! Try again!")
            return redirect('apAddNewPackageName')

    context = {
        'curnt_package_name': curnt_package_name,
    }

    return render(request, 'backEnd_superAdmin/membership_package/update_package_name.html', context)


@login_required(login_url='/ap/register/updated')
def ap_remove_packageName(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = get_object_or_404(PackageNameList, pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddNewPackageName')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddNewPackageName')

    return redirect('apAddNewPackageName')

@login_required(login_url='/ap/register/updated')
def ap_add_packageFeatureOptions(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        option = request.POST.get('add_packge_options')

        if option and PackageOptions.objects.filter(option=option.capitalize()).count() <= 0:
            package_option_model = PackageOptions.objects.create(option=option.capitalize())
            messages.success(request, "Successfully added!")
            return redirect('apAddPackageFeatureOptions')
        else:
            messages.warning(request, "Can't be added! This option already exists!")
            return redirect('apAddPackageFeatureOptions')

    # existing package feature options
    existing_package_features = PackageOptions.objects.all()

    context = {
        'existing_package_features': existing_package_features,
    }

    return render(request, 'backEnd_superAdmin/membership_package/add_package_options.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_packageFeatureOptions(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    package_option_model = get_object_or_404(PackageOptions, pk=pk)

    if request.method == 'POST':
        option = request.POST.get('package_option')

        if option and PackageOptions.objects.filter(option=option.capitalize()).count() <= 0:
            package_option_model.option = option.capitalize()
            package_option_model.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddPackageFeatureOptions')
        else:
            messages.warning(request, "Can't be updated! This option already exists!")
            return redirect('apAddPackageFeatureOptions')

    context = {
        'package_option_model': package_option_model,
    }

    return render(request, 'backEnd_superAdmin/membership_package/update_package_options.html', context)


@login_required(login_url='/ap/register/updated')
def ap_remove_packageFeatureOption(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = get_object_or_404(PackageOptions, pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddPackageFeatureOptions')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddPackageFeatureOptions')

    return redirect('apAddPackageFeatureOptions')

@login_required(login_url='/ap/register/updated')
def ap_add_package(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # existing package name list
    package_names = PackageNameList.objects.all()

    # existing package feature options
    package_feature_options = PackageOptions.objects.all()

    # existing products
    products = ProductList.objects.all()

    if request.method == 'POST':
        name_id = request.POST.get('package_name')
        package_price = request.POST.get('package_price')
        package_old_price = request.POST.get('package_old_price')
        package_products = request.POST.getlist('package_products')
        package_options = request.POST.getlist('package_options')

        if name_id and package_price and package_products and package_options:
            package_uniqe_id = get_random_string(15)

            package_name = get_object_or_404(PackageNameList, pk=name_id)
            package_list_model = PackageList.objects.create(
                package_id=package_uniqe_id,
                name=package_name,
                price=package_price,
                old_price=package_old_price,
            )
            for id in package_products:
                product = get_object_or_404(ProductList, pk=id)
                package_list_model.products.add(product)
                package_list_model.save()
            for id in package_options:
                option = get_object_or_404(PackageOptions, pk=id)
                package_list_model.options.add(option)
                package_list_model.save()
            messages.success(request, "New package has been added successfully!")
            return redirect('apAddPackage')
        else:
            messages.warning(request, "New package can't be added! Try again!")
            return redirect('apAddPackage')

    # existing package list
    current_package_list = PackageList.objects.all()

    context = {
        'package_names': package_names,
        'package_feature_options': package_feature_options,
        'products': products,
        'current_package_list': current_package_list,
    }

    return render(request, 'backEnd_superAdmin/membership_package/add_package.html', context)

@login_required(login_url='/ap/register/updated')
def ap_activate_package(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = get_object_or_404(PackageList, pk=pk)
        activate_status(request, crnt_obj) # from congi.active_deactivate_status.py fiile
        return redirect('apAddPackage')
    except:
        messages.warning(request, "Can't be activated! Try again later!")
        return redirect('apAddPackage')

    return redirect('apAddPackage')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_package(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = get_object_or_404(PackageList, pk=pk)
        deactivate_status(request, crnt_obj)# from congi.active_deactivate_status.py fiile
        return redirect('apAddPackage')
    except:
        messages.warning(request, "Can't be de-activated! Try again later!")
        return redirect('apAddPackage')

    return redirect('apAddPackage')

@login_required(login_url='/ap/register/updated')
def ap_update_package(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # existing package name list
    package_names = PackageNameList.objects.all()

    # existing package feature options
    package_feature_options = PackageOptions.objects.all()

    # existing products
    products = ProductList.objects.all()

    # current package
    current_package = get_object_or_404(PackageList, pk=pk)

    if request.method == 'POST':
        name_id = request.POST.get('package_name')
        package_price = request.POST.get('package_price')
        package_old_price = request.POST.get('package_old_price')
        package_products = request.POST.getlist('package_products')
        package_options = request.POST.getlist('package_options')

        if name_id and package_price and package_products and package_options:

            current_package.package_name = get_object_or_404(PackageNameList, pk=name_id)
            current_package.price = package_price
            current_package.old_price = package_old_price
            current_package.save()

            # clearing previous objects
            current_package.products.clear()
            current_package.options.clear()

            for id in package_products:
                product = get_object_or_404(ProductList, pk=id)
                current_package.products.add(product)
                current_package.save()
            for id in package_options:
                option = get_object_or_404(PackageOptions, pk=id)
                current_package.options.add(option)
                current_package.save()
            messages.success(request, "Package has been updated successfully!")
            return redirect('apAddPackage')
        else:
            messages.warning(request, "Package can't be updated! Try again!")
            return redirect('apAddPackage')


    context = {
        'current_package': current_package,
        'package_names': package_names,
        'package_feature_options': package_feature_options,
        'products': products,
    }

    return render(request, 'backEnd_superAdmin/membership_package/update_package.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_package(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        curnt_obj = get_object_or_404(PackageList, pk=pk)
        delete_obj(request, curnt_obj)
        return redirect('apAddPackage')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddPackage')

    return redirect('apAddPackage')

# package part ends here ********************************************************************

@login_required(login_url='/ap/register/updated')
def ap_add_admin_custsom_product(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    product_cat = ProductCategory.objects.all()
    product_subcat = ProductSubCategory.objects.all()

    if request.method == 'GET':
        # getting current product category ajax request
        current_product_cat = request.GET.get('current_prodct_cat')

        # product subcategory by selected category
        subcat_of_current_cat = list(ProductSubCategory.objects.filter(category=current_product_cat).values())

        if request.is_ajax():
            return JsonResponse({'crrnt_product_subcat': subcat_of_current_cat})

    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST.get('sub_category')
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = float(request.POST['new_price'])
        old_price = float(request.POST['old_price'])
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        thumbnail_img = request.FILES['product__main__thumbnail__img']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']

        sponsor_status = request.POST.get('sponsor__status')

        product_id = uuid.uuid4()

        curnt_product_cat = ProductCategory.objects.filter(pk=category).first()

        curnt_product_subcat = None

        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()


        try:
            extra_imgs = request.FILES.getlist('product__extra__images')
            length_of_extra_imgs = len(extra_imgs)

            if length_of_extra_imgs >= 0:
                for img in extra_imgs:
                    product_img_model = ProductImg.objects.create(product_id=product_id, product_type='mcp', img=img)

                if policy == 'company':
                    # mcp stands for "My Custom Product
                    # apcp stands for "As Per Company Policy"
                    product_list_model = ProductList.objects.create(
                        product_id=product_id,
                        product_type='mcp',
                        user=request.user,
                        category=curnt_product_cat,
                        subcategory=curnt_product_subcat,
                        title=title,
                        brand_name=brand__name,
                        old_price=float(old_price),
                        new_price=float(new_price),
                        short_des=short_des,
                        details=details,
                        product_thumbnail=thumbnail_img,
                        use_case=use_cases,
                        benefits=benefits,
                        security_policy='apcp',
                        return_policy='apcp',
                        delivery_policy='apcp',
                        store_name=store__name,
                        store_link=store_link,
                        about_store=about_store,
                        in_stock=in_stock,
                        policy_followed=policy,
                        sponsor_status=sponsor_status
                    )
                    product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                    if product_extra_img_list:
                        for img in product_extra_img_list:
                            product_list_model.productImg.add(img)
                            product_list_model.save()

                if policy == 'own':
                    product_list_model = ProductList.objects.create(
                        product_id=product_id,
                        product_type='mcp',
                        user=request.user,
                        category=curnt_product_cat,
                        subcategory=curnt_product_subcat,
                        title=title,
                        brand_name=brand__name,
                        old_price=old_price,
                        new_price=new_price,
                        short_des=short_des,
                        details=details,
                        product_thumbnail=thumbnail_img,
                        use_case=use_cases,
                        benefits=benefits,
                        security_policy=security_policy,
                        return_policy=return_policy,
                        delivery_policy=delivery_policy,
                        store_name=store__name,
                        store_link=store_link,
                        about_store=about_store,
                        in_stock=in_stock,
                        policy_followed=policy,
                        sponsor_status=sponsor_status
                    )
                    product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                    if product_extra_img_list:
                        for img in product_extra_img_list:
                            product_list_model.productImg.add(img)
                            product_list_model.save()

                # saving to Game sponsored product list
                if sponsor_status == 'yes':
                    spnsored_prdct = ProductList.objects.get(product_id=product_id)
                    sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                    sponsord_prdct_for_game.save()

                messages.success(request, "Successfully added!")
                return redirect('apAddAdminCustomProduct')

        except:
            if policy == 'company':
                product_list_model = ProductList.objects.create(
                    product_id=product_id,
                    product_type='mcp',
                    user=request.user,
                    category=curnt_product_cat,
                    subcategory=curnt_product_subcat,
                    title=title,
                    brand_name=brand__name,
                    old_price=float(old_price),
                    new_price=float(new_price),
                    short_des=short_des,
                    details=details,
                    product_thumbnail=thumbnail_img,
                    use_case=use_cases,
                    benefits=benefits,
                    security_policy='apcp', # apcp== As per company policy
                    return_policy='apcp',  # apcp== As per company policy
                    delivery_policy='apcp', # apcp== As per company policy
                    store_name=store__name,
                    store_link=store_link,
                    about_store=about_store,
                    in_stock=in_stock,
                    policy_followed=policy,
                    sponsor_status=sponsor_status
                )
                product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                if product_extra_img_list:
                    for img in product_extra_img_list:
                        product_list_model.productImg.add(img)
                        product_list_model.save()

            if policy == 'own':
                product_list_model = ProductList.objects.create(
                    product_id=product_id,
                    product_type='mcp',
                    user=request.user,
                    category=curnt_product_cat,
                    subcategory=curnt_product_subcat,
                    title=title,
                    brand_name=brand__name,
                    old_price=old_price,
                    new_price=new_price,
                    short_des=short_des,
                    details=details,
                    product_thumbnail=thumbnail_img,
                    use_case=use_cases,
                    benefits=benefits,
                    security_policy=security_policy,
                    return_policy=return_policy,
                    delivery_policy=delivery_policy,
                    store_name=store__name,
                    store_link=store_link,
                    about_store=about_store,
                    in_stock=in_stock,
                    policy_followed=policy,
                    sponsor_status=sponsor_status
                )
                product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                if product_extra_img_list:
                    for img in product_extra_img_list:
                        product_list_model.productImg.add(img)
                        product_list_model.save()

            # saving to Game sponsored product list
            if sponsor_status == 'yes':
                spnsored_prdct = ProductList.objects.get(product_id=product_id)
                sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                sponsord_prdct_for_game.save()

            messages.success(request, "Successfully added!")
            return redirect('apAddAdminCustomProduct')

    context = {
        'product_cat' : product_cat,
        'product_subcat' : product_subcat,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/add__product.html', context)


@login_required(login_url='/ap/register/updated')
def ap_admin_custom_product_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product list
    product_list = ProductList.objects.filter(Q(user=request.user) & Q(product_type='mcp'))

    context = {
        'product_list' : product_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/product_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_admin_custom_product_details(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # current obj
    current_product = ProductList.objects.get(pk=pk)

    context = {
        'current_pk' : pk,
        'current_prodct_id' : product_id,
        'current_product': current_product,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/product_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_admin_custom_product(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product category
    product_category = ProductCategory.objects.all()

    # product sub-cat
    product_subcat = ProductSubCategory.objects.all()


    # get current obj
    current_product_data = ProductList.objects.get(pk=pk)

    # current product's extra image obj
    # currnt_product_extra_img = ProductImg.objects.filter(product=current_product_data).first()

    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST.get('sub_category')
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = float(request.POST['new_price'])
        old_price = float(request.POST['old_price'])
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']
        sponsor_status = request.POST.get('sponsor__status')

        delete_old_images = request.POST.get('delete_old_images')

        curnt_product_cat = ProductCategory.objects.filter(pk=category).first()

        curnt_product_subcat = None
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()

        fs = FileSystemStorage()

        try:

            if delete_old_images == 'on':
                # grabing extra images of current object
                currnt_obj_extra_img_list = ProductImg.objects.filter(product_id=current_product_data.product_id)

                if currnt_obj_extra_img_list:
                    for img in currnt_obj_extra_img_list:
                        fs.delete(img.img.name)
                        img.delete()

            thumbnail_img = request.FILES['product__main__thumbnail__img']

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()
            if sponsor_status == 'yes' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            # deleting current thumbnail
            if thumbnail_img:
                fs.delete(current_product_data.product_thumbnail.name)

                extra_imgs = request.FILES.getlist('product__extra__images')
                length_of_extra_imgs = len(extra_imgs)
                if length_of_extra_imgs > 0:
                    for img in extra_imgs:
                        product_extra_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, product_type='mcp', img=img)
                        current_product_data.productImg.add(product_extra_img_model)
                        current_product_data.save()

                    if policy == 'company':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = 'apcp' # apcp== As per company policy
                        current_product_data.return_policy = 'apcp'
                        current_product_data.delivery_policy = 'apcp'
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    if policy == 'own':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    messages.success(request, "Successfully updated!")
                    return redirect('apAdminCustomProductList')

                else:
                    if policy == 'company':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = 'apcp' # apcp == As per company policy
                        current_product_data.return_policy = 'apcp'
                        current_product_data.delivery_policy = 'apcp'
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.title = title
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    messages.success(request, "Successfully updated!")
                    return redirect('apAdminCustomProductList')
        except:

            if delete_old_images == 'on':
                # grabing extra images of current object
                currnt_obj_extra_img_list = ProductImg.objects.filter(product_id=current_product_data.product_id)

                if currnt_obj_extra_img_list:
                    for img in currnt_obj_extra_img_list:
                        fs.delete(img.img.name)
                        img.delete()

            extra_imgs = request.FILES.getlist('product__extra__images')

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()

            if sponsor_status == 'yes' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            length_of_extra_imgs = len(extra_imgs)
            if length_of_extra_imgs > 0:

                for img in extra_imgs:
                    product_extra_img_model = ProductImg.objects.create(product_id=current_product_data.product_id,
                                                                        product_type='mcp', img=img)
                    current_product_data.productImg.add(product_extra_img_model)
                    current_product_data.save()

                if policy == 'company':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = 'apcp'
                    current_product_data.return_policy = 'apcp'
                    current_product_data.delivery_policy = 'apcp'
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAdminCustomProductList')
            else:
                if policy == 'company':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = 'apcp'
                    current_product_data.return_policy = 'apcp'
                    current_product_data.delivery_policy = 'apcp'
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAdminCustomProductList')


    context = {
        'current_pk' : pk,
        'current_product_id' : product_id,
        'current_product_data' : current_product_data,
        'product_category' : product_category,
        'product_subcategory' : product_subcat,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/update_product.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_admin_custom_product(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = ProductList.objects.get(pk=pk)

        fs = FileSystemStorage()
        # checking wheathe it has any extra images or not
        related_imgs_of_currnt_obj = ProductImg.objects.filter(product_id=current_obj.product_id)
        if related_imgs_of_currnt_obj:
            for img in related_imgs_of_currnt_obj:
                fs.delete(img.img.name)
                img.delete()


        # deleting product thumbnail obj
        fs.delete(current_obj.product_thumbnail.name)
        current_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAdminCustomProductList')
        redirect('apAdminCustomProductList')
    except:
        messages.warning(request, 'Can not be deleted! Try again!')
        return redirect('apAdminCustomProductList')
        redirect('apAdminCustomProductList')

    return redirect('apAdminCustomProductList')

@login_required(login_url='/ap/register/updated')
def ap__update_admin_wcmrce_product(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product category
    product_category = ProductCategory.objects.all()

    # product sub-cat
    product_subcat = ProductSubCategory.objects.all()


    # get current obj
    current_product_data = ProductList.objects.get(pk=pk)


    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST['sub_category']
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = request.POST['new_price']
        old_price = request.POST['old_price']
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']
        sponsor_status = request.POST.get('sponsor__status')

        delete_old_images = request.POST.get('delete_old_images')

        curnt_product_cat = None
        curnt_product_subcat = None

        if category:
            curnt_product_cat = ProductCategory.objects.filter(pk=category).first()
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()

        fs = FileSystemStorage()

        if delete_old_images:
            related_img_model = ProductImg.objects.filter(product_id=current_product_data.product_id)

            if related_img_model:
                for img in related_img_model:
                    if img.img:
                        fs.delete(img.img.name)
                        img.delete()

        try:
            thumbnail_img = request.FILES['product__main__thumbnail__img']

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()
            if sponsor_status == 'yes' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            # deleting current thumbnail
            if thumbnail_img:
                if current_product_data.product_thumbnail:
                    fs.delete(current_product_data.product_thumbnail.name)

                extra_imgs = request.FILES.getlist('product__extra__images')
                length_of_extra_imgs = len(extra_imgs)

                if length_of_extra_imgs > 0:

                    for img in extra_imgs:
                        related_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, img=img)
                        current_product_data.productImg.add(related_img_model)
                        current_product_data.save()

                    if policy == 'company':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()

                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = "apcp" # apcp == as per company policy
                        current_product_data.return_policy = "apcp"
                        current_product_data.delivery_policy = "apcp"
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == '':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    # check if there is any extra images exists for current product

                    messages.success(request, "Successfully updated!")
                    return redirect('apAllProductList')

                else:
                    if policy == 'company':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat

                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = "apcp"
                        current_product_data.return_policy = "apcp"
                        current_product_data.delivery_policy = "apcp"
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.title = title
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == '':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    messages.success(request, "Successfully updated!")
                    return redirect('apAllProductList')
        except:

            extra_imgs = request.FILES.getlist('product__extra__images')

            if extra_imgs:

                for img in extra_imgs:
                    related_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, img=img)
                    current_product_data.productImg.add(related_img_model)
                    current_product_data.save()

                # removing/saving product from sponsored product prize list if sponsored status is false
                if sponsor_status == 'no' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                    sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                    sponsored_product.delete()

                if sponsor_status == 'yes' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                    sponsored_product = SponsoredProductForPrize(product=current_product_data)
                    sponsored_product.save()

                length_of_extra_imgs = len(extra_imgs)

                if policy == 'company':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = "apcp"
                    current_product_data.return_policy = "apcp"
                    current_product_data.delivery_policy = "apcp"
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == '':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()

                messages.success(request, "Successfully updated!")
                return redirect('apAllProductList')
            else:
                # removing/saving product from sponsored product prize list if sponsored status is false
                if sponsor_status == 'no' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                    sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                    sponsored_product.delete()

                if sponsor_status == 'yes' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                    sponsored_product = SponsoredProductForPrize(product=current_product_data)
                    sponsored_product.save()

                if policy == 'company':

                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = "apcp"
                    current_product_data.return_policy = "apcp"
                    current_product_data.delivery_policy = "apcp"
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == '':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAllProductList')


    context = {
        'current_pk' : pk,
        'current_product_data' : current_product_data,
        'product_category' : product_category,
        'product_subcategory' : product_subcat,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/update_product.html', context)


# gaming section starts *****************************************************************

# deactivating other segments while activating one segments
def deactivate_other_game_setting(obj):
    for x in obj:
        if x.status:
            x.status = False
            x.save()
    return True

@login_required(login_url='/ap/register/updated')
def ap_game_settings(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # no_of_segments = request.POST.get('no_of_segments')
        no_spins = request.POST.get('no_spins')
        spin_duration = request.POST.get('spin_duration')
        config_status = request.POST.get('config_status')

        try:
            if config_status:
                # deactivating other segments while activating the current segment
                other_segment_obj = GameSetting.objects.all()
                thrding_deactivation_process = threading.Thread(target=deactivate_other_game_setting,
                                                                args=[other_segment_obj])
                thrding_deactivation_process.start()

                game_setting_model = GameSetting(
                    no_of_segments=5,
                    no_of_complt_spins=no_spins,
                    spining_duration=spin_duration,
                    status=config_status
                )
                game_setting_model.save()

                messages.success(request, "Successfully added!")
                return redirect('apGameSettings')
        except:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apGameSettings')

    # game setting list
    game_config_list = GameSetting.objects.all()

    context = {
        'game_config_list' : game_config_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/game/setting.html', context)


@login_required(login_url='/ap/register/updated')
def ap_activate_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()

        # deactivating other segments while activating the current segment
        other_segment_obj = GameSetting.objects.all().exclude(pk=pk)
        thrding_deactivation_process = threading.Thread(target=deactivate_other_game_setting, args=[other_segment_obj])
        thrding_deactivation_process.start()

        messages.success(request, "Successfully activated!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_deactivate_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()

        messages.success(request, "Successfully de-activated!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_update_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        current_obj = GameSetting.objects.get(pk=pk)

        if request.method == 'POST':
            # no_of_segments = request.POST.get('no_of_segments')
            no_spins = request.POST.get('no_spins')
            spin_duration = request.POST.get('spin_duration')
            config_status = request.POST.get('config_status')

            try:
                current_obj.no_of_segments = 5
                current_obj.no_of_complt_spins = no_spins
                current_obj.spining_duration = spin_duration
                current_obj.status = config_status
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apGameSettings')
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('apGameSettings')

        context = {
            'current_obj' : current_obj,
            'currnt_pk' : pk,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/update_game_segment.html', context)

    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apGameSettings')

    return render(request, 'backEnd_superAdmin/game/update_game_segment.html')

@login_required(login_url='/ap/register/updated')
def ap_delete_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_segment_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        game__setting = GameSetting.objects.get(status=True)

        segments_list = Segment.objects.all()

        sponsored_products = SponsoredProductForPrize.objects.filter(status=True)

        if request.method == 'POST':
            segment = request.POST.get('segment_name')
            bg_color = request.POST.get('bg_color')
            prize_title = request.POST.get('prize_title')
            segment_prize__type = request.POST.get('segment_prize__type')
            point_as_prize = request.POST.get('point_as_prize')
            product_as_prize = request.POST.get('product_as_prize')
            segment_status = request.POST.get('segment_status')
            segment_order = request.POST.get('segment_order')


            if segment and bg_color and segment_prize__type and segment_status and len(SegmentList.objects.filter(segment=Segment.objects.get(pk=segment))) <= 0:
                if segment_prize__type == 'product':
                    current_segment = Segment.objects.get(pk=segment)
                    current_prodct_as_prize = SponsoredProductForPrize.objects.get(pk=product_as_prize)

                    segment_list_model = SegmentList(
                        segment_no=segment_order,
                        segment=current_segment,
                        bg_color=bg_color,
                        prize_title=prize_title,
                        segment_prize_type='1',
                        product_as_prize=current_prodct_as_prize,
                        status=segment_status
                    )
                    segment_list_model.save()
                    messages.success(request, "Succesfully added!")
                    return redirect('apSegmentSettings')
                if segment_prize__type == 'point':
                    current_segment = Segment.objects.get(pk=segment)

                    segment_list_model = SegmentList(
                        segment_no=segment_order,
                        segment=current_segment,
                        bg_color=bg_color,
                        prize_title=prize_title,
                        segment_prize_type='2',
                        prize_point_amount=point_as_prize,
                        status=segment_status
                    )
                    segment_list_model.save()
                    messages.success(request, "Succesfully added!")
                    return redirect('apSegmentSettings')

            else:
                messages.warning(request, "This segment already exists!")
                return redirect('apSegmentSettings')

        segment_list_with_prizes = SegmentList.objects.all()

        context = {
            'segments': segments_list,
            'sponsored_products' : sponsored_products,
            'game__setting' : game__setting,
            'segment_list_with_prizes': segment_list_with_prizes,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/segment_setting.html', context)
    except:
        messages.warning(request, "Number of segment is not specified. Please complete game setting or activate game configuration!")
        return redirect('apGameSettings')

    return render(request, 'backEnd_superAdmin/game/segment_setting.html')

@login_required(login_url='/ap/register/updated')
def ap_activate__segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "This segment has been activated!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "This segment can't be activated! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')

@login_required(login_url='/ap/register/updated')
def ap_deactivate__segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "This segment has been de-activated!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "This segment can't be de-activated! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')


@login_required(login_url='/ap/register/updated')
def ap_update_segment_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        current_obj = SegmentList.objects.get(pk=pk)

        segments_list = Segment.objects.all()

        sponsored_products = SponsoredProductForPrize.objects.all()

        if request.method == 'POST':
            segment = request.POST.get('segment_name')
            bg_color = request.POST.get('bg_color')
            prize_title = request.POST.get('prize_title')
            segment_prize__type = request.POST.get('segment_prize__type')
            point_as_prize = request.POST.get('point_as_prize')
            product_as_prize = request.POST.get('product_as_prize')
            segment_status = request.POST.get('segment_status')
            segment_order = request.POST.get('segment_order')

            if segment and bg_color and segment_prize__type and segment_status:
                if segment_prize__type == 'product':
                    current_segment = Segment.objects.get(pk=segment)
                    current_prodct_as_prize = SponsoredProductForPrize.objects.get(pk=product_as_prize)

                    segment_list_model = SegmentList.objects.get(pk=pk)
                    segment_list_model.segment_no=segment_order
                    segment_list_model.segment=current_segment
                    segment_list_model.bg_color=bg_color
                    segment_list_model.segment_prize_type='1'
                    segment_list_model.product_as_prize=current_prodct_as_prize
                    segment_list_model.status=segment_status
                    segment_list_model.prize_title = prize_title
                    segment_list_model.save()

                    messages.success(request, "Succesfully updated!")
                    return redirect('apSegmentSettings')

                if segment_prize__type == 'point':
                    current_segment = Segment.objects.get(pk=segment)

                    segment_list_model = SegmentList.objects.get(pk=pk)
                    segment_list_model.segment_no = segment_order
                    segment_list_model.segment=current_segment
                    segment_list_model.bg_color=bg_color
                    segment_list_model.segment_prize_type='2'
                    segment_list_model.prize_point_amount=point_as_prize
                    segment_list_model.status=segment_status
                    segment_list_model.prize_title = prize_title
                    segment_list_model.save()

                    messages.success(request, "Succesfully updated!")
                    return redirect('apSegmentSettings')

        context = {
            'segments': segments_list,
            'sponsored_products': sponsored_products,
            'current_obj' : current_obj,
            'current_pk': pk,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/update_segment_setting.html', context)
    except:
        pass

    return render(request, 'backEnd_superAdmin/game/update_segment_setting.html')


@login_required(login_url='/ap/register/updated')
def ap_del_segment_setting(request,pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')

@login_required(login_url='/ap/register/updated')
def ap_sponsored_prdacts_for_game(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    sponsored_product_list = SponsoredProductForPrize.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'sponsored_product_list' : sponsored_product_list,
    }

    return render(request, 'backEnd_superAdmin/game/sponsored_prdct_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_add_new_segment(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST.get('segment_name')

        print(name)

        if name and len(Segment.objects.filter(name=name)) <= 0:
            segment_model = Segment.objects.create(name=name)
            messages.success(request, "Successfully added!")
            return redirect('apAddNewSegment')
        else:
            messages.warning(request, "Can't be added!")
            return redirect('apAddNewSegment')

    # segments list
    segments_list = Segment.objects.all()

    context = {
        'segments_list': segments_list,
    }

    return render(request, 'backEnd_superAdmin/game/add_segment.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_new_segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = Segment.objects.filter(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddNewSegment')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddNewSegment')

    return redirect('apAddNewSegment')

# add game terms and policies
@login_required(login_url='/ap/register/updated')
def ap_add_terms_policies_forGame(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        game_terms_policies = request.POST.get('game_terms_policies')

        if game_terms_policies and GameTermsPolicies.objects.filter().count() <= 0:
            gameTermsPolicies = GameTermsPolicies.objects.create(terms=game_terms_policies)
            messages.success(request, "Successfully added!")
            return redirect('apAddTermsPoliciesForGame')
        else:
            messages.warning(request, "Can't be added! Terms & policies already exist! Update it or delete it!")
            return redirect('apAddTermsPoliciesForGame')

    # existing terms and policies
    existing_terms_policies = GameTermsPolicies.objects.filter().first()

    context = {
        'existing_terms_policies': existing_terms_policies,
    }

    return render(request, 'backEnd_superAdmin/game/terms_policies.html', context)


# update game terms and policies
@login_required(login_url='/ap/register/updated')
def ap_update_terms_policies_forGame(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        game_terms_policies = request.POST.get('game_terms_policies')

        if game_terms_policies:
            gameTermsPolicies = GameTermsPolicies.objects.get(pk=pk)
            gameTermsPolicies.terms = game_terms_policies
            gameTermsPolicies.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddTermsPoliciesForGame')
        else:
            messages.warning(request, "Can't be updated!")
            return redirect('apAddTermsPoliciesForGame')

    # existing terms and policies
    existing_terms_policies = GameTermsPolicies.objects.filter().first()

    context = {
        'existing_terms_policies': existing_terms_policies,
        'current_pk': pk,
    }

    return render(request, 'backEnd_superAdmin/game/update_game_terms_policies.html', context)


@login_required(login_url='/ap/register/updated')
def ap_delete_terms_policies_forGame(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameTermsPolicies.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddTermsPoliciesForGame')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddTermsPoliciesForGame')

    return redirect('apAddTermsPoliciesForGame')

# deactivate other sponsored product for winning chance
# def deactivateOtherProductFor_winning_chance(obj):
#
#     if obj:
#         for x in obj:
#             x.status = False
#             x.save()
#     return True

@login_required(login_url='/ap/register/updated')
def ap_activate_spnsored_prdct_for_game(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.status = True
        current_obj.prodct_id = get_random_string(8)
        current_obj.save()

        # threading de-activation process
        # other_active_products = SponsoredProductForPrize.objects.filter(status=True).exclude(pk=pk)
        # de_activate_other_prdcts = threading.Thread(target=deactivateOtherProductFor_winning_chance, args=[other_active_products])
        # de_activate_other_prdcts.start()

        messages.success(request, "This product has been activated for game to win!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "This item can't be activated! Try again!")
        return redirect('apGameSponsoredProducts')
    return redirect('apGameSponsoredProducts')


@login_required(login_url='/ap/register/updated')
def ap_deactivate_sponsord_prdct_for_game(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()

        messages.success(request, "This product has been de-activated for game to win!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "This item can't be de-activated! Try again!")
        return redirect('apGameSponsoredProducts')

    return redirect('apGameSponsoredProducts')

@login_required(login_url='/ap/register/updated')
def ap_del_sponsored_product(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apGameSponsoredProducts')

    return redirect('apGameSponsoredProducts')


# add applicable rules for prize winner
@login_required(login_url='/ap/register/updated')
def ap_applicable_rules_for_prize_winner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # sponsored product list
    sponsored_product_list = SponsoredProductForPrize.objects.all()

    if request.method == 'POST':
        product_pk = request.POST.get('product')
        rules = request.POST.get('applicable_rules')

        if product_pk and rules:
            product = SponsoredProductForPrize.objects.filter(pk=product_pk).first()
            applicable_rules_model = ApplicableRulesForWinner.objects.create(user=request.user, product=product, applicable_rules=rules)
            messages.success(request, "Successfully added!")
            return redirect('apApplicableRuleWinningPrize')

        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apApplicableRuleWinningPrize')

    # product list with applicable rules
    product_list_with_app_rules = ApplicableRulesForWinner.objects.all()

    context = {
        'sponsored_product_list': sponsored_product_list,
        'product_list_with_app_rules' : product_list_with_app_rules,
    }

    return render(request, 'backEnd_superAdmin/game/applicable_rules_setting_for_winner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_remove_prduct_with_applicable_rules(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        product = ApplicableRulesForWinner.objects.get(pk=pk)
        product.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apApplicableRuleWinningPrize')
    except:
        messages.warning(request, "can't be deleted! Try again please!")
        return redirect('apApplicableRuleWinningPrize')

    return redirect('apApplicableRuleWinningPrize')
# gaming section starts ends *****************************************************************


# accounts section *********************************************************
@login_required(login_url='/ap/register/updated')
def ap_seller_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    seller_list = Account.objects.filter(Q(is_seller=True) & Q(status='1') & Q(is_active=True))
    context = {
        'profile_pic' : profile_pic,
        'seller_list' : seller_list,
    }

    return render(request, 'backEnd_superAdmin/accounts/seller_accounts_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_buyer_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    buyer_list = Account.objects.filter(Q(is_buyer=True) & Q(status='1') & Q(status='1') & Q(is_active=True))

    context = {
        'buyer_list': buyer_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/accounts/buyer_accounts_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_single_buyer_details(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_buyer = Account.objects.get(pk=pk)
        spin_point_wallet_of_crnt_usr = PointWallet.objects.filter(user=crnt_buyer).first()
        spin_credit_wallet_of_crnt_usr = CreditWallet.objects.filter(user=crnt_buyer).first()
        spin_token_wallet_of_crnt_usr = CreditWallet.objects.filter(user=crnt_buyer).first()
    except:
        messages.warning(request, "Shopper not found with current information!")
        return redirect('apBuyerAccountsList')

    context = {
        'crnt_buyer': crnt_buyer,
        'spin_point_wallet_of_crnt_usr': spin_point_wallet_of_crnt_usr,
        'spin_credit_wallet_of_crnt_usr': spin_credit_wallet_of_crnt_usr,
        'spin_token_wallet_of_crnt_usr': spin_token_wallet_of_crnt_usr,
    }

    return render(request, 'backEnd_superAdmin/accounts/single_buyer_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_buyer_account(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_accnt = Account.objects.get(pk=pk)
        crnt_accnt.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apBuyerAccountsList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apBuyerAccountsList')

    return redirect('apBuyerAccountsList')


@login_required(login_url='/ap/register/updated')
def ap_staff_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    staff_list = Account.objects.filter(Q(is_a_staff=True) & Q(status='1'))

    context = {
        'staff_list': staff_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/accounts/staff_accounts_list.html', context)

# settings section ************************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_site_logo(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        logo = request.FILES['logo']

        if logo and SiteLogo.objects.count() <= 0:
            logo_model = SiteLogo(logo=logo)
            logo_model.save()
            messages.success(request, "Successfully added!")
            return redirect('apAddSiteLogo')
        else:
            messages.warning(request, "Logo already exists! Delete existing one to add new logo!")
            return redirect('apAddSiteLogo')

    # existing logo
    existing_logo = SiteLogo.objects.filter().first()

    context = {
        'existing_logo': existing_logo,
    }

    return render(request, 'backEnd_superAdmin/site_setting/logo/add_logo.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_site_logo(request, pk):

    try:
        fs = FileSystemStorage()
        current_obj = SiteLogo.objects.get(pk=pk)
        fs.delete(current_obj.logo.name)

        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddSiteLogo')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddSiteLogo')

    return redirect('apAddSiteLogo')

# top footer section starts***********************************************************
@login_required(login_url='/ap/register/updated')
def ap_top_footer_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # free delivery setting
    free_delivery_setting = FreeDelivery.objects.filter().first()

    # safe payment
    safe_payment_setting = SafePayment.objects.filter().first()

    # free delivery setting
    shop_with_confidence = ShopWithConfidence.objects.filter().first()

    # safe payment
    help_center = HelpCenter.objects.filter().first()

    context = {
        'free_delivery_setting' : free_delivery_setting,
        'safe_payment_setting' : safe_payment_setting,
        'shop_with_confidence' : shop_with_confidence,
        'help_center' : help_center,
    }

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html', context)

@login_required(login_url='/ap/register/updated')
def ap_free_delivery_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and FreeDelivery.objects.count() <= 0:
            free_delivery_model = FreeDelivery.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_free_delivery_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = FreeDelivery.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

@login_required(login_url='/ap/register/updated')
def ap_add_safe_payment_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and SafePayment.objects.count() <= 0:
            safe_payment_model = SafePayment.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_safe_payment_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SafePayment.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

# jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
@login_required(login_url='/ap/register/updated')
def ap_shop_with_confident_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and ShopWithConfidence.objects.count() <= 0:
            shop_with_confident_model = ShopWithConfidence.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_shop_with_confident_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = ShopWithConfidence.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

@login_required(login_url='/ap/register/updated')
def ap_add_help_center_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and HelpCenter.objects.count() <= 0:
            help_model = HelpCenter.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_help_center_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HelpCenter.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

# top footer section ends************************************************************

@login_required(login_url='/ap/register/updated')
def ap_about_us(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        content = request.POST['about_us']

        try:
            if content and AboutUs.objects.count() == 0:
                about_us_model = AboutUs(about_us=content)
                about_us_model.save()
                messages.success(request, "Successfully added!")
                return redirect('apAboutUs')
            else:
                messages.warning(request, "Already exists! Try to edit or delete existing info!")
                return redirect('apAboutUs')
        except:
            messages.warning(request, "Already exists! Try to edit or delete existing info!")
            return redirect('apAboutUs')

    # about us content
    about_us_content = AboutUs.objects.filter().first()

    context = {
        'about_us': about_us_content,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/site_setting/about_us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_about_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = AboutUs.objects.get(pk=pk)
        obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAboutUs')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAboutUs')

    return redirect('apAboutUs')

@login_required(login_url='/ap/register/updated')
def ap_edit_about_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = AboutUs.objects.get(pk=pk)

    if request.method == 'POST':
        content = request.POST['about_us']

        try:
            if content:
                current_obj.about_us = content
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAboutUs')
            else:
                messages.warning(request, "Something wrong! Try again!")
                return redirect('apAboutUs')
        except:
            messages.warning(request, "Something wrong! Try again!")
            return redirect('apAboutUs')


    context = {
        'profile_pic' : profile_pic,
        'obj_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/site_setting/edit_about_us.html', context)

# contact us section ********************************************************
@login_required(login_url='/ap/register/updated')
def ap_contact_us(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        short_qoute = request.POST['short_qoute']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        mobile = request.POST['mobile']
        hotline = request.POST['hotline']
        email = request.POST['email']
        email2 = request.POST['email2']

        try:
            if short_qoute and address_line_1 and mobile and email and ContactUs.objects.count() == 0:
                contact_us_model = ContactUs(
                    short_qoute=short_qoute,
                    address_line_one=address_line_1,
                    address_line_two=address_line_2,
                    mobile=mobile,
                    hotline=hotline,
                    email_one=email,
                    email_two=email2
                )
                contact_us_model.save()
                messages.success(request, "Successfully added!")
                return redirect('apcontactUs')
            else:
                messages.warning(request, "Already exists! Try to edit or delete existing info!")
                return redirect('apcontactUs')
        except:
            messages.warning(request, "Already exists! Try to edit or delete existing info!")
            return redirect('apcontactUs')

    # about us content
    contact_us_obj = ContactUs.objects.filter().first()

    context = {
        'contact_us': contact_us_obj,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/site_setting/contact-us/contact-us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_edit_contact_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = ContactUs.objects.get(pk=pk)

    if request.method == 'POST':
        short_qoute = request.POST['short_qoute']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        mobile = request.POST['mobile']
        hotline = request.POST['hotline']
        email = request.POST['email']
        email2 = request.POST['email2']

        try:
            if short_qoute and address_line_1 and mobile and email:
                current_obj.short_qoute = short_qoute
                current_obj.address_line_one = address_line_1
                current_obj.address_line_two = address_line_2
                current_obj.mobile = mobile
                current_obj.hotline = hotline
                current_obj.email_one = email
                current_obj.email_two = email2
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apcontactUs')
            else:
                messages.warning(request, "Something wrong! Try again!")
                return redirect('apcontactUs')
        except:
            messages.warning(request, "Something wrong! Try again!")
            return redirect('apcontactUs')


    context = {
        'profile_pic' : profile_pic,
        'obj_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/site_setting/contact-us/edit_contact_us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_contact_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = ContactUs.objects.get(pk=pk)
        obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apcontactUs')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAboutUs')

    return redirect('apcontactUs')


# policy setting ***************************************************************

# beta test
@login_required(login_url='/ap/register/updated')
def ap_add_betaTest_termsConditions(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        content = request.POST.get('beta_test_termsConditions')

        if content and BetaTestTermsConditions.objects.filter().count() <= 0:
            betsTestTermsConditionsModel = BetaTestTermsConditions.objects.create(content=content)
            messages.success(request, "Successfully added!")
            return redirect('apAddBetaTestTermsConditions')
        else:
            messages.warning(request, "Terms & condition already exists! Delete it to add new one or update it!")
            return redirect('apAddBetaTestTermsConditions')

    # existing data
    existing_terms_condition = BetaTestTermsConditions.objects.filter().first()

    context = {
        'existing_terms_condition': existing_terms_condition,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/add_betaTest_termsCondition.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_betaTest_termsConditions(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # existing data
    existing_terms_condition = BetaTestTermsConditions.objects.filter(pk=pk).first()

    if request.method == 'POST':
        content = request.POST.get('beta_test_termsConditions')

        if content:
            existing_terms_condition.content = content
            existing_terms_condition.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddBetaTestTermsConditions')
        else:
            messages.warning(request, "Terms & condition can not be updated!")
            return redirect('apAddBetaTestTermsConditions')

    context = {
        'existing_terms_condition': existing_terms_condition,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_betaTestTermsCondition.html', context)

@login_required(login_url='/ap/register/updated')
def ap_removeBetaTestTermsCondition(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        existing_obj = BetaTestTermsConditions.objects.get(pk=pk)
        existing_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddBetaTestTermsConditions')
    except:
        messages.success(request, "Can't be  deleted! Try again!")
        return redirect('apAddBetaTestTermsConditions')

    return redirect('apAddBetaTestTermsConditions')

# members policy
@login_required(login_url='/ap/register/updated')
def ap_add_MembersPolicy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        content = request.POST.get('members_policy')

        if content and MembersPolicy.objects.filter().count() <= 0:
            membersPolicyModel = MembersPolicy.objects.create(content=content)
            messages.success(request, "Successfully added!")
            return redirect('apAddMembersPolicy')
        else:
            messages.warning(request, "Members already exists! Delete it to add new one or update it!")
            return redirect('apAddMembersPolicy')

    # existing data
    existing_membersPolicy = MembersPolicy.objects.filter().first()

    context = {
        'existing_membersPolicy': existing_membersPolicy,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/members/add_members.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_MembersPolicy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # existing data
    existing_member_policy = MembersPolicy.objects.filter(pk=pk).first()

    if request.method == 'POST':
        content = request.POST.get('members_policy')

        if content:
            existing_member_policy.content = content
            existing_member_policy.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddMembersPolicy')
        else:
            messages.warning(request, "Terms & condition can not be updated!")
            return redirect('apAddMembersPolicy')

    context = {
        'existing_member_policy': existing_member_policy,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/members/update_membersPolicy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_removeMembersPolicy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        existing_obj = MembersPolicy.objects.get(pk=pk)
        existing_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddMembersPolicy')
    except:
        messages.success(request, "Can't be  deleted! Try again!")
        return redirect('apAddMembersPolicy')

    return redirect('apAddMembersPolicy')

# shopper policy
@login_required(login_url='/ap/register/updated')
def ap_add_ShopperPolicy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        content = request.POST.get('shopper_policy')

        if content and ShopperPolicy.objects.filter().count() <= 0:
            shopperPolicyModel = ShopperPolicy.objects.create(content=content)
            messages.success(request, "Successfully added!")
            return redirect('apAddShopperPolicy')
        else:
            messages.warning(request, "Shopper policy already exists! Delete it to add new one or update it!")
            return redirect('apAddShopperPolicy')

    # existing data
    existing_shopperPolicy = ShopperPolicy.objects.filter().first()

    context = {
        'existing_shopperPolicy': existing_shopperPolicy,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/shoppers/add_shopper_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_ShopperPolicy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # existing data
    existing_shopper_policy = ShopperPolicy.objects.filter(pk=pk).first()

    if request.method == 'POST':
        content = request.POST.get('shopper_policy')

        if content:
            existing_shopper_policy.content = content
            existing_shopper_policy.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddShopperPolicy')
        else:
            messages.warning(request, "Shopper policy can not be updated!")
            return redirect('apAddShopperPolicy')

    context = {
        'existing_shopper_policy': existing_shopper_policy,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/shoppers/update_shopper_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_removeShopperPolicy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        existing_obj = ShopperPolicy.objects.get(pk=pk)
        existing_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddMembersPolicy')
    except:
        messages.success(request, "Can't be  deleted! Try again!")
        return redirect('apAddMembersPolicy')

    return redirect('apAddMembersPolicy')



@login_required(login_url='/ap/register/updated')
def ap_delivery_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        delivery_policy = request.POST['delivery_policy']

        try:
            if delivery_policy and DeliveryPolicy.objects.count() == 0:
                delvery_model = DeliveryPolicy(content=delivery_policy)
                delvery_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apDeliveryPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apDeliveryPolicy')

    # delivery policy list
    current_delivery_policy = DeliveryPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_delivery_policy' : current_delivery_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/delivery_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_delivery_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = DeliveryPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        delivery_policy = request.POST['delivery_policy']

        try:
            if delivery_policy:
                current_obj.content = delivery_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apDeliveryPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apDeliveryPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_delivery_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_delivery_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = DeliveryPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apDeliveryPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apDeliveryPolicy')

    return redirect('apDeliveryPolicy')


# return policy
@login_required(login_url='/ap/register/updated')
def ap_add_return_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        return_policy = request.POST['return_policy']

        try:
            if return_policy and ReturnPolicy.objects.count() == 0:
                return_model = ReturnPolicy(content=return_policy)
                return_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddReturnPolicy')
            else:
                messages.warning(request, 'Already exists! Try again!')
                return redirect('apAddReturnPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddReturnPolicy')

    # return policy list
    current_return_policy = ReturnPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_return_policy' : current_return_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/return_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_return_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = ReturnPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        return_policy = request.POST['return_policy']

        try:
            if return_policy:
                current_obj.content = return_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddReturnPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddReturnPolicy')

    context = {
        'profile_pic': profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_return_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_return_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = ReturnPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddReturnPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddReturnPolicy')

    return redirect('apAddReturnPolicy')


# product refund policy
@login_required(login_url='/ap/register/updated')
def ap_add_refund_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        refund_policy = request.POST['refund_policy']

        try:
            if refund_policy and RefundPolicy.objects.count() == 0:
                refund_policy_model = RefundPolicy(content=refund_policy)
                refund_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddRefundPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddRefundPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddRefundPolicy')

    # return policy list
    current_refund_policy = RefundPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_refund_policy' : current_refund_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/refund_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_refund_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = RefundPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        refund_policy = request.POST['refund_policy']

        try:
            if refund_policy:
                current_obj.content = refund_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddRefundPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddRefundPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_refund_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_refund_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = RefundPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddRefundPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddRefundPolicy')

    return redirect('apAddRefundPolicy')

# product security
@login_required(login_url='/ap/register/updated')
def ap_add_security_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        security_policy = request.POST['security_policy']

        try:
            if security_policy and SecurityPolicy.objects.count() == 0:
                security_policy_model = SecurityPolicy(content=security_policy)
                security_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddSecurityPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddSecurityPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddSecurityPolicy')

    # security policy list
    current_security_policy = SecurityPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_security_policy' : current_security_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/security_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_security_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = SecurityPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        security_policy = request.POST['security_policy']

        try:
            if security_policy:
                current_obj.content = security_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddSecurityPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddSecurityPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_security_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_security_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = SecurityPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddSecurityPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddSecurityPolicy')

    return redirect('apAddSecurityPolicy')


# terms & conditions policy
@login_required(login_url='/ap/register/updated')
def ap_add_termCondition_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        terms_condition_policy = request.POST['terms_condition_policy']

        try:
            if terms_condition_policy and TermsConditions.objects.count() == 0:
                terms_condition_policy_model = TermsConditions(content=terms_condition_policy)
                terms_condition_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddTermsConditionPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddTermsConditionPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddTermsConditionPolicy')

    # security policy list
    currnt_terms_condition_policy = TermsConditions.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_terms_condition_policy' : currnt_terms_condition_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/terms_condition.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_termCondition_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = TermsConditions.objects.get(pk=pk)

    if request.method == 'POST':
        terms_condition_policy = request.POST['terms_condition_policy']

        try:
            if terms_condition_policy:
                current_obj.content = terms_condition_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddTermsConditionPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddTermsConditionPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_terms_condition.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_termCondition_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = TermsConditions.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddTermsConditionPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddTermsConditionPolicy')

    return redirect('apAddTermsConditionPolicy')


# product privacy policy
@login_required(login_url='/ap/register/updated')
def ap_add_ProductPrivacy_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        product_privacy_policy = request.POST['product_privacy_policy']

        try:
            if product_privacy_policy and PrivacyPolicy.objects.count() == 0:
                product_privacy_policy_model = PrivacyPolicy(content=product_privacy_policy)
                product_privacy_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddProductPrivacyPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddProductPrivacyPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddProductPrivacyPolicy')

    # security policy list
    currnt_privacy_policy = PrivacyPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_privacy_policy' : currnt_privacy_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/add_product_privacy_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_ProductPrivacy_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = PrivacyPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        product_privacy_policy = request.POST['product_privacy_policy']

        try:
            if product_privacy_policy:
                current_obj.content = product_privacy_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddProductPrivacyPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddProductPrivacyPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_add_product_privacy_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_ProductPrivacy_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = PrivacyPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddProductPrivacyPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddProductPrivacyPolicy')

    return redirect('apAddProductPrivacyPolicy')


# cookie policy
@login_required(login_url='/ap/register/updated')
def ap_add_cookie_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        cookie_policy = request.POST['cookie_policy']

        try:
            if cookie_policy and CookiePolicy.objects.count() == 0:
                cookie_policy_model = CookiePolicy(content=cookie_policy)
                cookie_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddCookiePolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddCookiePolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddCookiePolicy')

    # security policy list
    currnt_cookie_policy = CookiePolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_cookie_policy' : currnt_cookie_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/add_cookie_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_cookie_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = CookiePolicy.objects.get(pk=pk)

    if request.method == 'POST':
        cookie_policy = request.POST['cookie_policy']

        try:
            if cookie_policy:
                current_obj.content = cookie_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddCookiePolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddCookiePolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_add_cookie_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_cookie_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = CookiePolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddCookiePolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddCookiePolicy')

    return redirect('apAddCookiePolicy')

# profile settings **************************************************************
@login_required(login_url='/ap/register/updated')
def ap_my_profile(request, username):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    context = {
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/profile/my-profile.html', context)


# banner section starts ******************************************************************

# Home page main banner
@login_required(login_url='/ap/register/updated')
def ap_add_banner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        offer_title = request.POST.get('offer_title')
        offer_title_amnt = request.POST.get('offer_title_amnt')
        offer_duration = request.POST.get('offer_duration')
        prduct_title = request.POST.get('prduct_title')
        price = request.POST.get('price')
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        if banner_img and url:
            banner_id = uuid.uuid4()

            banner_model = BannerList(
                banner_id=banner_id,
                user=request.user,
                offer_title=offer_title,
                offer_amount_or_title=offer_title_amnt,
                offer_duration=offer_duration,
                product_title=prduct_title,
                starting_price=price,
                img=banner_img,
                product_url=url
            )
            banner_model.save()
            messages.success(request, "New banner has been added successfully!")
            return redirect('apAddBanner')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/banner_section/add_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_banner(request, pk, banner_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_banner = BannerList.objects.get(pk=pk)

    if request.method == 'POST':
        offer_title = request.POST.get('offer_title')
        offer_title_amnt = request.POST.get('offer_title_amnt')
        offer_duration = request.POST.get('offer_duration')
        prduct_title = request.POST.get('prduct_title')
        price = request.POST.get('price')
        url = request.POST.get('url')

        try:
            fs = FileSystemStorage()
            banner_img = request.FILES['banner_img']

            if banner_img:
                # deleting current banner image
                fs.delete(current_banner.img.name)

                current_banner.offer_title = offer_title
                current_banner.offer_amount_or_title = offer_title_amnt
                current_banner.offer_duration = offer_duration
                current_banner.product_title = prduct_title
                current_banner.starting_price = price
                current_banner.img = banner_img
                current_banner.product_url = url
                current_banner.save()
                messages.success(request, "Successfully updated!")
                return redirect('apBannerList')
        except:
            current_banner.offer_title = offer_title
            current_banner.offer_amount_or_title = offer_title_amnt
            current_banner.offer_duration = offer_duration
            current_banner.product_title = prduct_title
            current_banner.starting_price = price
            current_banner.product_url = url
            current_banner.save()
            messages.success(request, "Successfully updated!")
            return redirect('apBannerList')
    context = {
        'profile_pic' : profile_pic,
        'current_banner': current_banner,
        'current_pk': pk,
        'banner_id': banner_id,
    }

    return render(request, 'backEnd_superAdmin/banner_section/update_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_banner_details(request, pk, banner_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_banner = BannerList.objects.get(pk=pk)

    context = {
        'profile_pic' : profile_pic,
        'current_banner': current_banner,
        'current_pk': pk,
        'banner_id': banner_id,
    }

    return render(request, 'backEnd_superAdmin/banner_section/banner_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    banner_list = BannerList.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'banner_list' : banner_list,
    }

    return render(request, 'backEnd_superAdmin/banner_section/banner_list.html', context)


# home page mini top banner
@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_topBanner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        bnr_id = uuid.uuid4()

        if banner_img and url:
            mini_top_bnr = HomeMiniTopBanner.objects.create(banner_id=bnr_id, user=request.user, img=banner_img, url=url)
            messages.success(request, "Successfully added!")
            return redirect('apAddHomePageMiniTopBanner')
        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apAddHomePageMiniTopBanner')

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/add_to_mini_top_slider.html')


@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_topBanrList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    home_top_bnr_list = HomeMiniTopBanner.objects.all()
    context = {
        'home_top_slider_list': home_top_bnr_list,
    }

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/mini_top_slider_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_activate_home_pageMini_topBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apHomePageMiniTopBannerList')

    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_home_pageMini_topBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "Successfully de-activated!")
        return redirect('apHomePageMiniTopBannerList')

    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')

@login_required(login_url='/ap/register/updated')
def ap_delete_home_pageMiniTopBanner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apHomePageMiniTopBannerList')
    except:
        messages.warning(request, "Can't deleted!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')


# home page mini bottom banner
@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_bottomBanner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        bnr_id = uuid.uuid4()

        if banner_img and url:
            mini_top_bnr = HomeMiniBottomBanner.objects.create(banner_id=bnr_id, user=request.user, img=banner_img, url=url)
            messages.success(request, "Successfully added!")
            return redirect('apAddHomePageMiniTopBanner')
        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apAddHomePageMiniTopBanner')

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/add_to_mini_bottom_slider.html')


@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_BottomBanrList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    home_bottom_bnr_list = HomeMiniBottomBanner.objects.all()

    context = {
        'home_bottom_bnr_list': home_bottom_bnr_list,
    }

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/mini_bottom_slider_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_activate_home_pageMini_BottomBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apHomePageMiniBottomBannerList')

    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')


@login_required(login_url='/ap/register/updated')
def ap_de_activate_home_pageMini_bottomBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "Successfully de-activated!")
        return redirect('apHomePageMiniBottomBannerList')

    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')

@login_required(login_url='/ap/register/updated')
def ap_delete_home_pageMiniBottomBanner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apHomePageMiniBottomBannerList')
    except:
        messages.warning(request, "Can't deleted!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')


@login_required(login_url='/ap/register/updated')
def ap_del_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = BannerList.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)

        current_obj.delete()
        messages.success(request, "Banner has been deleted!")
        return redirect('apBannerList')

    except:
        messages.warning(request, "Banner can't be deleted! Try again!")
        return redirect('apBannerList')

    return redirect('apBannerList')



# advertisement section *******************************************
@login_required(login_url='/ap/register/updated')
def ap_add_banner_at_prod_detail_page(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        if banner_img and url:
            banner_id = uuid.uuid4()

            banner_model = BannerProdDetail.objects.create(
                banner_id=banner_id,
                user=request.user,
                img=banner_img,
                link=url
            )
            messages.success(request, "New banner has been added successfully!")
            return redirect('apAddBnrProdDetialPg')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product_details_page_bannr/add_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_prod_details_pg_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    banner_list = BannerProdDetail.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'banner_list' : banner_list,
    }

    return render(request, 'backEnd_superAdmin/product_details_page_bannr/banner_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()
        banner = BannerProdDetail.objects.get(pk=pk)
        fs.delete(banner.img.name)
        banner.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apProductDetailsPgBnrList')
    return redirect('apProductDetailsPgBnrList')

def deactivate_product_detail_pg_bnr(banner_list):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    for banner in banner_list:
        banner.status = False
        banner.save()

    return True

@login_required(login_url='/ap/register/updated')
def ap_activate_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = BannerProdDetail.objects.get(pk=pk)

        other_banners = BannerProdDetail.objects.filter().exclude(pk=pk)
        banner.status = True
        banner.save()

        # theading deaactivate other banners
        thread = threading.Thread(target=deactivate_product_detail_pg_bnr, args=[other_banners])
        thread.start()

        messages.success(request, "Banner has been activated!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apProductDetailsPgBnrList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = BannerProdDetail.objects.get(pk=pk)
        banner.status = False
        banner.save()

        messages.success(request, "Banner has been de-activated!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be de-actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apProductDetailsPgBnrList')


# banner on shop page
@login_required(login_url='/ap/register/updated')
def ap_add_shop_page_banner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        banner_id = uuid.uuid4()

        if banner_img and url:
            shopPageBanner_model = ShopPageBanner.objects.create(banner_id=banner_id, user=request.user, img=banner_img, link=url)
            messages.success(request, "Successfully added new banner!")
            return redirect('apAddShopPageBanner')
        else:
            messages.warning(request, "Can't be added new banner! Try once again!")
            return redirect('apAddShopPageBanner')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/banner_shop_page/add_banner.html', context)

@login_required(login_url='/ap/register/updated')
def ap_shop_page_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    shop_page_banner_list = ShopPageBanner.objects.all()

    context = {
        'profile_pic': profile_pic,
        'shop_page_banner_list': shop_page_banner_list,
    }

    return render(request, 'backEnd_superAdmin/banner_shop_page/banner_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_delete_shop_page_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()
        current_obj = ShopPageBanner.objects.get(pk=pk)
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Banner has been successfully deleted!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apShopPageBannerList')

    return redirect('apShopPageBannerList')

def deactivate_shop_page_banner(banner_list):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    for banner in banner_list:
        banner.status = False
        banner.save()

    return True

@login_required(login_url='/ap/register/updated')
def ap_activate_shop_page_bannr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = ShopPageBanner.objects.get(pk=pk)

        other_banners = ShopPageBanner.objects.filter().exclude(pk=pk)
        banner.status = True
        banner.save()

        # theading deaactivate other banners
        thread = threading.Thread(target=deactivate_shop_page_banner, args=[other_banners])
        thread.start()

        messages.success(request, "Banner has been activated!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be actiavated! Try again!")
        return redirect('apShopPageBannerList')

    return redirect('apShopPageBannerList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_shop_page_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = ShopPageBanner.objects.get(pk=pk)
        banner.status = False
        banner.save()

        messages.success(request, "Banner has been de-activated!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be de-actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apShopPageBannerList')


@login_required(login_url='/ap/register/updated')
def ap_add_ads_toUser_profilePage(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product list
    product_list = ProductList.objects.all()

    if request.method == 'POST':
        ads_type = request.POST.get('ads_type')

        if ads_type == 'product':
            product_id = request.POST.get('product')
            if product_id:
                product = ProductList.objects.filter(product_id=product_id).first()
                usr_profile_ads_model = UserProfileAds.objects.create(user=request.user, ads_type=ads_type, product=product)
                messages.success(request, "Successfully added new banner!")
                return redirect('apAddAdsToUserProfilePg')
        else:
            banner_img = request.FILES['banner_img']
            usr_profile_ads_model = UserProfileAds.objects.create(user=request.user, ads_type=ads_type, banner_img=banner_img)
            messages.success(request, "Successfully added new banner!")
            return redirect('apAddAdsToUserProfilePg')

    context = {
        'profile_pic': profile_pic,
        'product_list': product_list,
    }

    return render(request, 'backEnd_superAdmin/profile_page_ads/add_ads.html', context)

@login_required(login_url='/ap/register/updated')
def ap_user_profile_ads_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # all ads in user profile page
    user_profile_page_ads = UserProfileAds.objects.all()

    context = {
        'user_profile_page_ads' : user_profile_page_ads,
    }

    return render(request, 'backEnd_superAdmin/profile_page_ads/ads_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_usr_profile_ads(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()
        current_obj = UserProfileAds.objects.get(pk=pk)

        if current_obj.ads_type == 'banner':
            fs.delete(current_obj.banner_img.name)
            current_obj.delete()
            messages.success(request, "Successfully deleted!")
            return redirect('apUserProfileAdsList')
        else:
            current_obj.delete()
            messages.success(request, "Successfully deleted!")
            return redirect('apUserProfileAdsList')
    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apUserProfileAdsList')

    return redirect('apUserProfileAdsList')

@login_required(login_url='/ap/register/updated')
def ap_activate_usr_profile_ads(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = UserProfileAds.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apUserProfileAdsList')
    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apUserProfileAdsList')

    return redirect('apUserProfileAdsList')


@login_required(login_url='/ap/register/updated')
def ap_deactivate_usr_profile_ads(request, pk):
    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = UserProfileAds.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "Successfully de-activated!")
        return redirect('apUserProfileAdsList')
    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apUserProfileAdsList')

    return redirect('apUserProfileAdsList')
# advertisement section ends ******************************************************************


@login_required(login_url='/ap/register/updated')
def ap_subscriber_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    subscriber_list = SubscriberList.objects.all()

    context = {
        'subscriber_list': subscriber_list,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/subscriber/subscriber_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_subscriber(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SubscriberList.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apSubscriberList')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apSubscriberList')

    return redirect('apSubscriberList')

@login_required(login_url='/ap/register/updated')
def ap_customer_msg_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    msg_list = CustomerMessageList.objects.all()

    context = {
        'profile_pic': profile_pic,
        'msg_list' : msg_list,
    }

    return render(request, 'backEnd_superAdmin/message_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_customer_msg(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        currn_obj = CustomerMessageList.objects.get(pk=pk)
        currn_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apCustomerMessageList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apCustomerMessageList')
    return redirect('apCustomerMessageList')

# membership rank part started ****************************************************
@login_required(login_url='/ap/register/updated')
def apAddNewMembershipRank(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        title = request.POST.get('title')
        earnings = request.POST.get('earnings')
        num_of_product = request.POST.get('num_of_product')

        if title and earnings and num_of_product and MemberShipRank.objects.filter(title__icontains=title.capitalize()).count() <= 0:
            rank_id = get_random_string(15)
            membership_rank_model = MemberShipRank.objects.create(
                rank_id= rank_id,
                title=title.capitalize(),
                total_earnings=earnings,
                number_of_prodct_need_to_sell=num_of_product,
            )
            messages.success(request, "Successfully added new membership rank!")
            return redirect('apAddNewMembershipRank')
        else:
            messages.warning(request, "Can't be added new membership rank! This rank already exists!")
            return redirect('apAddNewMembershipRank')

    # existing membership ranks
    existing_membership_ranks = MemberShipRank.objects.all()

    context = {
        'existing_membership_ranks': existing_membership_ranks,
    }

    return render(request, 'backEnd_superAdmin/membership_rank/add_membership_rank.html', context)

@login_required(login_url='/ap/register/updated')
def apUpdateMembershipRank(request, rank_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    crnt_obj = get_object_or_404(MemberShipRank, rank_id=rank_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        earnings = request.POST.get('earnings')
        num_of_product = request.POST.get('num_of_product')

        if title and earnings and num_of_product:
            crnt_obj.title=title.capitalize()
            crnt_obj.total_earnings=earnings
            crnt_obj.number_of_prodct_need_to_sell=num_of_product
            crnt_obj.save()
            messages.success(request, "Successfully update membership rank!")
            return redirect('apAddNewMembershipRank')
        else:
            messages.warning(request, "Can't be updated membership rank! Try again!")
            return redirect('apAddNewMembershipRank')

    context = {
        'crnt_obj': crnt_obj,
    }

    return render(request, 'backEnd_superAdmin/membership_rank/update_membership_rank.html', context)

@login_required(login_url='/ap/register/updated')
def apRemoveMembershipRank(request, rank_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = get_object_or_404(MemberShipRank, rank_id=rank_id)
        if crnt_obj:
            crnt_obj.delete()
            messages.success(request, "Successfully deleted!")
            return redirect('apAddNewMembershipRank')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddNewMembershipRank')

    return redirect('apAddNewMembershipRank')


@login_required(login_url='/ap/register/updated')
def apAddOfferProductsToDiffRankedMember(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # current membership ranks
    crnt_membership_ranks = MemberShipRank.objects.all()

    # product category
    product_all_cats = ProductCategory.objects.all()

    if request.method == 'GET':
        crnt_product_cat_id = request.GET.get('current_prodct_cat')

        crnt_product_cat = ProductCategory.objects.filter(pk=crnt_product_cat_id).first()

        if crnt_product_cat:
            crnt_products = ProductList.objects.filter(Q(category=crnt_product_cat) | Q(cat_name__icontains=crnt_product_cat.name))

            if crnt_products:
                crnt_product_list = list(crnt_products.values())
                if request.is_ajax():
                    return JsonResponse({'crnt_product_list': crnt_product_list})
            else:
                crnt_product_list = 0
                if request.is_ajax():
                    return JsonResponse({'crnt_product_list': crnt_product_list})

    if request.method == 'POST':
        rank_id = request.POST.get('rank')
        discount_ammount = request.POST.get('discount_ammount')
        product_category_id = request.POST.get('product_category')
        product_list = request.POST.getlist('product_list')

        if rank_id and discount_ammount and product_category_id and product_list:
            membership_rank = MemberShipRank.objects.filter(pk=rank_id).first()
            product_cat = ProductCategory.objects.filter(pk=product_category_id).first()

            if membership_rank and product_cat:

                # save all offered items together
                offeredItemsTogether = OfferedProductItemsByMembershipRank.objects.create(
                    membership_rank=membership_rank,
                    product_cat=product_cat,
                    discount_amount=int(discount_ammount),
                )

                for product_id in product_list:
                    product = ProductList.objects.filter(pk=product_id).first()

                    existing_offer = OfferedProductItemsByMembershipRank.objects.filter(product_cat=product_cat).first()
                    if existing_offer:
                        if product in existing_offer.product.all():
                            pass
                        else:
                            # update offered items together model
                            offeredItemsTogether.product.add(product)
                            offeredItemsTogether.save()

                            # saving to offered single product list based on membership rank
                            offeredSingleProductList = OfferedSingleProductBasedOnMembershipRank.objects.create(
                                membership_rank=membership_rank,
                                product_cat=product_cat,
                                product=product,
                                discount_amount=int(discount_ammount),
                            )

                messages.success(request, "Successfully added!")
                return redirect('apAddOfferToDiffRankedMembers')
            else:
                messages.warning(request, "Can't be added! Membership rank or product category may not found!")
                return redirect('apAddOfferToDiffRankedMembers')
        else:
            messages.warning(request, "Can't be added! Empty fields not allowed!")
            return redirect('apAddOfferToDiffRankedMembers')

    # existing offers
    existing_offers_by_membership = OfferedProductItemsByMembershipRank.objects.all()

    context = {
        'crnt_membership_ranks': crnt_membership_ranks,
        'product_all_cats': product_all_cats,
        'existing_offers_by_membership': existing_offers_by_membership,
    }

    return render(request, 'backEnd_superAdmin/membership_rank/offer_product.html', context)


@login_required(login_url='/ap/register/updated')
def apUpdateOfferProductsToDiffRankedMember(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # membership ranks
    crnt_membership_ranks = MemberShipRank.objects.all()

    # product cat list
    product_all_cats = ProductCategory.objects.all()

    # current obj
    current_obj = OfferedProductItemsByMembershipRank.objects.filter(pk=pk).first()

    crnt_cat_products = ProductList.objects.filter(Q(category=current_obj.product_cat) | Q(cat_name__icontains=current_obj.product_cat.name))

    if request.method == 'POST':
        rank_id = request.POST.get('rank')
        discount_ammount = request.POST.get('discount_ammount')
        product_category_id = request.POST.get('product_category')
        product_list = request.POST.getlist('product_list')

        if rank_id and discount_ammount and product_category_id and product_list:
            membership_rank = MemberShipRank.objects.filter(pk=rank_id).first()
            product_cat = ProductCategory.objects.filter(pk=product_category_id).first()

            if membership_rank and product_cat:

                # save all offered items together
                offeredItemsTogether = OfferedProductItemsByMembershipRank.objects.filter(pk=pk).first()
                offeredItemsTogether.membership_rank = membership_rank
                offeredItemsTogether.product_cat = product_cat
                offeredItemsTogether.discount_amount = int(discount_ammount)
                offeredItemsTogether.save()

                for product_id in product_list:
                    product = ProductList.objects.filter(pk=product_id).first()

                    # existing offer model
                    existing_offer = OfferedProductItemsByMembershipRank.objects.filter(product_cat=product_cat).first()
                    if existing_offer:
                        if product in existing_offer.product.all():
                            pass
                        else:
                            # update offered items together model
                            offeredItemsTogether.product.add(product)
                            offeredItemsTogether.save()

                            # saving to offered single product list based on membership rank
                            offeredSingleProductList = OfferedSingleProductBasedOnMembershipRank.objects.create(
                                membership_rank=membership_rank,
                                product_cat=product_cat,
                                product=product,
                                discount_amount=int(discount_ammount),
                            )

                messages.success(request, "Successfully added!")
                return redirect('apAddOfferToDiffRankedMembers')
            else:
                messages.warning(request, "Can't be added! Membership rank or product category may not found!")
                return redirect('apAddOfferToDiffRankedMembers')
        else:
            messages.warning(request, "Can't be added! Empty fields not allowed!")
            return redirect('apAddOfferToDiffRankedMembers')


    context = {
        'product_all_cats': product_all_cats,
        'current_obj': current_obj,
        'crnt_cat_products': crnt_cat_products,
        'crnt_membership_ranks': crnt_membership_ranks,
    }

    return render(request, 'backEnd_superAdmin/membership_rank/upate_offer_product.html', context)


@login_required(login_url='/ap/register/updated')
def apRemoveOfferProductToDifferentRankedMember(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # existing offer
    existing_offer = OfferedProductItemsByMembershipRank.objects.filter(pk=pk).first()
    if existing_offer:
        for p in existing_offer.product.all():
            offerSingleProductModel = OfferedSingleProductBasedOnMembershipRank.objects.filter(product=p).first()
            offerSingleProductModel.delete()
        existing_offer.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddOfferToDiffRankedMembers')
    else:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddOfferToDiffRankedMembers')

    return redirect('apAddOfferToDiffRankedMembers')

# analytics part starts**************************************************************
@login_required(login_url='/ap/register/updated')
def ap_unique_visitors_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    visitor_ip_address_list = VisitorInfo.objects.all()

    context = {
        'visitor_ip_address_list': visitor_ip_address_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/unique_users_info.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_visitor_from_uniqueVisitorList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj= VisitorInfo.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apUniqueVisitorsList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apUniqueVisitorsList')

    return redirect('apUniqueVisitorsList')


@login_required(login_url='/ap/register/updated')
def ap_registered_userList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # registered user list
    registrd_usr_list = Account.objects.filter(Q(is_seller=True) | Q(is_buyer=True) & Q(status='1') & Q(is_active=True))

    context = {
        'registrd_usr_list': registrd_usr_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/registered_usr_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_userFromUserList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_user = Account.objects.get(pk=pk)
        crnt_user.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apRegisteredUserList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apRegisteredUserList')

    return redirect('apRegisteredUserList')


@login_required(login_url='/ap/register/updated')
def ap_givenPointBonusHistory(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # calculating capthca bonus
    home_pg_captcha = CheckBoxCaptcha.objects.all()
    shop_pg_captcha = ShopCheckBoxCaptcha.objects.all()
    categoryShop_pg_captcha = CategoryShopCheckBoxCaptcha.objects.all()
    prodct_detals_pg_captcha = ProductDetailsCheckBoxCaptcha.objects.all()
    gameCheck_pg_captcha = GameCheckBoxCaptcha.objects.all()
    usrProfile_pg_captcha = UsrProfileCheckBoxCaptcha.objects.all()
    buyWinningChance_pg_captcha = BuyWinningChanceBoxCaptcha.objects.all()
    cart_pg_captcha = CartCheckBoxCaptcha.objects.all()
    contactUs_pg_captcha = ContactUsCheckBoxCaptcha.objects.all()
    paymentWinning_pg_captcha = PaymentWinningChnceCheckBoxCaptcha.objects.all()
    prodctPurchase_pg_captcha = ProductPurchaseCheckBoxCaptcha.objects.all()
    prdct_payment_success_pg_captcha = ProdctPaymntSccssCheckBoxCaptcha.objects.all()
    wishList_pg_captcha = WishlistCheckBoxCaptcha.objects.all()
    purchageCredit_pg_captcha = PurchaseCreditCheckBoxCaptcha.objects.all()
    credt_prchagePayment_pg_captcha = CreditPurchasePaymntCheckBoxCaptcha.objects.all()
    credt_prchaseSucccess_pg_captcha = CreditPurchaseSuccessCheckBoxCaptcha.objects.all()

    total_captha_bonus_objects = home_pg_captcha.count() + shop_pg_captcha.count() + categoryShop_pg_captcha.count() + prodct_detals_pg_captcha.count() + gameCheck_pg_captcha.count() + usrProfile_pg_captcha.count() + buyWinningChance_pg_captcha.count() + cart_pg_captcha.count() + contactUs_pg_captcha.count() + paymentWinning_pg_captcha.count() + prodctPurchase_pg_captcha.count() + prdct_payment_success_pg_captcha.count() + wishList_pg_captcha.count() + purchageCredit_pg_captcha.count() + credt_prchagePayment_pg_captcha.count() + credt_prchaseSucccess_pg_captcha.count()

    # total given bonus for solving captcha
    total_given_bonus_for_captcha_solving = total_captha_bonus_objects * 50

    # total daily sign in given bonus
    total_given_bonus_point_forDailySignIn = GivenDailySignInBonusUsrList.objects.count() * 50

    # total given bonus for registering account
    total_given_bonus_for_registering_accnt = BonusPoinForRegistration.objects.count() * 1000

    # total given bonus for refering people (per people is 250)
    total_given_bonus_for_refering_people = ReferalBonusList.objects.count() * 250

    # total given bonus for email invitation people (per people is 50)
    total_given_bonus_for_emailInvitation = EmailInvitationBonusUserList.objects.count() * 50

    # total given bonus
    total_given_bonus_point = total_given_bonus_for_captcha_solving + total_given_bonus_point_forDailySignIn + total_given_bonus_for_registering_accnt + total_given_bonus_for_refering_people + total_given_bonus_for_emailInvitation


    context = {
        'total_given_bonus_for_captcha_solving' : total_given_bonus_for_captcha_solving,
        'total_given_bonus_point_forDailySignIn' : total_given_bonus_point_forDailySignIn,
        'total_given_bonus_for_registering_accnt': total_given_bonus_for_registering_accnt,
        'total_given_bonus_for_refering_people': total_given_bonus_for_refering_people,
        'total_given_bonus_for_emailInvitation': total_given_bonus_for_emailInvitation,
        'total_given_bonus_point': total_given_bonus_point,
    }

    return render(request, 'backEnd_superAdmin/analytics/point_history/point_history_home.html', context)

# daily sign in bonus list
@login_required(login_url='/ap/register/updated')
def ap_dailySignInBonusUserList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # daily sign in bonus user list
    dailySignInBonusUserList = GivenDailySignInBonusUsrList.objects.all()

    context = {
        'dailySignInBonusUserList': dailySignInBonusUserList,
    }

    return render(request, 'backEnd_superAdmin/analytics/point_history/daily_signIn_bonus_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_removeDailySignInBonusUserList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = GivenDailySignInBonusUsrList.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apDailySignInBonusUserList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apDailySignInBonusUserList')

    return redirect('apDailySignInBonusUserList')

# registration bonus list
@login_required(login_url='/ap/register/updated')
def ap_registrationBonusUserList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # daily sign in bonus user list
    registrationBonusUserList = BonusPoinForRegistration.objects.all()

    context = {
        'registrationBonusUserList': registrationBonusUserList,
    }

    return render(request, 'backEnd_superAdmin/analytics/point_history/registration_bonus_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_registrationBonusUserList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = BonusPoinForRegistration.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_registrationBonusUserList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_registrationBonusUserList')

    return redirect('ap_registrationBonusUserList')

# referal bonus list
@login_required(login_url='/ap/register/updated')
def ap_referalBonusUserList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # daily sign in bonus user list
    referalBonusUserList = ReferalBonusList.objects.all()

    context = {
        'referalBonusUserList': referalBonusUserList,
    }

    return render(request, 'backEnd_superAdmin/analytics/point_history/referal_bonus_usr_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_referalBonusUserList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ReferalBonusList.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_referalBonusUserList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_referalBonusUserList')

    return redirect('ap_referalBonusUserList')


# email bonus list
@login_required(login_url='/ap/register/updated')
def ap_emailInvitationBonusUserList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # daily sign in bonus user list
    emailInvitationBonusUserList = EmailInvitationBonusUserList.objects.all()

    context = {
        'emailInvitationBonusUserList': emailInvitationBonusUserList,
    }

    return render(request, 'backEnd_superAdmin/analytics/point_history/email_invitation_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_emailInvitationBonusUserList(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = EmailInvitationBonusUserList.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_emailInvitationBonusUserList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_emailInvitationBonusUserList')

    return redirect('ap_emailInvitationBonusUserList')


# captcha part starts******************************************************

@login_required(login_url='/ap/register/updated')
def ap_all_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # calculating capthca bonus
    home_pg_captcha = CheckBoxCaptcha.objects.all()
    shop_pg_captcha = ShopCheckBoxCaptcha.objects.all()
    categoryShop_pg_captcha = CategoryShopCheckBoxCaptcha.objects.all()
    prodct_detals_pg_captcha = ProductDetailsCheckBoxCaptcha.objects.all()
    gameCheck_pg_captcha = GameCheckBoxCaptcha.objects.all()
    usrProfile_pg_captcha = UsrProfileCheckBoxCaptcha.objects.all()
    buyWinningChance_pg_captcha = BuyWinningChanceBoxCaptcha.objects.all()
    winChancePurchaseSccMsg_pg_captcha = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.all()
    cart_pg_captcha = CartCheckBoxCaptcha.objects.all()
    checkOut_pg_captcha = CheckoutCheckBoxCaptcha.objects.all()
    contactUs_pg_captcha = ContactUsCheckBoxCaptcha.objects.all()
    paymentWinning_pg_captcha = PaymentWinningChnceCheckBoxCaptcha.objects.all()
    prodctPurchase_pg_captcha = ProductPurchaseCheckBoxCaptcha.objects.all()
    prdct_payment_success_pg_captcha = ProdctPaymntSccssCheckBoxCaptcha.objects.all()
    wishList_pg_captcha = WishlistCheckBoxCaptcha.objects.all()
    purchageCredit_pg_captcha = PurchaseCreditCheckBoxCaptcha.objects.all()
    credt_prchagePayment_pg_captcha = CreditPurchasePaymntCheckBoxCaptcha.objects.all()
    credt_prchaseSucccess_pg_captcha = CreditPurchaseSuccessCheckBoxCaptcha.objects.all()

    total_captha_bonus_objects = home_pg_captcha.count() + shop_pg_captcha.count() + categoryShop_pg_captcha.count() + prodct_detals_pg_captcha.count() + gameCheck_pg_captcha.count() + usrProfile_pg_captcha.count() + buyWinningChance_pg_captcha.count() + cart_pg_captcha.count() + contactUs_pg_captcha.count() + paymentWinning_pg_captcha.count() + prodctPurchase_pg_captcha.count() + prdct_payment_success_pg_captcha.count() + wishList_pg_captcha.count() + purchageCredit_pg_captcha.count() + credt_prchagePayment_pg_captcha.count() + credt_prchaseSucccess_pg_captcha.count() + checkOut_pg_captcha.count() + winChancePurchaseSccMsg_pg_captcha.count()

    # total given bonus for solving captcha
    total_given_bonus_for_captcha_solving = total_captha_bonus_objects * 50

    context = {
        'home_pg_captcha': home_pg_captcha.count(),
        'shop_pg_captcha': shop_pg_captcha.count(),
        'categoryShop_pg_captcha': categoryShop_pg_captcha.count(),
        'prodct_detals_pg_captcha': prodct_detals_pg_captcha.count(),
        'gameCheck_pg_captcha': gameCheck_pg_captcha.count(),
        'usrProfile_pg_captcha': usrProfile_pg_captcha.count(),
        'buyWinningChance_pg_captcha': buyWinningChance_pg_captcha.count(),
        'cart_pg_captcha': cart_pg_captcha.count(),
        'contactUs_pg_captcha': contactUs_pg_captcha.count(),
        'paymentWinning_pg_captcha': paymentWinning_pg_captcha.count(),
        'prodctPurchase_pg_captcha': prodctPurchase_pg_captcha.count(),
        'prdct_payment_success_pg_captcha': prdct_payment_success_pg_captcha.count(),
        'wishList_pg_captcha': wishList_pg_captcha.count(),
        'purchageCredit_pg_captcha': purchageCredit_pg_captcha.count(),
        'credt_prchagePayment_pg_captcha': credt_prchagePayment_pg_captcha.count(),
        'credt_prchaseSucccess_pg_captcha': credt_prchaseSucccess_pg_captcha.count(),
        'checkout_pg_captcha': checkOut_pg_captcha.count(),
        'winChancePurchaseSccMsg_pg_captcha': winChancePurchaseSccMsg_pg_captcha.count(),
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/all_pages_with_captcha.html', context)

@login_required(login_url='/ap/register/updated')
def ap_home_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    home_pg_captcha_userList = CheckBoxCaptcha.objects.all()

    context = {
        'home_pg_captcha_userList': home_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/home_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_homePg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apHomePageCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apHomePageCaptchaBonusList')

    return redirect('apHomePageCaptchaBonusList')

# shop page by category
@login_required(login_url='/ap/register/updated')
def ap_shop_pgByCat_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    shopByCat_pg_captcha_userList = CategoryShopCheckBoxCaptcha.objects.all()

    context = {
        'shopByCat_pg_captcha_userList': shopByCat_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/shopPgByCat.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_shopPgByCat_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CategoryShopCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apShopPageByCatCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apShopPageByCatCaptchaBonusList')

    return redirect('apShopPageByCatCaptchaBonusList')

# shop page
@login_required(login_url='/ap/register/updated')
def ap_shop_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    shop_pg_captcha_userList = ShopCheckBoxCaptcha.objects.all()

    context = {
        'shop_pg_captcha_userList': shop_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/shop_page.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_shopPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ShopCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apShopPageCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apShopPageCaptchaBonusList')

    return redirect('apShopPageCaptchaBonusList')


# product details page
@login_required(login_url='/ap/register/updated')
def ap_productDetails_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    prodct_details_pg_captcha_userList = ProductDetailsCheckBoxCaptcha.objects.all()

    context = {
        'prodct_details_pg_captcha_userList': prodct_details_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/product_details_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_productDetails_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ProductDetailsCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apProductDetailsPageByCatCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apProductDetailsPageByCatCaptchaBonusList')

    return redirect('apProductDetailsPageByCatCaptchaBonusList')

# game details page
@login_required(login_url='/ap/register/updated')
def ap_game_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    game_pg_captcha_userList = GameCheckBoxCaptcha.objects.all()

    context = {
        'game_pg_captcha_userList': game_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/game_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_gamePg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = GameCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apGamePageByCatCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apGamePageByCatCaptchaBonusList')

    return redirect('apGamePageByCatCaptchaBonusList')


# user profile page
@login_required(login_url='/ap/register/updated')
def ap_userProfile_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    usrProfile_pg_captcha_userList = UsrProfileCheckBoxCaptcha.objects.all()

    context = {
        'usrProfile_pg_captcha_userList': usrProfile_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/usr_profile_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_userProfilePg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = UsrProfileCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apUserProfilePageCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apUserProfilePageCaptchaBonusList')

    return redirect('apUserProfilePageCaptchaBonusList')

# buy winning chance page
@login_required(login_url='/ap/register/updated')
def ap_buyWinningChance_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    buyWinningChance_pg_captcha_userList = BuyWinningChanceBoxCaptcha.objects.all()

    context = {
        'buyWinningChance_pg_captcha_userList': buyWinningChance_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/buy_winning_chance.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_buyWinningChance_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = BuyWinningChanceBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apBuyWinningChancePageCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apBuyWinningChancePageCaptchaBonusList')

    return redirect('apBuyWinningChancePageCaptchaBonusList')

# cart  page
@login_required(login_url='/ap/register/updated')
def ap_cart_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    cart_pg_captcha_userList = CartCheckBoxCaptcha.objects.all()

    context = {
        'cart_pg_captcha_userList': cart_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/cart_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_cartPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CartCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apCartPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apCartPgCaptchaBonusList')

    return redirect('apCartPgCaptchaBonusList')

# contact us  page
@login_required(login_url='/ap/register/updated')
def ap_contactUs_pg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    contactUs_pg_captcha_userList = ContactUsCheckBoxCaptcha.objects.all()

    context = {
        'contactUs_pg_captcha_userList': contactUs_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/contact_us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_contactUsPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ContactUsCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apContactUsPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apContactUsPgCaptchaBonusList')

    return redirect('apContactUsPgCaptchaBonusList')


# winning chance payment  page
@login_required(login_url='/ap/register/updated')
def ap_winning_chancePaymentPage_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    winningChancePayment_pg_captcha_userList = PaymentWinningChnceCheckBoxCaptcha.objects.all()

    context = {
        'winningChancePayment_pg_captcha_userList': winningChancePayment_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/winning_chance_payment_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_winning_chancePaymentPage_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = PaymentWinningChnceCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apWinningChancePaymentPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apWinningChancePaymentPgCaptchaBonusList')

    return redirect('apWinningChancePaymentPgCaptchaBonusList')

# product purchase  page
@login_required(login_url='/ap/register/updated')
def ap_productPurchasePage_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    productPurchase_pg_captcha_userList = ProductPurchaseCheckBoxCaptcha.objects.all()

    context = {
        'productPurchase_pg_captcha_userList': productPurchase_pg_captcha_userList,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/product_purchase_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_productPurchasePage_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ProductPurchaseCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apProductPurchasePgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apProductPurchasePgCaptchaBonusList')

    return redirect('apProductPurchasePgCaptchaBonusList')

# product payment success  page
@login_required(login_url='/ap/register/updated')
def ap_productPaymentSuccessPage_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    productPaymentSuccessPage = ProdctPaymntSccssCheckBoxCaptcha.objects.all()

    context = {
        'productPaymentSuccessPage': productPaymentSuccessPage,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/product_paymnt_succss_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_productPaymentSuccessPage_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ProdctPaymntSccssCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apProductPaymentSuccessPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apProductPaymentSuccessPgCaptchaBonusList')

    return redirect('apProductPaymentSuccessPgCaptchaBonusList')

# wishilist  page
@login_required(login_url='/ap/register/updated')
def ap_wishListPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    wishListPageCaptcha_list = WishlistCheckBoxCaptcha.objects.all()

    context = {
        'wishListPageCaptcha_list': wishListPageCaptcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/wishList.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_wishListPage_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = WishlistCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apWishListPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apWishListPgCaptchaBonusList')

    return redirect('apWishListPgCaptchaBonusList')

# wishilist  page
@login_required(login_url='/ap/register/updated')
def ap_wishListPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    wishListPageCaptcha_list = WishlistCheckBoxCaptcha.objects.all()

    context = {
        'wishListPageCaptcha_list': wishListPageCaptcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/wishList.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_wishListPage_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = WishlistCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apWishListPgCaptchaBonusList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apWishListPgCaptchaBonusList')

    return redirect('apWishListPgCaptchaBonusList')

# credit purchase  page
@login_required(login_url='/ap/register/updated')
def ap_creditPurchasePg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    creditPurchasePageCaptcha_list = PurchaseCreditCheckBoxCaptcha.objects.all()

    context = {
        'creditPurchasePageCaptcha_list': creditPurchasePageCaptcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/credit_prchase_pg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_creditPurchasePg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = PurchaseCreditCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_creditPurchasePg_captcha_bonus_list')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_creditPurchasePg_captcha_bonus_list')

    return redirect('ap_creditPurchasePg_captcha_bonus_list')

# credit purchase payment  page
@login_required(login_url='/ap/register/updated')
def ap_creditPurchasePaymntPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    creditPurchasePaymntPgCaptcha_list = CreditPurchasePaymntCheckBoxCaptcha.objects.all()

    context = {
        'creditPurchasePaymntPgCaptcha_list': creditPurchasePaymntPgCaptcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/creditPrchasePaymntPg.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_creditPurchasePaymntPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CreditPurchasePaymntCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_creditPurchasePaymntPg_captcha_bonus_list')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_creditPurchasePaymntPg_captcha_bonus_list')

    return redirect('ap_creditPurchasePaymntPg_captcha_bonus_list')

# credit purchase payment success  page
@login_required(login_url='/ap/register/updated')
def ap_creditPurchasePaymntSccssPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    credit_prchasePaymntSuccess = CreditPurchaseSuccessCheckBoxCaptcha.objects.all()

    context = {
        'credit_prchasePaymntSuccess': credit_prchasePaymntSuccess,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/credit_prchasePaymntSuccess.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_creditPurchasePaymntSccssPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CreditPurchaseSuccessCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_creditPurchasePaymntSccssPg_captcha_bonus_list')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_creditPurchasePaymntSccssPg_captcha_bonus_list')

    return redirect('ap_creditPurchasePaymntSccssPg_captcha_bonus_list')


# check out  page
@login_required(login_url='/ap/register/updated')
def ap_checkOutPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    checkout_pg_captcha_list = CheckoutCheckBoxCaptcha.objects.all()

    context = {
        'checkout_pg_captcha_list': checkout_pg_captcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/checkOut.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_checkOutPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = CheckoutCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_checkOutPg_captcha_bonus_list')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_checkOutPg_captcha_bonus_list')

    return redirect('ap_checkOutPg_captcha_bonus_list')


# winning chance purchase success out  page
@login_required(login_url='/ap/register/updated')
def ap_WinningChncePrchaseSuccessPg_captcha_bonus_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    winningChabcePrchaseSuccss_pg_captcha_list = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.all()

    context = {
        'winningChabcePrchaseSuccss_pg_captcha_list': winningChabcePrchaseSuccss_pg_captcha_list,
    }

    return render(request, 'backEnd_superAdmin/analytics/captcha/wnningChancePrchaseSuccess.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_WinningChncePrchaseSuccessPg_captcha_bonus(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('ap_WinningChncePrchaseSuccessPg_captcha_bonus_list')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('ap_WinningChncePrchaseSuccessPg_captcha_bonus_list')

    return redirect('ap_WinningChncePrchaseSuccessPg_captcha_bonus_list')



# analytics part ends**************************************************************

@login_required(login_url='/ap/register/updated')
def ap_add_how_spinit2Win_works(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        content = request.POST.get('how_spinitwin_works')

        if content and HowSpinIt2WinWorks.objects.all().count() <= 0:
            how_spinwin_works_model = HowSpinIt2WinWorks.objects.create(content=content)
            messages.success(request, "Successfully added!")
            return redirect('apAddHowSpin2winWorks')
        else:
            messages.warning(request, "Can't be added more than one object! Delete or update it!")
            return redirect('apAddHowSpin2winWorks')

    # existing data
    how_spin_win_works = HowSpinIt2WinWorks.objects.filter().first()

    context = {
        'how_spin_win_works': how_spin_win_works,
    }

    return render(request, 'backEnd_superAdmin/how_it_works/how_spinit2win_works.html', context)


@login_required(login_url='/ap/register/updated')
def ap_delete_how_spinit2Win_works(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = HowSpinIt2WinWorks.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddHowSpin2winWorks')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddHowSpin2winWorks')

    return redirect('apAddHowSpin2winWorks')

@login_required(login_url='/ap/register/updated')
def ap_update_how_spinit2Win_works(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_obj = HowSpinIt2WinWorks.objects.get(pk=pk)

    if request.method == 'POST':
        content = request.POST.get('how_spinitwin_works')

        if content:
            current_obj.content = content
            current_obj.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddHowSpin2winWorks')
        else:
            messages.warning(request, "Can't be updated! Try again!")
            return redirect('apAddHowSpin2winWorks')

    context = {
        'current_obj': current_obj,
    }

    return render(request, 'backEnd_superAdmin/how_it_works/update_how_spinit2win_works.html', context)


# shipping section starts*******************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_shippingClass(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST.get('className')
        cost = request.POST.get('cost')

        if name and cost and ShippingClass.objects.filter(name=name.capitalize()).count() <= 0:
            shippingClassId = get_random_string(12)
            shippingClassList = ShippingClass.objects.create(classID=shippingClassId, name=name.capitalize(), cost_rate=cost)
            messages.success(request, "Successfully added!")
            return redirect('apAddShippingClass')
        else:
            messages.warning(request, "Already exists! Try with new one!")
            return redirect('apAddShippingClass')

    # existing classes
    existing_shippingClassList = ShippingClass.objects.all()

    context = {
        'existing_shippingClassList': existing_shippingClassList,
    }

    return render(request, 'backEnd_superAdmin/shipping/add_shipping_class.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_shippingClass(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # current object
    shippingClassList = ShippingClass.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('className')
        cost = request.POST.get('cost')

        if name and cost and ShippingClass.objects.filter(name=name.capitalize()).count() <= 0:
            shippingClassList.name = name.capitalize()
            shippingClassList.cost_rate = cost
            shippingClassList.save()

            messages.success(request, "Successfully updated!")
            return redirect('apAddShippingClass')
        else:
            messages.warning(request, "Already exists! Try with new one!")
            return redirect('apAddShippingClass')

    context = {
        'shippingClassList': shippingClassList,
    }

    return render(request, 'backEnd_superAdmin/shipping/update_shipping_class.html', context)


@login_required(login_url='/ap/register/updated')
def ap_remove_shippingClass(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ShippingClass.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddShippingClass')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddShippingClass')

    return redirect('apAddShippingClass')


@login_required(login_url='/ap/register/updated')
def ap_productListByShippingClass(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_shippingClass = ShippingClass.objects.get(pk=pk)
        productsByShippingClass = ProductList.objects.filter(shipping_class=crnt_shippingClass)
    except:
        messages.warning(request, "No products found!")
        return redirect('apAddShippingClass')

    context = {
        'crnt_shippingClass': crnt_shippingClass,
        'productsByShippingClass': productsByShippingClass,
    }

    return render(request, 'backEnd_superAdmin/shipping/products_underShippingClass.html', context)

# product weight criteria
@login_required(login_url='/ap/register/updated')
def ap_add_productWeightCriteria(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        min_weight = request.POST.get('min_weight')
        max_weight = request.POST.get('max_weight')

        if min_weight and max_weight:
            id = get_random_string(15)
            productWeightCriteria = ProductWeightCriteria.objects.create(criteria_id=id, min_weight=min_weight, max_weight=max_weight)
            messages.success(request, "Successfully added!")
            return redirect('apAddProductWeightCriteria')
        else:
            messages.warning(request, "Can't be added!")
            return redirect('apAddProductWeightCriteria')

    # existing weight criteria
    existingProductWeightCriteria = ProductWeightCriteria.objects.all()

    context = {
        'existingProductWeightCriteria': existingProductWeightCriteria,
    }

    return render(request, 'backEnd_superAdmin/shipping/criteria/add_criteria.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_productWeightCriteria(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    crnt_productWeightCriteria = ProductWeightCriteria.objects.get(pk=pk)

    if request.method == 'POST':
        min_weight = request.POST.get('min_weight')
        max_weight = request.POST.get('max_weight')

        if min_weight and max_weight:
            crnt_productWeightCriteria.min_weight=min_weight
            crnt_productWeightCriteria.max_weight=max_weight
            crnt_productWeightCriteria.save()
            messages.success(request, "Successfully updated!")
            return redirect('apAddProductWeightCriteria')

        else:
            messages.warning(request, "Can't be updated!")
            return redirect('apAddProductWeightCriteria')

    context = {
        'crnt_productWeightCriteria': crnt_productWeightCriteria,
    }

    return render(request, 'backEnd_superAdmin/shipping/criteria/update_criteria.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_productWeightCriteria(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        crnt_obj = ProductWeightCriteria.objects.get(pk=pk)
        crnt_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddProductWeightCriteria')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddProductWeightCriteria')

    return redirect('apAddProductWeightCriteria')



@login_required(login_url='/ap/register/updated')
def ap_group_up_productsByShippingClass(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # all weight criteria
    all_weight_criteria = ProductWeightCriteria.objects.all()

    # all shipping class
    all_shipping_class = ShippingClass.objects.all()

    if request.method == 'GET':
        # selected criteria
        weight_criteria_id = request.GET.get('weight_criteria_id')

        # products id by selected criteria
        selectedProductsIDsByCriteria = request.GET.get('selectedProductsByCriteria')

        if weight_criteria_id and ProductWeightCriteria.objects.filter(pk=weight_criteria_id).first():
            crnt_product_criteria_obj = ProductWeightCriteria.objects.filter(pk=weight_criteria_id).first()
            min_weight_of_crnt_criteria = crnt_product_criteria_obj.min_weight
            max_weight_of_crnt_criteria = crnt_product_criteria_obj.max_weight

            # products with current min and max weight
            products = list(ProductList.objects.filter(Q(product_weight__gte=min_weight_of_crnt_criteria) & Q(product_weight__lt=max_weight_of_crnt_criteria) & Q(shipping_class__isnull=True)).values())

            if request.is_ajax():
                return JsonResponse({'products': products})

        if selectedProductsIDsByCriteria:
            crnt_selected_all_products_by_criteria = []
            selectedProductIDs_by_crnt_criteria = json.loads(selectedProductsIDsByCriteria)

            if selectedProductIDs_by_crnt_criteria:
                # converting current ids into int
                crnt_products_ids = [int(i) for i in selectedProductIDs_by_crnt_criteria]
                selected_products_by_crnt_criterias = list(ProductList.objects.filter(pk__in=crnt_products_ids).values())

                if request.is_ajax():
                    return JsonResponse({'crnt_selected_all_products_by_criteria': selected_products_by_crnt_criterias})


    context = {
        'all_shipping_class': all_shipping_class,
        'all_weight_criteria': all_weight_criteria,
    }

    return render(request, 'backEnd_superAdmin/shipping/group_up_products.html', context)

@login_required(login_url='/ap/register/updated')
def ap_updateGroupedProductsShippingClass(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        shippingClassId = request.POST.get('shippingClass')
        selected_productsIds_byCriteria = request.POST.getlist('selected_products_byCriteria')

        if shippingClassId and selected_productsIds_byCriteria:
            shipping__Class = ShippingClass.objects.filter(pk=shippingClassId).first()
            if selected_productsIds_byCriteria:
                for id in selected_productsIds_byCriteria:
                    crnt__product = ProductList.objects.filter(pk=id).first()
                    crnt__product.shipping_class = shipping__Class
                    crnt__product.save()
                messages.success(request, "Successfully added!")
                return redirect('apGroupUpProductsByShippinigClass')
            else:
                messages.warning(request, "No products found!")
                return redirect('apGroupUpProductsByShippinigClass')
        else:
            messages.warning(request, "No products found!")
            return redirect('apGroupUpProductsByShippinigClass')

    return redirect('apGroupUpProductsByShippinigClass')

























