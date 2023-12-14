import datetime
import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import DataBaseTgBot as mdb


def get_service_simple():
    return build('sheets', 'v4', developerKey=api_key)


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/mypythonproject.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


service = get_service_sacc()
sheet = service.spreadsheets()

sheet_id = "1WcZ9aCw4vm8Y4vTAwJmqPPHdKAYvY4Rw4GlEvurumd0"
sheetMilk_id = "17YLkwH3gaECYkOUBCZnGynhZODNGDAM0rpsOH7Pmn6E"

plowingRange = dict()
rp = ""


def initial_ranges():
    rep = f"Ежедневный отчёт на {data}, Глусский район.\n\n"
    works = mdb.getWorks()
    if works is None:
        print("\nEmpty\n")
    else:
        for el in works:
            try:
                wr = sheet.values().batchGet(spreadsheetId=sheet_id,  # пахота под зябь
                                             ranges=[f"{el.list_name + '!' + el.fact}",
                                                     f"{el.list_name + '!' + el.per_day}"]).execute()
                rep += (el.work_name + " всего: " + get_cell_value_from_ranges(wr)[0] +
                        f" {el.unit}, в том числе за день: " + get_cell_value_from_ranges(wr)[1]) + f" {el.unit}\n"
            except Exception:
                rep += "?" * 20 + "\n"
        return rep


compoundFeed, addingOrganic, removalOrganic, fuel, productionMilk, sortMilk, rowsMtsTurino, rowsMtsZaryaKom = None, None, None, None, None, None, None, None
rowsMtsGlZarya, rowsMtsGlZarya, rowsMtsSlavgorod, rowsMtsEksBaza, rowsMtsRpts = None, None, None, None, None
dirCompoundFeed, dirAddingOrganic, dirRemovalOrganic, dirFuel, dirSortMilk = None, None, None, None, None


def read_data_from_google_table():
    global compoundFeed, addingOrganic, removalOrganic, fuel, productionMilk, sortMilk, rowsMtsTurino, rowsMtsZaryaKom
    global rowsMtsGlZarya, rowsMtsGlZarya, rowsMtsSlavgorod, rowsMtsEksBaza, rowsMtsRpts
    global dirCompoundFeed, dirAddingOrganic, dirRemovalOrganic, dirFuel, dirSortMilk

    compoundFeed = sheet.values().batchGet(spreadsheetId=sheet_id,  # внесение органики
                                           ranges=["органика!N13", "органика!O13"]).execute()
    addingOrganic = sheet.values().batchGet(spreadsheetId=sheet_id,  # внесение органики
                                            ranges=["органика!G6:I6", "органика!G13:I13"]).execute()

    removalOrganic = sheet.values().batchGet(spreadsheetId=sheet_id,  # Вывозка органики
                                             ranges=["органика!C6:E6", "органика!C13:E13"]).execute()

    fuel = sheet.values().batchGet(spreadsheetId=sheet_id,  # внесение органики
                                   ranges=["органика!K4:L4", "органика!K13:L13"]).execute()

    productionMilk = sheet.values().batchGet(spreadsheetId=sheetMilk_id,  # производство молока
                                             ranges=["ежедневный!D24:H24", "ежедневный!J24:M24"]).execute()

    sortMilk = sheet.values().batchGet(spreadsheetId=sheetMilk_id,  # сортность молока
                                       ranges=["ежедневный!B28:D28", "ежедневный!B29:D29"]).execute()

    mtsTurino = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс турино
                                   range="Техника!B4:D4").execute()
    mtsZaryaKom = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс заря коммуны
                                     range="Техника!B5:D5").execute()
    mtsGlZarya = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс глусская заря
                                    range="Техника!B6:D6").execute()
    mtsSlavgorod = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс славгородский
                                      range="Техника!B7:D7").execute()
    mtsEksBaza = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс экс база
                                    range="Техника!B8:D8").execute()
    mtsRpts = sheet.values().get(spreadsheetId=sheet_id,  # техника мтс раптс
                                 range="Техника!B9:D9").execute()

    rowsMtsTurino = mtsTurino.get('values', [])
    rowsMtsZaryaKom = mtsZaryaKom.get('values', [])
    rowsMtsGlZarya = mtsGlZarya.get('values', [])
    rowsMtsSlavgorod = mtsSlavgorod.get('values', [])
    rowsMtsEksBaza = mtsEksBaza.get('values', [])
    rowsMtsRpts = mtsRpts.get('values', [])

    dirCompoundFeed = createDictionary(getRowsFromRanges(compoundFeed))
    dirAddingOrganic = createDictionary(getRowsFromRanges(addingOrganic))
    dirRemovalOrganic = createDictionary(getRowsFromRanges(removalOrganic))
    dirFuel = createDictionary(getRowsFromRanges(fuel))
    dirSortMilk = createDictionary(getRowsFromRanges(sortMilk))


