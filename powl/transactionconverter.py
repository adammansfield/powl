"""Provides conversion for transaction data into an exchange format."""
import textwrap
import time

class TransactionConverter(object):
    """
    Provides methods to convert data into a financial exchange format.
    """

    def convert(self, date, debit, credit, amount, memo):
        """
        Convert a transaction into an exchange financial format.

        Parameters
        ----------
        date : time.struct_time
            Date of the transaction.
        debit : str
            Debit account of the transaction.
        credit : str
            Credit account of the transaction.
        amount : float
            Amount of the transaction.
        memo : str
            Description of the transaction.
        """
        pass


class QifConverter(TransactionConverter):
    """
    Provides methods to convert a transaction into QIF format.
    """

    def __init__(self, log, files, account_types, assets, liabilities,
                 revenues, expenses):
        """
        Parameters
        ----------
        log : powl.logwriter.Log
            Used to log.
        files : dict of powl.filesystem.File
            Map of account key to files. Every key in files must exist in
            either of assets, liabilities, revenues, or expenses.
        account_types : dict
            Map of account key to QIF account types.
        assets : dict
            Map of account key to Assets.
        liabilities : dict
            Map of account key to Liabilitess.
        revenues : dict
            Map of account key to Revenuess.
        expenses : dict
            Map of account key to Expensess.

        Notes
        -----
        An account key is a string that maps to a QIF account.
        Multiple account key words can map to the same account.
        For example "ent" can map to "Expenses:Entertainment" and
        "entertainment" can also map to "Expenses:Entertainment".
        """
        self._log = log
        self._files = files
        self._account_types = account_types
        self._assets = assets
        self._liabilities = liabilities
        self._revenues = revenues
        self._expenses = expenses

        self._accounts = dict(
            self._assets.items() +
            self._liabilities.items() +
            self._revenues.items() +
            self._expenses.items())

        for key, value in self._files.items():
            if key not in self._accounts.keys():
                raise KeyError(
                    "account key ({0}) ".format(key) +
                    "for file ({0}) ".format(value.filename) +
                    "does not have has an associated QIF account")

    def convert(self, date, debit, credit, amount, memo):
        """
        Convert transaction data into QIF format.

        Parameters
        ----------
        date : time.struct_time
            Date of the transaction.
        debit : str
            Debit account of the transaction.
        credit : str
            Credit account of the transaction.
        amount : float
            Amount of the transaction.
        memo : str
            Description of the transaction.

        Returns
        -------
        record : str
            QIF record of the transaction.
        qif_file : powl.filesystem.File
            The QIF file to output to.

        Notes
        -----
        Since it depends which QIF file records the transaction, the return
        value also contains the file to write to.
        """
        qif_date = self._format_date(date)
        qif_transfer = self._get_transfer_account(debit, credit)
        qif_amount = self._format_amount(debit, amount)
        qif_memo = memo
        qif_record = self._format_qif_record(
            qif_date,
            qif_transfer,
            qif_amount,
            qif_memo)
        qif_file = self._get_qif_file(debit, credit)

        self._log_transaction(
            qif_date,
            qif_file.filename,
            qif_transfer,
            qif_amount,
            qif_memo)
        return qif_record, qif_file

    def _create_qif_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self._format_qif_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates

    def _format_amount(self, debit, amount):
        """
        Convert amount to QIF format based on debit.

        Parameters
        ----------
        debit : str
            Account key for the debit of a transaction.
        amount : str or float
            Amount of the transaction.

        Returns
        -------
        str
            Formatted amount to use in QIF file.

        Raises
        ------
        ValueError
            If amount cannot be converted to a float.
        KeyError
            If debit key is not an account.
        """
        try:
            formatted_amount = "{0:.2f}".format(float(amount))
        except ValueError:
            raise ValueError(
                "amount ({0}) cannot be converted to float".format(amount))

        if debit in self._expenses:
            # Amount should be negative.
            return '-' + formatted_amount
        elif debit in self._accounts:
            return formatted_amount
        else:
            raise KeyError("account key ({0}) does not exist".format(debit))

    def _format_date(self, date):
        """
        Convert struct_time to QIF date format (MM/DD/YYYY).

        Parameters
        ----------
        date : time.struct_time
            The date of the transaction.

        Returns
        -------
        str
            String date in the format of "MM/DD/YYYY".

        Raises
        ------
        TypeError
            If date is not a struct_time.
        ValueError
            If a date value is out of range.
        OverflowError
            If a value in the tuple is too large to be stored in a C long.
        """
        try:
            return time.strftime("%m/%d/%Y", date)
        except TypeError as e:
            raise TypeError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {0}".format(e.message))
        except ValueError as e:
            raise ValueError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {0}".format(e.message))
        except OverflowError as e:
            raise OverflowError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {0}".format(e.message))

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

    def _format_qif_record(self, date, transfer, amount, memo):
        """
        Formats qif data into a transaction for a QIF file.

        Parameters
        ----------
        date : str
            Date of the transaction
        transfer : str
            Transfer QIF account.
        amount : str
            Formatted amount.
        memo : str
            Description of the transaction.
        """
        return textwrap.dedent(
            """\
            D{0}
            T{1}
            L{2}
            M{3}
            ^""".format(date, amount, transfer, memo))


    def _get_qif_file(self, debit, credit):
        """
        Get the associated QIF file from the debit and credit keys.

        Parameters
        ----------
        debit : str
            Account key for the debit of a transaction.
        credit : str
            Account key for the credit of a transaction.

        Raises
        ------
        KeyError
            If neither key has an associated QIF file.

        Notes
        -----
        Debit key has priority so if both debit and credit key has an
        associated QIF file than the QIF file associated with the debit
        key is returned.

        This is linked with get_transfer_account. If the QIF file returned
        from this is from the debit key then the transfer account must be
        from the credit key and vice versa.
        """
        if debit in self._files:
            return self._files[debit]
        elif credit in self._files:
            return self._files[credit]
        else:
            raise KeyError(
                "neither debit key ({0}) ".format(debit) +
                "or credit key ({0}) ".format(credit) +
                "has an associated QIF file")

    def _get_transfer_account(self, debit, credit):
        """
        Get the associated QIF account from the debit and credit keys.

        Parameters
        ----------
        debit : str
            Account key for the debit of a transaction.
        credit : str
            Account key for the credit of a transaction.

        Raises
        ------
        KeyError
            If neither key has an associated QIF file.
            If neither key has an associated QIF account.

        Notes
        -----
        Credit key has priority so if both debit and credit key has an
        associated QIF account than the QIF account associated with the
        credit key is returned.

        This is linked with get_qif_file. If the transfer account returned
        from this is from the credit key then the QIF file must be from the
        debit key and vice versa.
        """
        if debit in self._files:
            key = credit
        elif credit in self._files:
            key = debit
        else:
            raise KeyError(
                "neither debit key ({0}) ".format(debit) +
                "or credit key ({0}) ".format(credit) +
                "has an associated QIF file")

        if key in self._accounts:
            return self._accounts[key]
        else:
            raise KeyError(
                "account key ({0}) ".format(key) +
                "does not have has an associated QIF account")

    def _log_transaction(self, date, filename, transfer, amount, memo):
        """
        Debug logs the transaction.

        Parameters
        ----------
        date : str
            Date of the transaction
        filename : str
            Name of the QIF file.
        transfer : str
            Transfer QIF account.
        amount : str
            Formatted amount.
        memo : str
            Description of the transaction.
        """
        self._log.debug("QIF transaction:")
        self._log.debug("   date:     %s", date)
        self._log.debug("   file:     %s", filename)
        self._log.debug("   transfer: %s", transfer)
        self._log.debug("   amount:   %s", amount)
        self._log.debug("   memo:     %s", memo)

