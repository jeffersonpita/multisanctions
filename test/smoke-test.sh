#!/bin/sh

alias curl="curl --fail --silent"
alias jq="jq --exit-status"

search() {
  name=$1
  assertion=$2
  test_case="search: ${name}, expect: ${assertion}"

  curl ${API}/search -G --data-urlencode "name=${name}" | \
    (jq "$assertion" > /dev/null) && echo "PASS | ${test_case}" || (echo "FAIL | ${test_case}" && exit 1)
}

echo ${API}
until $(curl --output /dev/null ${API}/status); do
  echo 'waiting for api...'
  sleep 5
done

search 'Robert Gabriel Mugabe' '.[0].sanctioned == true and .[0].relevance == 1'
search 'Abou Ali' '.[0].sanctioned == true and .[0].relevance == 1'
search 'οργάνωση Al-Qaida στην Αραβική Χερσόνησο' '.[0].sanctioned == true and .[0].relevance == 1'
search 'Université Malek Ashtar' '.[0].sanctioned == true and .[0].relevance == 1'
search 'KCST' '.[0].sanctioned == true and .[0].relevance == 1'
search 'Iran Modern Devices' '.[0].sanctioned == true and .[0].relevance >= 0.8'
search 'Pop Credit Bank' '.[0].sanctioned == true and .[0].relevance >= 0.8'
search 'Bank of Syria' '.[0].sanctioned == true and .[0].relevance >= 0.8'
exit 0
