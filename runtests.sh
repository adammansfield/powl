#!/bin/sh
echo
echo "powl.action"
echo "==========="
python test/action.test.py

echo
echo "powl.main"
echo "========="
python test/main.test.py

echo
echo "powl.parser"
echo "==========="
python test/parser.test.py

echo
echo "powl.transactionconverter"
echo "========================="
python test/transactionconverter.test.py

