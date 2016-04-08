# this program finds dollar amounts in text, creating a file with dollar amounts being bracketed (output_dollar.txt), and another file listing all the dollar amounts (dollar.txt)
# run this program by running ./regex_dollar.sh INPUT_FILE
# if file permissions deny execution, run chmod 700 regex_dollar.sh

sed -E 's/(\$[0-9,]+(\.[0-9][0-9])?)|(\$?[A-Za-z0-9_.,]+ *([dD]ollars?\b|\b[cC]ents?))/[&]/g' $1 > output_dollar.txt

grep -Eo '(\b\$[0-9,]+(\.[0-9][0-9])?\b)|(\b\$?[A-Za-z0-9_.,]+ *(\b[dD]ollars?\b|\b[cC]ents?\b)\b)' $1 > dollar.txt
