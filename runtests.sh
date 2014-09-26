#!/bin/sh
echo "powl.action"
echo "-----------"
python test/action.test.py

echo "\n"
echo "powl.exception"
echo "--------------"
python test/exception.test.py

echo "\n"
echo "powl.parser"
echo "-----------"
python test/parser.test.py

echo "\n"
echo "powl.transactionconverter"
echo "-------------------------"
python test/transactionconverter.test.py

