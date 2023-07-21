import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DF_COLUMNS = ["id", "amount", "category", "date"]

class PersonalSpending:
    def __init__(self):
        self.spent_money_this_month = 0
        self.spent_money_this_day = 0
        self.all_spending = pd.DataFrame(columns=DF_COLUMNS) # todo: should be DataBase
        self.categories = {"supermarket", "transport", "infrequent spending", "restaurant", "one per month", "travel"}
        self.current_id = 0
        self.today = datetime.today()

    def set_categories(self, categories):
        self.categories = categories

    def add_spending(self, amount: int, category: str, date=None):
        today = datetime.today()
        if self.today.month != today.month:
            self.spent_money_this_month = 0
        if self.today != today:
            self.today = today
            self.spent_money_this_day = 0
        if date is None:
            date = today
        new_row = {"id": self.current_id, "amount": amount, "category": category, "date": date}
        self.all_spending.append(new_row, ignore_index=True)
        self.current_id += 1
        if date == today:
            self.spent_money_this_day += amount
        if date.month == today.month:
            self.spent_money_this_month += amount

    def undo(self, id: int):
        undo_row = self.all_spending[self.all_spending["id"] == id]["sp"].iloc[0]
        if undo_row["date"] == self.today:
            self.spent_money_this_day -= undo_row["amount"]
        if undo_row["date"].month == self.today.month:
            self.spent_money_this_month -= undo_row["amount"]
        self.all_spending = self.all_spending.drop(self.all_spending[self.all_spending["id"] == id].index)

    def get_spending(self):
        today = datetime.today()
        if self.today.month != today.month:
            self.spent_money_this_month = 0
        if self.today != today:
            self.today = today
            self.spent_money_this_day = 0

        return self.spent_money_this_day, self.spent_money_this_month / self.today.day

