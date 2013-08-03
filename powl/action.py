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


class AccountingAction(Action):

    def __init__(self, log, parser, filenames, types, assets, liabilities, revenues, expenses):
        """
        Args:
            log (powl.parser.BodyCompositionDataParser): Used to parse input string.
            log (powl.parser.BodyCompositionDataParser): Used to parse input string.
            file_object (powl.filesystem.File): Output file.
        """
        self.filenames = filenames
        self.types = types
        self.assets = assets
        self.liabilities = liabilities
        self.revenues = revenues
        self.expenses = expenses
        self.accounts = dict(self.assets.items() +
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
        debit, credit, amount, memo = self._parse_message(self._input_data)

        if self.valid_transaction(date, debit, credit, amount):
            qif_date = self.qif_convert_date(date)
            qif_filename = self.qif_convert_filename(debit, credit)
            qif_transfer = self.qif_convert_transfer(debit, credit)
            qif_amount = self.qif_convert_amount(debit, amount)
            qif_memo = memo
            qif_transaction = self.qif_format_transaction(qif_date,
                                                          qif_transfer,
                                                          qif_amount,
                                                          qif_memo)
            self.log_transaction(qif_date,
                                 qif_filename,
                                 qif_transfer,
                                 qif_amount,
                                 qif_memo)
            self._output_filepath = qif_filename
            self._output_data = qif_transaction
        else:
            # TODO: return an error for powl.py to handle
            self.log_transaction_error(date, debit, credit, amount, memo)
            self._output_filepath = ""
            self._output_data = ""

    def _parse_message(self, data):
        """Parse a transaction data into debit, credit, amount and memo."""
        debit = ''
        credit = ''
        amount = ''
        memo = ''
        params = re.split('-', data)
        for param in params:
            if re.match('^d', param):
                debit = re.sub('^d', '', param)
            elif re.match('^c', param):
                credit = re.sub('^c', '', param)
            elif re.match('^a', param):
                amount = re.sub('^a', '', param)
            elif re.match('^m', param):
                memo = re.sub('^m', '', param)
                memo = memo.replace("\"", '')
        debit = debit.strip()
        credit = credit.strip()
        amount = amount.strip()
        memo = memo.strip()
        return debit, credit, amount, memo


    def get_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self.qif_format_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates


    # VALIDITY
    def valid_accounts(self, debit, credit):
        """Check if both accounts are valid."""
        if debit in self.accounts and credit in self.accounts:
            return True
        else:
            return False

    def valid_amount(self, amount):
        """Check if amount is valid."""
        try:
            float(amount)
            return True
        except ValueError:
            return False

    def valid_date(self, date):
        """Check if date is valid."""
        try:
            time.mktime(date)
            return True
        except (TypeError, OverflowError, ValueError):
            return False


    def valid_file(self, debit, credit):
        """Check if one of the accounts is a file for qif."""
        if debit in self.filenames or credit in self.filenames:
            return True
        else:
            return False

    def valid_transaction(self, date, debit, credit, amount):
        """Check if the transaction is valid for qif formatting."""
        valid_accounts = self.valid_accounts(debit, credit)
        valid_amount = self.valid_amount(amount)
        valid_date = self.valid_date(date)
        valid_file = self.valid_file(debit, credit)
        return valid_accounts and valid_amount and valid_date and valid_file

    # QIF FORMATTING
    def qif_format_transaction(self, date, transfer, amount, memo):
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

    def qif_format_header(self, account_name, account_type):
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
    def qif_convert_amount(self, debit, amount):
        """Convert amount based on debit."""
        if debit in self.expenses:
            return '-' + amount
        else:
            return amount

    def qif_convert_date(self, date):
        """Convert struct_time to qif date format."""
        return time.strftime('%m/%d/%Y', date)

    def qif_convert_filename(self, debit, credit):
        """Convert filename based on debit and credit."""
        if debit in self.filenames:
            return self.filenames.get(debit)
        else:
            return self.filenames.get(credit)

    def qif_convert_transfer(self, debit, credit):
        """Convert transfer account based on debit and credit."""
        if debit in self.filenames:
            return self.accounts.get(credit)
        else:
            return self.accounts.get(debit)

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
