from dataclasses import dataclass, field
from os import walk
from script import say, ask, validated

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
        self.budgets = [Budget("Unbudgeted", self.total_input_money)]

        say("su_first_cat")
        self.add_budget_initial()

        keep_asking = True
        while keep_asking and self.cat_value("Unbudgeted") > 0:
            say("su_next_cat")
            new = self.add_budget_initial()
            keep_asking = new != "DONE"

        if self.cat_value("Unbudgeted") > 0:
            say("creating_misc", self.cat_value("Unbudgeted"))
            self.budgets.append(Budget("Misc", self.cat_value("Unbudgeted")))
        self.budgets.remove([b for b in self.budgets if b.category == "Unbudgeted"][0])

        self.setup_done = True

        self.print_budgets()
        say("su_commands")
        self.print_commands()

    def add_budget_initial(self):
        new_bud_cat = self.new_budget_cat_name()

        if new_bud_cat == "DONE":
            return "DONE"

        new_bud_value = self.new_budget_value(new_bud_cat, "Unbudgeted")

        self.budgets.append(Budget(new_bud_cat, new_bud_value))
        say("ab_success", new_bud_cat, new_bud_value)

        self.cat_adjust("Unbudgeted", -new_bud_value)
        say("remaining_total", self.cat_value("Unbudgeted"))
        return new_bud_cat

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

    def val_in_list(self, val, list):
        return val in list

    def in_budgets(self, category):
        return category in ["Misc"] + [b.category for b in self.budgets]

    def choose_existing(self, script):
        chosen = ask(script)
        while not self.in_budgets(chosen):
            say("not_a_budget")
            chosen = ask(script)
        return chosen

    def cat_value(self, cat):
        return [b for b in self.budgets if b.category == cat][0].value

    def cat_adjust(self, cat, amount):
        [b for b in self.budgets if b.category == cat][0].adjust(amount)

    def new_budget_cat_name(self):
        new_bud_cat = ask("enter_category")
        while not new_bud_cat or self.in_budgets(new_bud_cat):
            say("name_unavailable")
            new_bud_cat = ask("enter_category")
        return new_bud_cat

    def new_budget_value(self, fund_to, fund_from=""):
        new_bud_value = ask("assign_amount", fund_to, num=True)
        while fund_from and new_bud_value > self.cat_value(fund_from):
            say("not_enough", fund_from, fund_to)
            new_bud_value = ask("assign_amount", fund_to, num=True)
        return new_bud_value
    
    def save_file_exists(self, filename):
        return filename in [filenames for _, _, filenames in walk(self.sav_dir)][0]

    # COMMANDS

    def print_commands(self):
        say("i_commands", ", ".join(self.commands.keys()))

    def print_budgets(self):
        say("b_balances_are")
        for b in self.budgets:
            print(f"    {b.category}: {b.value}")
        say("b_total", sum([b.value for b in self.budgets]))

    def transfer(self):
        budget_from = self.choose_existing("tr_which_from")
        budget_to = self.choose_existing("tr_which_to")
        amount = ask("tr_how_much", num=True)
        self.cat_adjust(budget_from, -amount)
        self.cat_adjust(budget_to, amount)
        say("tr_success", amount, budget_from, budget_to)

    def spend(self):
        spent_from = self.choose_existing("sp_which")
        amount = ask("sp_how_much", num=True)
        self.cat_adjust(spent_from, -amount)
        say("sp_success", amount, spent_from, self.cat_value(spent_from))

    def add_money(self):
        add_to = self.choose_existing("am_which_to")
        amount = ask("am_how_much", add_to, num=True)
        self.cat_adjust(add_to, amount)
        self.total_input_money += amount
        say("am_success", amount, add_to)

    def route_new_budget(self):
        choice = ""
        while choice not in ["NEW", "SPLIT"]:
            choice = ask("rb_new_or_split")
        if choice == "NEW":
            self.add_new_budget()
        elif choice == "SPLIT":
            self.div_budget()

    def div_budget(self):
        budget_from = ask("div_which_from")
        new_bud_cat = self.new_budget_cat_name()
        new_bud_value = self.new_budget_value(new_bud_cat, budget_from)

        self.cat_adjust(budget_from, -new_bud_value)
        self.budgets.append(Budget(new_bud_cat, new_bud_value))
        say("div_success", new_bud_cat, new_bud_value, budget_from)

    def add_new_budget(self):
        new_bud_cat = self.new_budget_cat_name()
        new_bud_value = self.new_budget_value(new_bud_cat)
        self.budgets.append(Budget(new_bud_cat, new_bud_value))
        say("ab_success", new_bud_cat, new_bud_value)
    
    def save_to_file(self):
        save_name = ask("sv_save_name")

        if self.save_file_exists(save_name):
            yn = ask("sv_overwrite", save_name).lower()
            while yn.lower() not in ["y", "n"]:
                yn = ask("i_must_be_y_n").lower()
            if yn == "n":
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
            self.print_commands()
            return

        self.commands[command.upper()]()

    def run(self):
        if self.setup_done:
            say("app_welcome_back", self.username)
            self.print_budgets()
        else:
            say("app_welcome")
        
        while not self.setup_done:
            new_or_load = ask("new_or_load").upper()
            while new_or_load not in ["NEW", "LOAD"]:
                say("not_new_or_load")
                new_or_load = ask("new_or_load").upper()
            
            if new_or_load == "NEW":
                self.setup()

            elif new_or_load == "LOAD":
                load_file = self.load_chooser()
                if load_file != "CANCEL":
                    return BudgetApp(load_file)
                
        while not self.exit:
            self.route_command(ask("i_what_do"))

