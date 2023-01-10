
#!/bin/bash

if [ $# -eq 0 ]
then 
    echo
    echo "Please use the following format: ./requests.sh fieldname=fieldvalue fieldname=fieldvalue fieldname=fieldvalue... if phone, use +71234445577"
    echo
    exit 1
fi

d=""
for i in "$@"
do
    d+=$i
    d+="&"
done

url="http://127.0.0.1:8000/get_form?"$d

echo "Fetching the name of form from" $url
ans="$(curl -s POST $url)"

echo $ans