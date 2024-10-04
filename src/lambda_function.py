#!/usr/bin/env python3

"""
Lambda handler to incoming whois requests for the Just Report It plugin
"""

from http import HTTPStatus
import validators
from tldextract import extract
from lambdawarmer import warmer
from whois import whois
from response import HttpResponse

@warmer(send_metric=True)
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
            whois_result = whois(domain)
            if whois_result.emails is None:
                return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST,
                                            error="No email addresses found in WHOIS lookup")

            emails = whois_result.emails if isinstance(whois_result.emails, list) else [whois_result.emails]

            for email in emails:
                if "abuse" in email.lower():
                    return HttpResponse.success(status=HTTPStatus.OK, email=email)

            # If no abuse email found, return the first email
            return HttpResponse.success(status=HTTPStatus.OK, email=emails[0])
        except Exception as e:
            return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST, error=f"WHOIS lookup failed: {str(e)}")
    return HttpResponse.failure(status=HTTPStatus.BAD_REQUEST,
                                error=f"Domain ({domain}) is invalid or not supported.")


if __name__ == "__main__":
    print(email("test.com"))
    print(validate_domain("test.com"))
