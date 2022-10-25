def return_council_tax(band, number_of_tenants):
    band_payment_ratio = {
        # discoverable from this website: https://www.edinburgh.gov.uk/council-tax/council-tax-bands?documentId=12238&categoryId=20005
        'A': 1238.13,
        'B': 1444.48,
        'C': 1650.84,
        'D': 1857.19,
        'E': 2396.28,
        'F': 2931.55,
        'G': 3497.45,
        'H': 4334.82
    }

    date_payment_ratio = {
        '5th May': 261.55,
        '5th Jun': 267,
        '5th July': 267,
        '5th Aug': 267,
        '5th Sep': 267,
        '5th Oct': 267,
        '5th Nov': 267,
        '5th Dec': 267,
        '5th Jan': 267,
        '5th Feb': 267,
        '5th Mar': 267
    }

    total_council_tax = band_payment_ratio[band.upper()]
    sum_of_payments = sum([date_payment_ratio[key] for key in date_payment_ratio])
    assert total_council_tax == sum_of_payments, "purported total council tax & sum of council tax payments don't add up!"
    return total_council_tax / number_of_tenants