#!/bin/sh
echo "powl.action"
echo "-----------"
python test/small/action.test.py

echo "\n"
echo "powl.actionretriever"
echo "--------------------"
python test/small/actionretriever.test.py

echo "\n"
echo "powl.exception"
echo "--------------"
python test/small/exception.test.py

echo "\n"
echo "powl.parser"
echo "-----------"
python test/small/parser.test.py

echo "\n"
echo "powl.transactionconverter"
echo "-------------------------"
python test/small/transactionconverter.test.py

