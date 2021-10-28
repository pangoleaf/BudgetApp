from time import sleep

script = {
    # setup
    "app_welcome": "Welcome to BudgetApp!",
    "app_welcome_back": "Hi [[[0]]]! Welcome back to BudgetApp!",
    "app_goodbye": "Goodbye [[[0]]]!",
    "su_what_name": "First of all, what's your name?",
    "su_how_much_total": "Hi [[[0]]], how much money do you want to budget with in total this month?",
    "su_first_cat": "Now choose your first category to budget for (HINT: Food is pretty important)",
    "su_next_cat": "Now choose another category (or type DONE to assign remaining money to Misc)",
    "su_commands": "While you're using this app, you can type in the following commands:",
    "remaining_total": "[[[0]]] left to assign to budgets",
    "enter_category": "Enter new budget category",
    "assign_amount": "Enter amount to assign to [[[0]]]",
    "not_enough": "Sorry, you don't have enough money left in [[[0]]] to add that much to [[[1]]]",
    "name_unavailable": "Sorry, that name is invalid or already reserved",
    "creating_misc": "Creating Misc budget with remaining money of value [[[0]]]",
    "i_gt_zero": "Must be a positive value, try again...",
    "i_needs_num": "I need that to be a number, try again...",
    "i_must_be_y_n": "That's got to be Y or N. Try again...",
    "i_what_do": "What can I do for you? (type COMMANDS to see available commands)",
    "i_commands": "Available commands are: [[[0]]]",
    "i_not_command": "Command not found. Make sure you're spelling it right.",
    "b_balances_are": "Currently, your budgets look like this:",
    "b_unbudgeted": "Unbudgeted: [[[0]]]",
    "b_total": "Total: [[[0]]]",
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
    "div_which_from": "Which budget would you like to use money from?",
    "div_success": "New budget [[[0]]] created with [[[1]]] assigned to it from [[[2]]]",
    "rb_new_or_split": "Would you like to make a new budget with new funds (type NEW), or split funds off an existing budget (type SPLIT)?",
    "sv_save_name": "What would you like to name your save file?",
    "sv_overwrite": "[[[0]]] exists, confirm overwrite? Y/N",
    "sv_file_saved": "Budgets saved as [[[0]]]",
    "new_or_load": "Would you like to start a new set of budgets or load from a file? Type NEW or LOAD",
    "not_new_or_load": "Command needs to be either NEW or LOAD, try again...",
    "ld_load_file": "What is the name of the file you would like to load?",
    "ld_not_a_file": "Sorry, [[[0]]] is not an existing saved file, try again... (or type CANCEL to cancel loading)",
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
            say("i_needs_num")
            return ask(key, *args, num=True)

        if given < 0:
            say("i_gt_zero")
            return ask(key, *args, num=True)
    return given
    

## perhaps an ask_while_not function which takes a check function, script, script_fail, parameters