#!/bin/sh
export PYTHONPATH=.
echo
echo "Transaction Processor Tests"
echo "==========================="
python powl/tests/test_processor_transaction.py
#echo
#echo "Parse Tests"
#echo "==========="
#python powl/tests/test_processor_action.py
