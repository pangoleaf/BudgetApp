from dataclasses import dataclass
from script import say, ask


class BudgetApp:
    exit = False
    budgets = []

    def __init__(self):
        self.run()

    # SETUP

    def setup(self):
        self.username = ask("welcome")
        self.total_money = ask("how_much_total", self.username, num=True)
        self.unbudgeted = self.total_money

        say("first_cat")
        self.add_budget(from_unbudgeted=True)

        keep_asking = True
        while keep_asking and self.unbudgeted > 0:
            say("next_cat")
            new = self.add_budget(from_unbudgeted=True)
            keep_asking = new != "DONE"

        if self.unbudgeted > 0:
            say("creating_misc", self.unbudgeted)
            self.budgets.append(Budget("Misc", self.unbudgeted))
            self.unbudgeted = 0

        self.print_budgets()

    def set_commands(self):
        self.commands = {
            "COMMANDS": self.print_commands,
            "BALANCE": self.print_budgets,
            "TRANSFER": self.transfer,
            "SPEND": self.spend,
            "ADD_MONEY": self.add_money,
            "NEW_BUDGET": self.add_budget,
            "EXIT": self.set_exit,
        }

    # UTILS

    def in_budgets(self, category):
        return category.lower in ["misc"] + [b.category.lower for b in self.budgets]

    def choose_existing(self, script):
        chosen = ask(script)
        while not self.in_budgets(chosen):
            say("not_a_budget")
            chosen = ask(script)
        return chosen

    def cat_value(self, cat):
        return [b for b in self.budgets if b.category == cat][0].value

    def adjust_cat(self, cat, amount):
        [b for b in self.budgets if b.category == cat][0].adjust(amount)

    def add_budget(self, from_unbudgeted=False):
        new_bud_cat = ask("enter_category")

        if new_bud_cat == "DONE":
            return "DONE"

        if self.in_budgets(new_bud_cat):
            say("name_unavailable")
            return "FAIL"

        new_bud_value = ask("assign_amount", new_bud_cat, num=True)

        if from_unbudgeted and new_bud_value > self.unbudgeted:
            say("not_enough", new_bud_cat)
            return "FAIL"

        self.budgets.append(Budget(new_bud_cat, new_bud_value))
        say("ab_success", new_bud_cat, new_bud_value)

        if from_unbudgeted:
            self.unbudgeted -= new_bud_value
            say("remaining_total", self.unbudgeted)
        return new_bud_cat

    # COMMANDS

    def print_commands(self):
        say(f"Available commands are: {', '.join(self.commands.keys())}")

    def print_budgets(self):
        say("balances_are")
        for b in self.budgets:
            print(f"    {b.category}: {b.value}")
        print(f"Unbudgeted: {self.unbudgeted}")
        print(f"Total: {sum([b.value for b in self.budgets]) + self.unbudgeted}")

    def transfer(self):
        budget_from = self.choose_existing("tr_which_from")
        budget_to = self.choose_existing("tr_which_to")
        amount = ask("tr_how_much", num=True)
        self.adjust_cat(budget_from, -amount)
        self.adjust_cat(budget_to, amount)
        say("tr_success", amount, budget_from, budget_to)

    def spend(self):
        spent_from = self.choose_existing("sp_which")
        amount = ask("sp_how_much", num=True)
        self.adjust_cat(spent_from, -amount)
        say("sp_success", amount, spent_from, self.cat_value(spent_from))

    def add_money(self):
        add_to = self.choose_existing("am_which_to")
        amount = ask("am_how_much", add_to)
        self.adjust_cat(add_to, amount)
        say("am_success", amount, add_to)

    # APP

    def set_exit(self):
        self.exit = True

    def route(self, command):
        if command not in self.commands.keys():
            say("not_command")
            self.print_commands()
            return

        self.commands[command]()

    def run(self):
        self.setup()
        self.set_commands()

        while not self.exit:
            self.route(ask("what_do"))


@dataclass
class Budget:
    category: str
    value: int

    def adjust(self, amount):
        self.value += amount



