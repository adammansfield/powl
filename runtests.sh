#!/bin/sh
echo
echo "main.py"
echo "======="
python test/main.test.py

echo
echo "parser.py"
echo "========="
python test/parser.test.py

echo
echo "transactionconverter.py"
echo "======================="
python test/transactionconverter.test.py

