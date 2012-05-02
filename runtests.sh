#!/bin/sh
echo
echo "Transaction Processor Tests"
echo "==========================="
python -m tests.test_TransactionProcessor
echo
echo "Parse Tests"
echo "==========="
python -m tests.test_Parse
