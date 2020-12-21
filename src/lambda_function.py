#!/usr/bin/env python3

"""
Lambda handler to incoming whois requests for the Just Report It plugin
"""

from http import HTTPStatus
import validators
from tldextract import extract
from whois import whois
from response import HttpResponse

def lambda_handler(event, context):
    """
    Returns completed request with response code (used by the lambda handler)
    """
    if event["pathParameters"]["domain"] is not None:
        return email(event["pathParameters"]["domain"])
    return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST,
                                error="No domain included in the request")

def validate_domain(domain):
    """
    Validates incoming domain and filters for ip-based 'domains'
    """
    return validators.domain(extract(domain).domain + "." + extract(domain).suffix)

def email(domain):
    """
    Finds the relevant abuse email address for the domain
    """
    if validate_domain(domain):
        try:
            emails = whois(domain).emails
            if isinstance(emails, list):
                for email in emails:
                    if "abuse" in email:
                        return HttpResponse.success(status=HTTPStatus.OK, email=email)
            else:
                return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST, error="WHOIS lookup has failed")
        except:
            return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST, error="TLD is not yet supported")
    return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST,
                                error="Domain (%s) is invalid or not supported." % domain)
