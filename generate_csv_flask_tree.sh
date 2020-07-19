cat output.csv|grep call, |cut -d ',' -f5,4|tr ',' ' '|awk '{print $2,",",$1}'|tr -d ' '|sed 's/\.py,/,/g' > flask_tree.csv
