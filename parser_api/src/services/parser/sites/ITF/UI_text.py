from enum import Enum


class ITFDataWaterNameSelector(str, Enum):
    ADDRESS = 'Հասցե'
    CONSUMPTION = 'Սպառում'  # потребление, расход
    DEBIT_FULL = 'Պարտք'  # долг итого


class ITFDataElectricityNameSelector(str, Enum):
    ADDRESS = 'Հասցե'
    CONSUMPTION = 'էլ. էներգիայի ծախսը'  # потребление, расход
    DEBIT_FULL = 'Ենթակա է վճարման'  # долг итого


class ITFDataGasNameSelector(str, Enum):
    ADDRESS = 'Հասցե'
    CONSUMPTION = 'Ծախս'  # потребление, расход
    DEBIT_CONSUMPTION = 'Սպառողական պարտք'  # долг за потребление
    DEBIT_SERVICE = 'Սպասարկման պարտք'  # долг за обслуживание
    DEBIT_FULL = 'Պարտք'  # долг итого


class ITFFormTextAreaName(str, Enum):
    CUSTOMER_ID = 'customer_id'
    AGREEMENT = 'agreement_number'


class ITFGasFormClassSelect(str, Enum):
    SELECT_CITY_LIST = 'select2-selection__rendered'
    SELECT_CITY_SEARCH_TEXT_AREA = 'select2-search__field'
    SELECT_TEST = 'select2 - city - eh - results'


class ITFSiteButton(str, Enum):
    SEARCH_BTN = 'btn btn-success'

# class ITFGasFormIDSelectCity(str, Enum):
#     YEREVAN = 'select2-city-1o-result-3fo4-0'  # Ереван
#     ABOVYAN = 'select2-city-1o-result-tssw-6532'  # Абовян
#     ALAVERDI = 'select2-city-1o-result-hxdf-6537'  # Алаверди
#     ANGEHAKOT = 'select2-city-1o-result-o03r-6545'  # Ангехакот
#     ARARAT = 'select2-city-1o-result-gduz-6524'  # Арарат
#     ARZNI = 'select2-city-1o-result-x9ew-6533'  # Арзни
#     ARMAVIR = 'select2-city-1o-result-v0zq-6526'  # Армавир
#     ARTASHAT = 'select2-city-1o-result-h8eh-6523'  # Арташат
#     ARTIK = 'select2-city-1o-result-yt59-6542'  # Артик
#     AKHTALA = 'select2-city-1o-result-8knd-6536'  # Ахтала
#     ASHTARAK = 'select2-city-1o-result-sq2s-6543'  # Аштарак
#     VANADZOR = 'select2-city-1o-result-9do2-6541'  # Ванадзор
#     VARDENIS = 'select2-city-1o-result-u1s9-6531'  # Варденис
#     VAGHARSHAPAT = 'select2-city-1o-result-qck2-6527'  # Вагаршапат
#     GAVAR = 'select2-city-1o-result-pl1i-6528'  # Гавар
#     GORIS = 'select2-city-1o-result-2gah-6546'  # Горис
#     GYUMRI = 'select2-city-1o-result-0vja-6543'  # Гюмри
#     DILIJAN = 'select2-city-1o-result-vvxt-6551'  # Дилижан
#     IJEVAN = 'select2-city-1o-result-xt6n-6552'  # Иджеван
#     KADJARAN = 'select2-city-1o-result-u8r1-6547'  # Каджаран
#     KAPAN = 'select2-city-1o-result-h0qx-6548'  # Капан
#     MARTUNI = 'select2-city-1o-result-3k3z-6529'  # Мартуни
#     MEGHRI = 'select2-city-1o-result-9npo-6549'  # Мегри
#     RAZDAN = 'select2-city-1o-result-msz7-6535'  # Раздан
#     SEVAN = 'select2-city-1o-result-74fs-6530'  # Севан
#     SISIAN = 'select2-city-1o-result-l8w6-6550'  # Сисиан
#     SPITAK = 'select2-city-1o-result-v17w-6538'  # Спитак
#     STEPANAVAN = 'select2-city-1o-result-hzhu-6539'  # Степанаван
#     STEPANAKERT = 'select2-city-1o-result-8uex-6544'  # Степанакерт
#     TALIN = 'select2-city-1o-result-9q1l-6523'  # Талин
#     TASHIR = 'select2-city-1o-result-csaw-6540'  # Ташир
#     CHARENTSAVAN = 'select2-city-1o-result-dz0m-6534'  # Чаренцаван
