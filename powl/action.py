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
        string (str):
            A string collection of attributes for the specific action.
        date (datetime.date):
            Date associated with the action.
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
            parser (powl.parser.BodyCompositionDataParser):
                Used to parse input string.
            file_object (powl.filesystem.File):
                Output file.
        """
        self._parser = parser
        self._file = file_object

    def do(self, string, date):
        """
        Output body composition to file.
        
        Args:
            string (string):
                Formatted string containing mass and fat percentage.
            date (datetime.date):
                Date associated with the action.
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
            log (powl.logwriter.LogWriter):
                Used to log.
            file_object (powl.filesystem.File):
                Output file.
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
            output_file: Output file.
            transfer_account: Transfer account.
            date: Date in the MM/DD/YYYY format.
            amount: Positive or negative dollar amount.
            memo: Description of the transaction.
        """
        
        def __init__(self,
                     output_file = None,    # powl.filesystem.File
                     transfer_account = "", # str
                     date = "",             # str
                     amount = "",           # str
                     memo = ""):            # str
            self.output_file = output_file
            self.transfer_account = transfer_account
            self.date = date
            self.amount = amount
            self.memo = memo


    def __init__(self,
                 log,           # powl.logwriter.LogWriter
                 parser,        # powl.parser.TransactionParser
                 files,         # {str: powl.filesystem.File}
                 account_types, # {str: str}
                 assets,        # {str: str}
                 liabilities,   # {str: str}
                 revenues,      # {str: str}
                 expenses):     # {str: str}
        """
        Args:
            TODO: add args here
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
        # TODO: check to make sure that:
        #         1. each key in filenames exists as a key in accounts
        #         2. each key in account_types exists as a key in accounts
        #       else throw a KeyValue Error and write a test for this

                             
    def do(self,
           string, # str
           date):  # time.struct_time
        """
        Output accounting transaction to a QIF file.
        
        Args:
            string: Formatted string containing debit, credit,
                    amount, and memo.
            date: Date of the transaction.
        """
        data = self._parser.parse(string)
        qif_data = self._convert_to_qif(data)
        output = self._format_qif_transaction(transaction_data)

        qif_data.output_file.append_line(output)
        self._log_transaction(transaction)

    def _convert_to_qif(self, data):
        """
        Parse a transaction data into debit, credit, amount and memo.
        """
        transaction = _QifTransactionData()

        transaction.amount = self.convert_amount_to_qif(
            data.debit,
            data.amount)
        transaction.date = self.convert_date_to_qif(data.date)
        transaction.memo = data.memo
        transaction.qif_file = self.get_qif_file(debit, credit)
        transaction.transfer_account = self.get_qif_transfer_account(
            debit,
            credit)

        return transaction


    def _get_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self.format_qif_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates


    # QIF FORMATTING
    def _format_qif_transaction(self, date, transfer, amount, memo):
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

    def _format_qif_header(self, account_name, account_type):
        """Format an account name and type into a header for a QIF file."""
        data = { 'name': account_name, 'type': account_type }
        header = textwrap.dedent("""\
            !Account
            N{name}
            T{type}
            ^
            !Type:{type}""".format(**data))
        return header
    
    # VALIDITY
    def _validate_account(self, account):
        """
        Raise an exception if account is invalid.

        Args:
            account: Account to check.

        Raises:
            ValueError: If account does not exist.
        """
        if account not in self.accounts:
            raise ValueError("account ({0}) does not exist".format(account))

    def _validate_date(self, date):
        """
        Raise an exception if date is invalid.

        Args:
            date: Date to check.

        Raises:
            ValueError: if amount is invalid.
        """
        try:
            time.mktime(date)
        except ValueError:
            raise ValueError("date ({0}) is invalid".format(date))

    def _validate_file_exists(self, debit, credit):
        """
        Raise an exception if both debit and credit do not have a 
        corresponding file.
        
        Args:
            debit: Debit account.
            credit: Credit account.

        Raises:
            KeyError: if neither debit or credit has a corresponding file.
        """
        if debit not in self.filenames and
           credit not in self.filenames:
           raise KeyError(
               "debit ({0}) and credit ({1})".format(debit, credit) +
               "do not have a corresponding file")

    # QIF CONVERSION
    def convert_amount(self, debit, amount):        
        """
        Convert amount to QIF format based on debit.

        Args:
            debit: Debit account of the transaction.
            amount: Amount of the transaction.

        Returns:
            Formatted amount to use in QIF file.

        Raises:
            ValueError: If amount cannot be converted to a float.
            KeyError: If debit is not an account.
        """
        try:
            formatted_amount = "{0:.2f}".format(float(amount))
        except ValueError:
            raise ValueError(
                "amount ({0}) cannot be converted to float".format(amount))

        if debit in self.expenses:
            return "-{0}".format(formatted_amount)
        else if debit in self.accounts:
            return formatted_amount
        else:
            raise KeyError("account ({0}) does not exist".format(debit))

    def convert_date_to_qif(self, date):
        """Convert struct_time to qif date format."""
        self._validate_date(date)
        return time.strftime('%m/%d/%Y', date)

    def get_qif_file(self, debit, credit):
        """Convert filename based on debit and credit."""
        self._validate_debit_or_cred(debit, credit)
        if debit in self.filenames:
            return self.files.get(debit)
        else:
            return self.files.get(credit)

    def get_transfer_account(self, debit, credit):
        """Convert transfer account based on debit and credit."""
        self.validate_file(debit, credit)
        if debit in self.filenames:
            return self.accounts[credit]
        else:
            return self.accounts[debit]

    # LOGGING
    def log_transaction(self, date, path, transfer, amount, memo):
        """Logs the transaction."""
        filename = os.path.basename(path)
        logindent = '\t\t\t\t  '
        # TODO: use textwrap.dedent
        logmsg = (
            "TRANSACTION{0}".format(os.linesep) +
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
        logmsg = (
            "TRANSACTION{0}".format(os.linesep) +
                  "{0}date: {1}{2}".format(logindent, date, os.linesep) +
                  "{0}debit: {1}{2}".format(logindent, debit, os.linesep) +
                  "{0}credit: {1}{2}".format(logindent, credit, os.linesep) +
                  "{0}amount: {1}{2}".format(logindent, amount, os.linesep) +
                  "{0}memo: {1}{2}".format(logindent, memo, os.linesep))
        logger.error(logmsg)
