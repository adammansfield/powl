"""Provides classes to perform specific actions."""
import time

class Action(object):
    """
    Provides methods to do an action with given data.
    """
    
    def do(self, string, date):
    """
    Perform an action on the given string.
    
    Args:
        string (str): A string collection of attributes for the specific action.
        date (datetime.date): Date associated with the action.
    """
        pass
                             
                             
class BodyCompositionAction(Action):
    """
    Performs a body composition action.
    """
    
    _OUTPUT_DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, parser, file_object):
        """
        Args:
            parser (powl.parser.BodyCompositionDataParser): Used to parse input string.
            file_object (powl.filesystem.File): Output file.
        """
        self._parser = parser
        self._file = file_object

    def do(self, string, date):
        """
        Output body composition to file.
        
        Args:
            string (string): Formatted string containing mass and fat percentage.
            date (datetime.date): Date associated with the action.
        """
        data = self._parser.parse(string)

        output = "{0}, {1}, {2}".format(
            time.strftime(self._OUTPUT_DATE_FORMAT, date),
            data.mass,
            data.fat_percentage)

        self._file.append_line(output)
        self._log.info(
            "Performed body composition action. Outputted '%s' to '%s'",
            string,
            self._file.filename)


class NoteAction(Action):
    """
    Performs a body composition action.
    """

    def __init__(self, log, file_object):
        """
        Args:
            log (powl.logwriter.LogWriter): Used to log.
            file_object (powl.filesystem.File): Output file.
        """
        self._log = log
        self._file = file_object

    def do(self, string, date):
        """
        Output the note to file.

        Args:
            string (string): Note to output to file.
            date (datetime.date): Date associated with the action.
        """
        self._file.append_line(string)
        self._log.info(
            "Performed note action. Outputted '%s' to '%s'",
            string,
            self._file.filename)


class TransactionAction(Action):

    class _QifTransactionData(object):
        """
        Data used to write a transaction for a QIF file.
        
        Attributes:
            qif_file (powl.filesystem.File): Output file.
            transfer_account (string): Transfer account.
            date (string): Date in the MM/DD/YYYY format.
            amount (string): Positive or negative dollar amount.
            memo (string): Description of the transaction.
        """
        
        def __init__(self, qif_file = None, transfer_account = "", date = "", amount = "", memo = ""):
            self.qif_file = qif_file
            self.transfer_account = transfer_account
            self.date = date
            self.amount = amount
            self.memo = memo


    def __init__(self, log, parser, files, account_types, assets, liabilities, revenues, expenses):
        """
        Args:
            log (powl.logwriter.LogWriter): Used to log.
            parser (powl.parser.AccountingDataParser): Used to parse input string.
            files (list of powl.filesystem.File): Output files.
            account_type (dict): 
        """
        self._log = log
        self._parser = parser
        self._files = files
        self._account_types = account_types
        self._assets = assets
        self._liabilities = liabilities
        self._revenues = revenues
        self._expenses = expenses

        self._accounts = dict(self.assets.items() +
                              self.liabilities.items() +
                              self.revenues.items() +
                              self.expenses.items())
                             
    def do(self, string, date):
        """
        Output accounting transaction to a QIF file.
        
        Args:
            string (string): Formatted string containing debit, credit, amount, and memo.
            date (datetime.date): Date of the transaction.
        """
        data = self._parser.parse(string)
        transaction_data = self._convert_to_qif(data)
        transaction_string = self._format_qif_transaction(transaction_data)

        transaction_data.qif_file.append_line(transaction_string)
        self._log_transaction(transaction)

    def _convert_to_qif(self, data):
        """
        Parse a transaction data into debit, credit, amount and memo.
        """
        transaction = _QifTransactionData()

        transaction.amount = self.convert_amount_to_qif(data.debit, data.amount)
        transaction.date = self.convert_date_to_qif(data.date)
        transaction.memo = data.memo
        transaction.qif_file = self.get_qif_file(debit, credit)
        transaction.transfer_account = self.get_qif_transfer_account(debit, credit)

        return transaction


    def get_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self.format_qif_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates


    # QIF FORMATTING
    def format_qif_transaction(self, date, transfer, amount, memo):
        """Formats qif data into a transaction for a QIF file."""
        data = { 'date': date,
                 'amount': amount,
                 'transfer': transfer,
                 'memo': memo }
        transaction = textwrap.dedent("""\
            D{date}
            T{amount}
            L{transfer}
            M{memo}
            ^""".format(**data))
        return transaction

    def format_qif_header(self, account_name, account_type):
        """Format an account name and type into a header for a QIF file."""
        data = { 'name': account_name, 'type': account_type }
        header = textwrap.dedent("""\
            !Account
            N{name}
            T{type}
            ^
            !Type:{type}""".format(**data))
        return header

    # QIF CONVERSION
    def convert_amount_to_qif(self, debit, amount):
        """Convert amount based on debit."""
        try:
            float(amount)
        except ValueError as error:
            raise 

        if debit in self.expenses:
            return '-' + amount
        else:
            return amount

    def convert_date_to_qif(self, date):
        """Convert struct_time to qif date format."""
        try:
            time.mktime(date)
        except (TypeError, OverflowError, ValueError) as error:
            raise

        return time.strftime('%m/%d/%Y', date)

    def get_qif_file(self, debit, credit):
        """Convert filename based on debit and credit."""
        if debit in self.filenames:
            return self.files.get(debit)
        elif credit in self.filenames:
            return self.files.get(credit)
        else:
            raise ValueError("Debit or credit not in filenames.")

    def get_transfer_account(self, debit, credit):
        """Convert transfer account based on debit and credit."""
        if debit in self.filenames:
            return self.accounts[credit]
        else credit in self.filenames:
            return self.accounts[debit]
        else:
            raise ValueError("Debit or credit not in filenames.")

    # LOGGING
    def log_transaction(self, date, path, transfer, amount, memo):
        """Logs the transaction."""
        filename = os.path.basename(path)
        logindent = '\t\t\t\t  '
        # TODO: use textwrap.dedent
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}file: {1}{2}".format(logindent, filename, os.linesep) +
                  "{0}transfer: {1}{2}".format(logindent, transfer, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        logger.info(logmsg)

    def log_transaction_error(self, date, debit, credit, amount, memo):
        """Logs the transaction."""
        date = time.strftime('%m/%d/%Y', date)
        logindent = '\t\t\t\t  '
        # TODO: use textwrap.dedent
        logmsg = ("TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}debit: {1}{2}".format(logindent, debit, os.linesep) +
                  "{0}credit: {1}{2}".format(logindent, credit, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        logger.error(logmsg)
