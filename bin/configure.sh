#!/bin/bash
# Creates and edits security.conf file

# Check 1 argument was given
if [ ! $# -lt 2 ]; then
   echo "This script does not take more than 1 argument"
else
  correctVal=false
  case "$1" in
  # Get brightness from user
  -b) ;&
  --brightness)
      if [ -f "security.conf" ]; then
        while [ $correctVal == false ]; do
          read -p "Enter a value for brightness (1-254): " brightness
          regex='^[0-9]+$'  # Checks for numbers only
          if [[ $brightness =~ $regex ]]; then
            if [ 0 -lt $brightness -a $brightness -lt 255 ]; then
              correctVal=true
            fi
          fi
        done
        sed -i "1s/[0-9][0-9]*/$brightness/g" security.conf
      else
        echo -e "\nYou need to generate the security.conf file first"
      fi
      ;;
  # Get threshold from user
  -t) ;&
  --threshold)
      if [ -f "security.conf" ]; then
        while [ $correctVal == false ]; do
          read -p "Enter a value for threshold (1-254): " threshold
          regex='^[0-9]+$'  # Checks for numbers only
          if [[ $threshold =~ $regex ]]; then
            if [ 0 -lt $threshold -a $threshold -lt 255 ]; then
              correctVal=true
            fi
          fi
        done
        sed -i "2s/[0-9][0-9]*/$threshold/g" security.conf
      else
        echo -e "\nYou need to generate the security.conf file first"
      fi
      ;;
  # Get help
  -h) ;&
  --help)
    echo -e "\n  (No arguments) - Generates security.conf file"
    echo -e "\n  -b, --brightness\n              Edits brightness value, "\
            "a higher value means a brighter image,\n"\
            "             178 is the default"
    echo -e "  -t, --threshold\n              Edits threshold value, "\
            "which makes it easier/harder to detect,\n"\
            "             60 is the default\n"\
            "             movement based on how low/high the value is set"
    echo -e "  -e, --email\n              Edits email information"
    echo -e "  -p, --phone\n              Edits phone information"
    echo -e "  -r, --reset\n              Deletes the current security.conf "\
            "file and starts the\n             "\
            "configuration process from scratch"
    echo  -e "  -h, --help\n              Brings up this help page"
      ;;
  # Updates email information
  -e)  ;&
  --email)
      if [ -f "security.conf" ]; then
        while [ "$receive_email" != "Y" ] && 
              [ "$receive_email" != "y" ] && 
              [ "$receive_email" != "N" ] && 
              [ "$receive_email" != "n" ]; do 
          read -p "Would you like to receive email alerts? (Y/N): " receive_email
        done
        if [ "$receive_email" = "Y" ] || [ "$receive_email" = "y" ]; then
          read -p "Enter your email address (Gmail only): " email_addr
          read -p "Enter your password for your email: " password
          if [ "$email_addr" != "" ] && [ "$password" != "" ]; then
            sed -i "3s/\s./ $receive_email/g" security.conf
            sed -i "4s/\s.*/ $email_addr/g" security.conf
            sed -i "5s/\s.*/ $password/g" security.conf
          fi
        fi
      fi
      ;;
  # Updates phone information
  -p) ;&
  --phone)
      if [ -f "security.conf" ]; then
        while [ "$receive_text" != "Y" ] && 
              [ "$receive_text" != "y" ] && 
              [ "$receive_text" != "N" ] && 
              [ "$receive_text" != "n" ]; do 
         read -p "Would you like to receive text alerts? (Y/N): " receive_text
        done 
        if [ "$receive_text" == "Y" ] || [ "$receive_text" == "y" ]; then
          read -p "Enter your phone number (no dashes): " phone_num
          read -p "Enter your carrier: " carrier
          if [ "$phone_num" != "" ] && [ "$carrier" != "" ]; then
            sed -i "6s/\s./ $receive_text/g" security.conf
            sed -i "7s/\s.*/ $phone_num/g" security.conf
            sed -i "8s/\s.*/ $carrier/g" security.conf
          fi
        fi
      fi
      ;;
  # Deletes current security.conf file
  -r) ;&
  --reset)
      if [ -f "security.conf" ]; then
        rm "security.conf"
      fi
      ;&
  # Create a new security.conf file if it doesn't already exist
  *) 
     if [ -f "security.conf" ]; then
       echo "'security.conf' already exists" 
     else 
       while [ "$receive_email" != "Y" ] && 
             [ "$receive_email" != "y" ] && 
             [ "$receive_email" != "N" ] && 
             [ "$receive_email" != "n" ]; do 
         read -p "Would you like to receive email alerts? (Y/N): " receive_email
       done
       if [ "$receive_email" = "Y" ] || [ "$receive_email" = "y" ]; then
         read -p "Enter your email address (Gmail only): " email_addr
         read -p "Enter your password for your email: " password
       fi
       while [ "$receive_text" != "Y" ] && 
             [ "$receive_text" != "y" ] && 
             [ "$receive_text" != "N" ] && 
             [ "$receive_text" != "n" ]; do 
         read -p "Would you like to receive text alerts? (Y/N): " receive_text
       done 
       if [ "$receive_text" == "Y" ] || [ "$receive_text" == "y" ]; then
         read -p "Enter your phone number: " phone_num
         read -p "Enter your carrier: " carrier
       fi

       echo "brightness: 128" >> security.conf
       echo "threshold: 60" >> security.conf
       if [ "$email_addr" == "" ] || [ "$password" == "" ]; then
         echo "receive_email: N" >> security.conf
         echo "email_address: " >> security.conf
         echo "password: " >> security.conf
       else
         echo "receive_email: $receive_email" >> security.conf
         echo "email_address: $email_addr" >> security.conf
         echo "password: $password" >> security.conf 
       fi  
       if [ "$phone_num" == "" ] || [ "$carrier" == "" ]; then
         echo "receive_text: N" >> security.conf
         echo "phone_number: " >> security.conf 
         echo "carrier: " >> security.conf
       else
         echo "receive_text: $receive_text" >> security.conf
         echo "phone_number: $phone_num" >> security.conf 
         echo "carrier: $carrier" >> security.conf
       fi 

     fi
     ;;
  esac
fi
