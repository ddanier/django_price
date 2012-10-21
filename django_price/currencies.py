# coding: utf-8

# see http://en.wikipedia.org/wiki/ISO_4217#Active_codes
CURRENCIES = [
    # ISO    ISO  dec  round name                        symbol
    # Code   Num  plac ing
    #             es
    ('AED', '784', 2, None, 'United Arab Emirates dirham', None),
    ('AFN', '971', 2, None, 'Afghan afghani', None),
    ('ALL', '008', 2, None, 'Albanian lek', None),
    ('AMD', '051', 2, None, 'Armenian dram', None),
    ('ANG', '532', 2, None, 'Netherlands Antillean guilder', None),
    ('AOA', '973', 2, None, 'Angolan kwanza', None),
    ('ARS', '032', 2, None, 'Argentine peso', None),
    ('AUD', '036', 2, None, 'Australian dollar', None),
    ('AWG', '533', 2, None, 'Aruban florin', None),
    ('AZN', '944', 2, None, 'Azerbaijani manat', None),
    ('BAM', '977', 2, None, 'Bosnia and Herzegovina convertible mark', None),
    ('BBD', '052', 2, None, 'Barbados dollar', None),
    ('BDT', '050', 2, None, 'Bangladeshi taka', None),
    ('BGN', '975', 2, None, 'Bulgarian lev', None),
    ('BHD', '048', 3, None, 'Bahraini dinar', None),
    ('BIF', '108', 0, None, 'Burundian franc', None),
    ('BMD', '060', 2, None, 'Bermudian dollar (customarily known as Bermuda dollar)', None),
    ('BND', '096', 2, None, 'Brunei dollar', None),
    ('BOB', '068', 2, None, 'Boliviano', None),
    ('BOV', '984', 2, None, 'Bolivian Mvdol (funds code)', None),
    ('BRL', '986', 2, None, 'Brazilian real', None),
    ('BSD', '044', 2, None, 'Bahamian dollar', None),
    ('BTN', '064', 2, None, 'Bhutanese ngultrum', None),
    ('BWP', '072', 2, None, 'Botswana pula', None),
    ('BYR', '974', 0, None, 'Belarusian ruble', None),
    ('BZD', '084', 2, None, 'Belize dollar', None),
    ('CAD', '124', 2, None, 'Canadian dollar', None),
    ('CDF', '976', 2, None, 'Congolese franc', None),
    ('CHE', '947', 2, None, 'WIR Euro (complementary currency)', None),
    ('CHF', '756', 2, None, 'Swiss franc', None),
    ('CHW', '948', 2, None, 'WIR Franc (complementary currency)', None),
    ('CLF', '990', 0, None, 'Unidad de Fomento (funds code)', None),
    ('CLP', '152', 0, None, 'Chilean peso', None),
    ('CNY', '156', 2, None, 'Chinese yuan', None),
    ('COP', '170', 2, None, 'Colombian peso', None),
    ('COU', '970', 2, None, 'Unidad de Valor Real', None),
    ('CRC', '188', 2, None, 'Costa Rican colon', None),
    ('CUC', '931', 2, None, 'Cuban convertible peso', None),
    ('CUP', '192', 2, None, 'Cuban peso', None),
    ('CVE', '132', 0, None, 'Cape Verde escudo', None),
    ('CZK', '203', 2, None, 'Czech koruna', None),
    ('DJF', '262', 0, None, 'Djiboutian franc', None),
    ('DKK', '208', 2, None, 'Danish krone', None),
    ('DOP', '214', 2, None, 'Dominican peso', None),
    ('DZD', '012', 2, None, 'Algerian dinar', None),
    ('EGP', '818', 2, None, 'Egyptian pound', None),
    ('ERN', '232', 2, None, 'Eritrean nakfa', None),
    ('ETB', '230', 2, None, 'Ethiopian birr', None),
    ('EUR', '978', 2, None, 'Euro', u'€'),
    ('FJD', '242', 2, None, 'Fiji dollar', None),
    ('FKP', '238', 2, None, 'Falkland Islands pound', None),
    ('GBP', '826', 2, None, 'Pound sterling', None),
    ('GEL', '981', 2, None, 'Georgian lari', None),
    ('GHS', '936', 2, None, 'Ghanaian cedi', None),
    ('GIP', '292', 2, None, 'Gibraltar pound', None),
    ('GMD', '270', 2, None, 'Gambian dalasi', None),
    ('GNF', '324', 0, None, 'Guinean franc', None),
    ('GTQ', '320', 2, None, 'Guatemalan quetzal', None),
    ('GYD', '328', 2, None, 'Guyanese dollar', None),
    ('HKD', '344', 2, None, 'Hong Kong dollar', None),
    ('HNL', '340', 2, None, 'Honduran lempira', None),
    ('HRK', '191', 2, None, 'Croatian kuna', None),
    ('HTG', '332', 2, None, 'Haitian gourde', None),
    ('HUF', '348', 2, None, 'Hungarian forint', None),
    ('IDR', '360', 0, None, 'Indonesian rupiah', None),
    ('ILS', '376', 2, None, 'Israeli new sheqel', None),
    ('INR', '356', 2, None, 'Indian rupee', None),
    ('IQD', '368', 0, None, 'Iraqi dinar', None),
    ('IRR', '364', 0, None, 'Iranian rial', None),
    ('ISK', '352', 0, None, 'Icelandic króna', None),
    ('JMD', '388', 2, None, 'Jamaican dollar', None),
    ('JOD', '400', 3, None, 'Jordanian dinar', None),
    ('JPY', '392', 0, None, 'Japanese yen', None),
    ('KES', '404', 2, None, 'Kenyan shilling', None),
    ('KGS', '417', 2, None, 'Kyrgyzstani som', None),
    ('KHR', '116', 2, None, 'Cambodian riel', None),
    ('KMF', '174', 0, None, 'Comoro franc', None),
    ('KPW', '408', 0, None, 'North Korean won', None),
    ('KRW', '410', 0, None, 'South Korean won', None),
    ('KWD', '414', 3, None, 'Kuwaiti dinar', None),
    ('KYD', '136', 2, None, 'Cayman Islands dollar', None),
    ('KZT', '398', 2, None, 'Kazakhstani tenge', None),
    ('LAK', '418', 0, None, 'Lao kip', None),
    ('LBP', '422', 0, None, 'Lebanese pound', None),
    ('LKR', '144', 2, None, 'Sri Lankan rupee', None),
    ('LRD', '430', 2, None, 'Liberian dollar', None),
    ('LSL', '426', 2, None, 'Lesotho loti', None),
    ('LTL', '440', 2, None, 'Lithuanian litas', None),
    ('LVL', '428', 2, None, 'Latvian lats', None),
    ('LYD', '434', 3, None, 'Libyan dinar', None),
    ('MAD', '504', 2, None, 'Moroccan dirham', None),
    ('MDL', '498', 2, None, 'Moldovan leu', None),
    #('MGA', '969', 0.7, None, 'Malagasy ariary', None),
    ('MKD', '807', 2, None, 'Macedonian denar', None),
    ('MMK', '104', 0, None, 'Myanma kyat', None),
    ('MNT', '496', 2, None, 'Mongolian tugrik', None),
    ('MOP', '446', 2, None, 'Macanese pataca', None),
    #('MRO', '478', 0.7, None, 'Mauritanian ouguiya', None),
    ('MUR', '480', 2, None, 'Mauritian rupee', None),
    ('MVR', '462', 2, None, 'Maldivian rufiyaa', None),
    ('MWK', '454', 2, None, 'Malawian kwacha', None),
    ('MXN', '484', 2, None, 'Mexican peso', None),
    ('MXV', '979', 2, None, 'Mexican Unidad de Inversion (UDI) (funds code)', None),
    ('MYR', '458', 2, None, 'Malaysian ringgit', None),
    ('MZN', '943', 2, None, 'Mozambican metical', None),
    ('NAD', '516', 2, None, 'Namibian dollar', None),
    ('NGN', '566', 2, None, 'Nigerian naira', None),
    ('NIO', '558', 2, None, 'Nicaraguan córdoba', None),
    ('NOK', '578', 2, None, 'Norwegian krone', None),
    ('NPR', '524', 2, None, 'Nepalese rupee', None),
    ('NZD', '554', 2, None, 'New Zealand dollar', None),
    ('OMR', '512', 3, None, 'Omani rial', None),
    ('PAB', '590', 2, None, 'Panamanian balboa', None),
    ('PEN', '604', 2, None, 'Peruvian nuevo sol', None),
    ('PGK', '598', 2, None, 'Papua New Guinean kina', None),
    ('PHP', '608', 2, None, 'Philippine peso', None),
    ('PKR', '586', 2, None, 'Pakistani rupee', None),
    ('PLN', '985', 2, None, 'Polish złoty', None),
    ('PYG', '600', 0, None, 'Paraguayan guaraní', None),
    ('QAR', '634', 2, None, 'Qatari rial', None),
    ('RON', '946', 2, None, 'Romanian new leu', None),
    ('RSD', '941', 2, None, 'Serbian dinar', None),
    ('RUB', '643', 2, None, 'Russian rouble', None),
    ('RWF', '646', 0, None, 'Rwandan franc', None),
    ('SAR', '682', 2, None, 'Saudi riyal', None),
    ('SBD', '090', 2, None, 'Solomon Islands dollar', None),
    ('SCR', '690', 2, None, 'Seychelles rupee', None),
    ('SDG', '938', 2, None, 'Sudanese pound', None),
    ('SEK', '752', 2, None, 'Swedish krona/kronor', None),
    ('SGD', '702', 2, None, 'Singapore dollar', None),
    ('SHP', '654', 2, None, 'Saint Helena pound', None),
    ('SLL', '694', 0, None, 'Sierra Leonean leone', None),
    ('SOS', '706', 2, None, 'Somali shilling', None),
    ('SRD', '968', 2, None, 'Surinamese dollar', None),
    ('SSP', '728', 2, None, 'South Sudanese pound', None),
    ('STD', '678', 0, None, 'São Tomé and Príncipe dobra', None),
    ('SYP', '760', 2, None, 'Syrian pound', None),
    ('SZL', '748', 2, None, 'Swazi lilangeni', None),
    ('THB', '764', 2, None, 'Thai baht', None),
    ('TJS', '972', 2, None, 'Tajikistani somoni', None),
    ('TMT', '934', 2, None, 'Turkmenistani manat', None),
    ('TND', '788', 3, None, 'Tunisian dinar', None),
    ('TOP', '776', 2, None, 'Tongan paʻanga', None),
    ('TRY', '949', 2, None, 'Turkish lira', 'TL'),
    ('TTD', '780', 2, None, 'Trinidad and Tobago dollar', None),
    ('TWD', '901', 2, None, 'New Taiwan dollar', None),
    ('TZS', '834', 2, None, 'Tanzanian shilling', None),
    ('UAH', '980', 2, None, 'Ukrainian hryvnia', None),
    ('UGX', '800', 2, None, 'Ugandan shilling', None),
    ('USD', '840', 2, None, 'United States dollar', '$'),
    #('USN', '997', 2, None, 'United States dollar (next day) (funds code)', None),
    #('USS', '998', 2, None, 'United States dollar (same day) (funds code) (one source[who?] claims it is no longer used, but it is still on the ISO 4217-MA list)', None),
    ('UYI', '940', 0, None, 'Uruguay Peso en Unidades Indexadas (URUIURUI) (funds code)', None),
    ('UYU', '858', 2, None, 'Uruguayan peso', None),
    ('UZS', '860', 2, None, 'Uzbekistan som', None),
    ('VEF', '937', 2, None, 'Venezuelan bolívar fuerte', None),
    ('VND', '704', 0, None, 'Vietnamese đồng', None),
    ('VUV', '548', 0, None, 'Vanuatu vatu', None),
    ('WST', '882', 2, None, 'Samoan tala', None),
    ('XAF', '950', 0, None, 'CFA franc BEAC', None),
    #('XAG', '961', None, None, 'Silver (one troy ounce)', None),
    #('XAU', '959', None, None, 'Gold (one troy ounce)', None),
    #('XBA', '955', None, None, 'European Composite Unit (EURCO) (bond market unit)', None),
    #('XBB', '956', None, None, 'European Monetary Unit (E.M.U.-6) (bond market unit)', None),
    #('XBC', '957', None, None, 'European Unit of Account 9 (E.U.A.-9) (bond market unit)', None),
    #('XBD', '958', None, None, 'European Unit of Account 17 (E.U.A.-17) (bond market unit)', None),
    ('XCD', '951', 2, None, 'East Caribbean dollar', None),
    #('XDR', '960', None, None, 'Special Drawing Rights', None),
    #('XFU', 'Nil', None, None, 'UIC franc (special settlement currency)', None),
    ('XOF', '952', 0, None, 'CFA Franc BCEAO', None),
    #('XPD', '964', None, None, 'Palladium (one troy ounce)', None),
    ('XPF', '953', 0, None, 'CFP franc', None),
    #('XPT', '962', None, None, 'Platinum (one troy ounce)', None),
    #('XTS', '963', None, None, 'Code reserved for testing purposes', None),
    #('XXX', '999', None, None, 'No currency', None),
    ('YER', '886', 2, None, 'Yemeni rial', None),
    ('ZAR', '710', 2, None, 'South African rand', None),
    ('ZMK', '894', 2, None, 'Zambian kwacha', None),
    ('ZWL', '932', 2, None, 'Zimbabwe dollar'),
]