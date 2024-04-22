import utils.farms_name as farm


def getMaxLenWorkName(works):
    max_len = 0
    for w in works:
        if len(w.work_name) >= max_len:
            max_len = len(w.work_name)

    return max_len


def parse_work_list(resp_dict):
    works = []
    for _ in resp_dict:
        works.append(_['work_name'])
    return works


def parse_work_to_string(work):
    text = ""
    plan = work[0]['plan'].split(",")
    fact = work[0]['fact'].split(",")
    per_day = work[0]['per_day'].split(",")
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.TURINO + " План: " + plan[0] + ", Факт: " + fact[0] + ", За день: " + \
            per_day[0] + ";"
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.KOMMUNI + " План: " + plan[1] + ", Факт: " + fact[1] + ", За день: " + \
            per_day[1] + ";"
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.ZARYA + " План: " + plan[2] + ", Факт: " + fact[2] + ", За день: " + \
            per_day[2] + ";"
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.SLAVG + " План: " + plan[3] + ", Факт: " + fact[3] + ", За день: " + \
            per_day[3] + ";"
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.EKSBAZA + " План: " + plan[4] + ", Факт: " + fact[4] + ", За день: " + \
            per_day[4] + ";"
    text += "\n" + ("➖➖➖" * 5) + "\n" + farm.RAPTS + " План: " + plan[5] + ", Факт: " + fact[5] + ", За день: " + \
            per_day[5] + ";"
    return text
