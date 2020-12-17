# Just Report It Server

## Introduction ##

Just Report It (<https://justreport.it>) is an email plugin which makes it easy to report spam emails back to the domain registrar. This method ensures that spam domains are effetively being blocked at the registrar level and not just locally.

## Limitations ##

Unfortunately, this whois lookup isn't perfect, and is lacking. This is because we are using an external library (python-whois) to query the whois database. This library currently supports the following TLD's (and a few more):

* com
* ai
* app
* dev
* games
* page
* money
* online
* cl
* ar
* by
* cr
* ca
* do
* de
* hk
* hn
* jobs
* lat
* li
* mx
* pe
* ist
* kz
* chat
* website