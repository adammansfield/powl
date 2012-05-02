#!/bin/sh
export PYTHONPATH=.
echo
echo "Transaction Processor Tests"
echo "==========================="
python powl/tests/test_TransactionProcessor.py
echo
echo "Parse Tests"
echo "==========="
python powl/tests/test_Parse.py
