#!/bin/sh
echo
echo "Processor - Transaction"
echo "======================="
python powl/test/test_processor.py
echo
echo "Processor - Transaction"
echo "======================="
python powl/test/test_transaction.py
echo
echo "Mail"
echo "===="
python powl/test/test_mail.py
