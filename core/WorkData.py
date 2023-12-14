from dataclasses import dataclass


@dataclass
class WorkData:
    list_name: str
    work_name: str
    range_one: str
    range_two: str
    unit_w: str

    def __init__(self, list_name, work_name, range_one, range_two, unit_w):
        self.list_name = list_name
        self.work_name = work_name
        self.range_one = range_one
        self.range_two = range_two
        self.unit_w = unit_w

    def set_list_name(self, list_name):
        self.list_name = list_name

    def set_work_name(self, work_name):
        self.work_name = work_name

    def set_range_one(self, range_one):
        self.range_one = range_one

    def set_range_two(self, range_two):
        self.range_two = range_two

    def set_unit_w(self, unit_w):
        self.unit_w = unit_w
