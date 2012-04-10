import decimal

def price_amount(value, currency=None):
    from .currency import Currency
    decimal_places = 3
    rounding = decimal.ROUND_HALF_UP
    if not currency is None:
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        if not currency.decimal_places is None:
            decimal_places = currency.decimal_places
        if not currency.rounding is None:
            rounding = currency.rounding
    if not isinstance(value, (decimal.Decimal)):
        value = decimal.Decimal(str(value))
    quantize_str = '0'
    if decimal_places > 0:
        quantize_str = '0.%s' % ('0' * decimal_places)
    return value.quantize(decimal.Decimal(quantize_str), rounding=rounding)

