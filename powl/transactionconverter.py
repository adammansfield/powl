"""Provides conversion for transaction data into an exchange format."""

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
            Map of account key to files.
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

        Raises
        ------
        ValueError
            If an account key that exists in filenames or account_types
            does not exist in any of assets, liabilities, revenues, or
            expenses.

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

        self._accounts = dict(self.assets.items() +
                              self.liabilities.items() +
                              self.revenues.items() +
                              self.expenses.items())

        for key in self._files:
            if key not in self._account_types:
                raise KeyError(
                    "Key ({0}) in files ".format(key) +
                    "does not have a corresponding key in account_types.")
            if key not in self._accounts:
                raise KeyError(
                    "Key ({0}) in files ".format(key) +
                    "does not have a corresponding key in any of assets, " +
                    "liabilities, revenues, or expenses.")

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
        qif_date = self._convert_date(date)
        qif_transfer = self._get_transfer_account(debit, credit)
        qif_amount = self._convert_amount(debit, credit)
        qif_memo = memo
        qif_record = self._format_qif_transaction(qif_date,
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

    # QIF FILE FORMATTING
    def _get_templates(self):
        templates = []
        for key, filename in self.filenames.iteritems():
            account_name = self.accounts.get(key)
            account_type = self.types.get(key)
            header = self.format_qif_header(account_name, account_type)
            template = (filename, header)
            templates.append(template)
        return templates

    def _format_qif_record(self, date, transfer, amount, memo):
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

    # QIF RECORD CONVERSION
    def _convert_amount(self, debit, amount):
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

        if debit in self.expenses:
            # Amount should be negative.
            return '-' + formatted_amount
        else if debit in self.accounts:
            return formatted_amount
        else:
            raise KeyError("account key ({0}) does not exist".format(debit))

    def _convert_date(self, date):
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
        except TypeError as err:
            raise TypeError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {1}".format(err.message))
        except ValueError as e:
            raise ValueError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {1}".format(err.message))
        except OverflowError as e:
            raise OverflowError(
                "date ({0}) cannot be converted to MM/DD/YYYY ".format(date) +
                "because {1}".format(err.message))

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
        """
        if debit in self._files:
            return self._files[debit]
        else if credit in self._files:
            return self._files[credit]
        else:
            raise KeyError(
                "neither debit key ({0}) ".format(debit) +
                "or credit key ({0}) ".format(credit) +
                "has an associated QIF file")

    def _get_transfer_account(self, debit, credit):
    # TODO: add explanation for transfer account.
        """Convert transfer account based on debit and credit."""
        self.validate_file(debit, credit)
        if debit in self.filenames:
            return self.accounts[credit]
        else:
            return self.accounts[debit]

    # LOGGING
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

