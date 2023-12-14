import DataBaseTgBot as db


def parse_works_list():
    works_list = db.getWorks()
    print("-" * 65)
    ss = ""
    for i, work in enumerate(works_list):
        ss += (f"{i + 1}. " + work.work_name + " | " + work.list_name + " | " + work.fact + " | " + work.per_day + " | " +
               work.unit + " | \n")
    return ss


def getMaxLenWorkName(works):
    max_len = 0
    for w in works:
        if len(w.work_name) >= max_len:
            max_len = len(w.work_name)

    return max_len
