#!/bin/sh
echo "powl.action:"
python test/action.test.py

echo "\n"
echo "powl.parser:"
python test/parser.test.py

echo "\n"
echo "powl.transactionconverter:"
python test/transactionconverter.test.py

