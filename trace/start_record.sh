if [ $4 == "True" ]; then
  cd trojan
  ./trojan &
  cd ../
  node record_trace.js $1 $2 $3 $4 $5
else
  node record_trace.js $1 $2 $3 $4 $5
fi