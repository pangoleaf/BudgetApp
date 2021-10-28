from dataclasses import dataclass, field
from os import walk
from script import say, ask, valid


@dataclass
class Budget:
    category: str
    value: int

    def adjust(self, amount):
        self.value += amount


@dataclass
class BudgetApp:
    load: str = ""

    username: str = ""
    total_input_money: int = 0
    budgets: list[Budget] = field(default_factory=list)
    setup_done: bool = False
    filename: str = ""

    sav_dir = "./saves"
    unb = "Unbudgeted"
    exit = False

    def __post_init__(self):
        self.set_commands()

        if self.load:
            with open(f"{self.sav_dir}/{self.load}", "r") as f:
                saved = f.read()
            return eval(saved)

        return self.run()

    # SETUP

    def setup(self):
        self.username = ask("su_what_name")
        self.total_input_money = ask("su_how_much_total", self.username, num=True)
        self.budgets = [Budget(self.unb, self.total_input_money)]

        say("su_first_cat")
        self.add_budget_initial()

        keep_asking = True
        while keep_asking and self.cat_value(self.unb) > 0:
            say("su_next_cat")
            new = self.add_budget_initial()
            keep_asking = new != "DONE"

        if self.cat_value(self.unb) > 0:
            say("creating_misc", self.cat_value(self.unb))
            self.budgets.append(Budget("Misc", self.cat_value(self.unb)))
        self.budgets.remove([b for b in self.budgets if b.category == self.unb][0])

        self.setup_done = True

        self.print_budgets()
        say("su_commands")
        self.print_commands()

    def add_budget_initial(self):
        new_cat = valid("enter_cat", self.vl_new_cat, f_say="name_unavailable")

        if new_cat == "DONE":
            return "DONE"

        new_amt = self.get_new_amt(new_cat, self.unb)

        self.budgets.append(Budget(new_cat, new_amt))
        say("ab_success", new_cat, new_amt)

        self.cat_adjust(self.unb, -new_amt)
        say("remaining_total", self.cat_value(self.unb))
        return new_cat

    def set_commands(self):
        self.commands = {
            "COMMANDS": self.print_commands,
            "BALANCES": self.print_budgets,
            "TRANSFER": self.transfer,
            "SPEND": self.spend,
            "ADD MONEY": self.add_money,
            "NEW BUDGET": self.route_new_budget,
            "SAVE": self.save_to_file,
            "EXIT": self.set_exit,
        }

    # UTILS
    def cat_value(self, cat):
        return [b for b in self.budgets if b.category == cat][0].value

    def cat_adjust(self, cat, amount):
        [b for b in self.budgets if b.category == cat][0].adjust(amount)

    def get_new_amt(self, f_to, f_frm=""):
        return valid(
            "asgn_amt", self.vl_new_amt, f_to, f_frm, s_args=(f_frm), f_say="nt_engh", fs_args=(f_to, f_frm), num=True
        )

    # VALIDATION FNS

    def in_list_cs(self, val, list_):
        return self.in_list(val, list_, case_sens=True)

    def in_list(self, val, list_, case_sens=False):
        return val in list_ if case_sens else val.upper() in [i.upper() for i in list_]

    def vl_new_cat(self, val):
        return val and not self.cat_exists(val)

    def vl_new_amt(self, val, fund_from=""):
        return not fund_from or val > self.cat_value(fund_from)

    def cat_exists(self, category):
        return category in ["Misc"] + [b.category for b in self.budgets]

    def cat_not_exists(self, category):
        return not self.cat_exists(category)

    def save_file_exists(self, filename):
        return filename in [filenames for _, _, filenames in walk(self.sav_dir)][0]

    # COMMANDS

    def print_commands(self):
        say("i_commands", ", ".join(self.commands.keys()))

    def print_budgets(self):
        print("")
        say("b_balances_are")
        say("total_at_start", self.total_input_money)
        for b in self.budgets:
            print(f"    {b.category}: {b.value}")
        say("b_total", sum([b.value for b in self.budgets]), wait=False)
        print("")

    def transfer(self):
        budget_from = valid("tr_which_from", self.cat_exists, f_say="not_cat")
        budget_to = valid("tr_which_to", self.cat_exists, f_say="not_cat")
        amount = ask("tr_how_much", num=True)
        self.cat_adjust(budget_from, -amount)
        self.cat_adjust(budget_to, amount)
        say("tr_success", amount, budget_from, budget_to)

    def spend(self):
        spent_from = valid("sp_which", self.cat_exists, f_say="not_cat")
        amount = ask("sp_how_much", num=True)
        self.cat_adjust(spent_from, -amount)
        say("sp_success", amount, spent_from, self.cat_value(spent_from))

    def add_money(self):
        add_to = valid("am_which_to", self.cat_exists, f_say="not_cat")
        amount = ask("am_how_much", add_to, num=True)
        self.cat_adjust(add_to, amount)
        self.total_input_money += amount
        say("am_success", amount, add_to)

    def route_new_budget(self):
        choice = valid("rb_new_or_split", self.in_list, ["NEW", "SPLIT"], f_say="rb_not_n_or_s")
        if choice.upper() == "NEW":
            self.add_new_budget()
        elif choice.upper() == "SPLIT":
            self.div_budget()

    def div_budget(self):
        budget_from = ask("div_which_from")
        new_cat = valid("enter_cat", self.vl_new_cat, f_say="name_unavailable")
        new_amt = self.get_new_amt(new_cat, budget_from)

        self.cat_adjust(budget_from, -new_amt)
        self.budgets.append(Budget(new_cat, new_amt))
        say("div_success", new_cat, new_amt, budget_from)

    def add_new_budget(self):
        new_cat = valid("enter_cat", self.vl_new_cat, f_say="name_unavailable")
        new_amt = self.get_new_amt(new_cat)
        self.budgets.append(Budget(new_cat, new_amt))
        say("ab_success", new_cat, new_amt)

    def save_to_file(self):
        save_name = ask("sv_save_name")
        if self.save_file_exists(save_name):
            yn = valid("sv_ovrwrt", self.in_list, ["Y", "N"], s_args=(save_name), f_ask="i_nt_yn")
            if yn.upper() == "N":
                return

        with open(f"{self.sav_dir}/{save_name}", "w") as f:
            f.write(repr(self))
        self.filename = save_name
        say("sv_file_saved", save_name)

    def load_chooser(self, load_file=""):
        if not load_file:
            load_file = ask("ld_load_file")
            while not self.save_file_exists(load_file):
                load_file = ask("ld_not_a_file", load_file)
                if load_file == "CANCEL":
                    return load_file
            return load_file

    # APP

    def set_exit(self):
        say("app_goodbye", self.username)
        self.exit = True

    def route_command(self, command):
        if command.upper() not in self.commands.keys():
            say("i_not_command")
            return

        self.commands[command.upper()]()

    def run(self):
        if self.setup_done:
            say("app_welcome_back", self.username)
            self.print_budgets()
        else:
            say("app_welcome")

        while not self.setup_done:
            new_or_load = valid("nw_or_ld", self.in_list, ["NEW", "LOAD"], f_ask="not_n_or_l")

            if new_or_load.upper() == "NEW":
                self.setup()

            elif new_or_load.upper() == "LOAD":
                load_file = self.load_chooser()
                if load_file != "CANCEL":
                    return BudgetApp(load_file)

        while not self.exit:
            self.route_command(ask("i_what_do"))
