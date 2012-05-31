#!/bin/sh
echo
echo "Processor - Transaction"
echo "======================="
python powl/test/test_processor_transaction.py
echo
echo "Mail"
echo "===="
python powl/test/test_mail.py
