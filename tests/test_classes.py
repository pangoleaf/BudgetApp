from classes import Budget, BudgetApp

def test_Budget():
    b = Budget("Food", 50)
    assert b.category == "Food"
    assert b.value == 50

    b.adjust(-20)
    assert b.category == "Food"
    assert b.value == 30

    b.adjust(-20)
    assert b.category == "Food"
    assert b.value == 30
