"""Provides classes to store data for actions."""


class AccountingData(object):
    """
    Data used for the accounting action.
    
    Attributes:
        debit (string): Debit account.
        credit (string): Credit account.
        amount (string): Dollar amount.
        memo (string): Transaction description.
    """
    
    def __init__(self, debit = "", credit = "", amount = "", memo = ""):
        self.debit = debit
        self.credit = credit
        self.amount = amount
        self.memo = memo
        
        
class BodyCompositionData(object):
    """
    Data used for the body composition action.
    
    Attributes:
        mass (float): Mass in pounds.
        fat_percentage (float): Body fat percentage.
    """

    def __init__(self, mass = 0.0, fat_percentage = 0.0):
        self.mass = mass
        self.fat_percentage = fat_percentage