def getTypeWorkList(ranges):
    listOne = list
    listTwo = list
    counter = 1
    for i in ranges:
        for j in i.values():
            if type(j) == list:
                for header in j:
                    if counter == 1:
                        listOne = header
                        counter += 1
                    elif counter == 2:
                        listTwo = header
    return [listOne, listTwo]


def get_cell_value_from_ranges(ranges) -> list:
    cell_value = []
    for i in ranges.get('valueRanges', []):
        cell_value.append(i['values'][0][0])

    return cell_value


def createDictionary(rows):
    header = getTypeWorkList(rows)[0]
    values = getTypeWorkList(rows)[1]

    dictionary = {}
    for i in range(len(header)):
        dictionary[header[i]] = values[i]

    return dictionary


def getRowsFromRanges(ranges):
    return ranges.get('valueRanges', [])


data = str(datetime.date.today())
data = f'{data[8:9 + 1]}.{data[5:7]}.{data[:4]}'


def generateReport():
    read_data_from_google_table()
    prdMilk = getRowsFromRanges(productionMilk)

    report = f'''
    Ежедневный отчёт на {data}, Глусский район.


Вывозка органических удобрений всего {dirRemovalOrganic.get("Факт, тонн")} тонн, в том числе за день {dirRemovalOrganic.get("За день, тонн")} тонн, {dirRemovalOrganic.get("% к плану")} от плана
Внесение органических удобрений всего {dirAddingOrganic.get("Факт, тонн")} тонн, в том числе за день {dirAddingOrganic.get("за день, тонн")} тонн, {dirAddingOrganic.get("% к плану")} от плана

Животноводство:
Валовый надой за день {getTypeWorkList(prdMilk)[0][0]} кг.
Надой за день по отношению к предыдущему дню: ({"+" + getTypeWorkList(prdMilk)[0][2] if (getTypeWorkList(prdMilk)[0][2])[0] != '-' else getTypeWorkList(prdMilk)[0][2]}),
Реализовано:  {getTypeWorkList(prdMilk)[1][0]} кг ({dirSortMilk.get("Экстра")}% - экстра, {dirSortMilk.get("Высший сорт")}% - высший сорт, {dirSortMilk.get("1 сорт")}%- 1 сорт) ,
Реализовано молока за день по отношению к предыдущему дню: ({"+" + getTypeWorkList(prdMilk)[1][3] if (getTypeWorkList(prdMilk)[1][3])[0] != '-' else getTypeWorkList(prdMilk)[1][3]}) кг.
Уровень товарности:  {getTypeWorkList(prdMilk)[1][2]}%
Удой на 1 голову: {getTypeWorkList(prdMilk)[0][4]} л.

Остаток комбикормов на конец дня: {get_cell_value_from_ranges(compoundFeed)[0]}
ППБК: {get_cell_value_from_ranges(compoundFeed)[1]}

Расход топлива за день {dirFuel.get("Расход")} л. Остаток топлива на конец дня {dirFuel.get("Остаток ДТ")} л.

Техника МТС:
{getTechnicalMts()}
    '''

    return report


def toFixed(numObj, digits=1):
    return f"{numObj:.{digits}f}"


def getTechnicalMts():
    turino = 'ОАО "Турино-агро" - ' + generateMtsReport(rowsMtsTurino) + '\n'
    zaryaKom = 'ОАО "Заря Коммуны" - ' + generateMtsReport(rowsMtsZaryaKom) + '\n'
    glZarya = 'ОАО "Глусская Заря" - ' + generateMtsReport(rowsMtsGlZarya) + '\n'
    slavg = 'ОАО "Агрофирма Славгородский" - ' + generateMtsReport(rowsMtsSlavgorod) + '\n'
    eksBaza = 'ОАО "Экспериментальная База Глуск" - ' + generateMtsReport(rowsMtsEksBaza) + '\n'
    rpts = 'ОАО "Глусский РАПТС" - ' + generateMtsReport(rowsMtsRpts)
    return turino + zaryaKom + glZarya + slavg + eksBaza + rpts


def generateMtsReport(val):
    teh = ""
    try:
        if len(val[0]) == 3:
            if val[0][0] != '':
                teh += val[0][0] + " - 3522, "
            if val[0][1] != '':
                teh += val[0][1] + " - 1221, "
            if val[0][2] != '':
                teh += val[0][2] + " - Амкодор "
        elif len(val[0]) == 2:
            if val[0][0] != '':
                teh += val[0][0] + " - 3522, "
            if val[0][1] != '':
                teh += val[0][1] + " - 1221 "
        elif len(val[0]) == 1:
            if val[0][0] != '':
                teh += val[0][0] + " - 3522"
        elif len(val[0]) == 0:
            teh += " - "
    except IndexError:
        teh += "-"
    return teh

