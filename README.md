# Just Report It Server

## Introduction ##

Just Report It (<https://justreport.it>) is an email plugin which makes it easy to report spam emails back to the domain registrar. This method ensures that spam domains are effetively being blocked at the registrar level and not just locally.

## Deployment ##

To deploy this script to AWS Lambda, you must create a self-contained archive containing all the necessary libraries. To do so, run the following commands in order:

> pip install -r requirements.txt -t ./package

> cd package

> zip -r9 ${OLDPWD}/src/function.zip .

> cd ${OLDPWD}/src

> zip -g function.zip lambda_function.py

> zip -g function.zip response.py