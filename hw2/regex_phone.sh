# this program finds phone numbers in text, creating a file with phone numbers being bracketed (output_phone.txt), and another file listing all the phone numbers (phone.txt)
# run this program by running ./regex_phone.sh INPUT_FILE
# if file permissions deny execution, run chmod 700 regex_phone.sh

sed -E 's/(\([0-9]{3}\)|[0-9]{3})[ -]?[0-9]{3}[ -]?[0-9]{4}/[&]/g' $1 > output_phone.txt

grep -Eo '(\([0-9]{3}\)|[0-9]{3})[ -]?[0-9]{3}[ -]?[0-9]{4}' $1 > phone.txt
