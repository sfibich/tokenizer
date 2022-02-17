#!/bin/bash

random-string() {
        cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w ${1:-32} | head -n 1
}

url="localhost:7071"
code=""
code2=""


for i in {1..50}
do
    #time_value=$(python2 -c 'import datetime; print datetime.datetime.now().strftime("%s.%f")')
    #random_value=$( echo $time_value | sha256sum | base64 | head -c 32 ; echo)
    random_value=$(curl -s 'https://random-words-api.vercel.app/word' | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['word'])")
    echo "starting value:${random_value}"
    output=$(curl -s -X GET "${url}/api/tokenize?customer=customer1&value=${random_value}${code}")
    echo $output
    token=$(echo $output | cut -d":" -f 2 | tr -d '"' | tr -d "}" | tr -d "\n" | tr -d " ")
    #echo "$token|"
    curl -X GET "${url}/api/detokenize?customer=customer1&token=${token}${code2}"
    echo ""
done