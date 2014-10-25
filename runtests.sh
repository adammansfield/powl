#!/bin/sh
echo "powl.action"
echo "-----------"
python test/small/test_action.py

echo "\n"
echo "powl.actionretriever"
echo "--------------------"
python test/small/test_actionretriever.py

echo "\n"
echo "powl.exception"
echo "--------------"
python test/small/test_exception.py

echo "\n"
echo "powl.parser"
echo "-----------"
python test/small/test_parser.py

echo "\n"
echo "powl.transactionconverter"
echo "-------------------------"
python test/small/test_transactionconverter.py

