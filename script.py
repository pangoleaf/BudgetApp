from time import sleep

script = {
    # setup
    "welcome": "Welcome to BudgetApp! First of all, what's your name?",
    "how_much_total": "Hi [[[0]]], how much money do you want to budget with in total this month?",
    "first_cat": "Now choose your first category to budget for (HINT: Food is pretty important)",
    "next_cat": "Now choose another category (or type DONE to assign remaining money to Misc)",
    "remaining_total": "[[[0]]] left to assign to budgets",
    "enter_category": "Enter budget category",
    "assign_amount": "Enter amount to assign to [[[0]]]",
    "not_enough": "Sorry, you dont have enough money left to add that much to [[[0]]]",
    "name_unavailable": "Sorry, that name is already reserved",
    "creating_misc": "Creating Misc budget with remaining money of value [[[0]]]",
    "needs_num": "I need that to be a number, try again...",
    "what_do": "So what can I do for you? (type COMMANDS to see available commands)",
    "not_command": "Command not found. Make sure you're using ALL CAPS and spelling it right.",
    "balances_are": "Currently, your budgets look like this:",
    "tr_which_from": "Which budget category would you like to transfer from?",
    "tr_which_to": "Which budget category would you like to transfer to?",
    "tr_how_much": "How much would you like to transfer?",
    "tr_success": "Successfully transferred [[[0]]] from [[[1]]] to [[[2]]].",
    "sp_which": "Which budget category have you spent from?",
    "sp_how_much": "How much did you spend?",
    "sp_success": "[[[0]]] has been removed, [[[1]]] remaining in [[[2]]]",
    "ab_success": "New budget [[[0]]] added with [[[1]]] available to spend",
    "am_which_to": "Which budget would you like to add money too?",
    "am_how_much": "How much do you want to add to [[[0]]]",
    "am_success": "[[[0]]] added to [[[1]]]",
}


def get_text(key, *args):
    try:
        output = script[key]
        for i, arg in enumerate(args):
            output = output.replace(f"[[[{i}]]]", str(arg))
    except KeyError:
        output = key
    sleep(1)
    return output


def say(key, *args):
    print(f"{get_text(key, *args)}")


def ask(key, *args, num=False):
    given = input(f"{get_text(key, *args)}: ")
    if num:
        try:
            given = int(given)
        except ValueError:
            say("needs_num")
            return ask(key, *args, num=True)
    return given
