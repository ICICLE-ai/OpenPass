import re
import cgi
from urllib.parse import urlparse, urlunparse, quote, unquote

def getUrlParameters(param_name, errorHTML, optional=False, error_message='No Parameter Specified'): 
    form = cgi.FieldStorage()
    param = str(form.getvalue(param_name))
    if (not optional) and (param == "None"):
        errorHTML = errorHTML.replace("CAUSE", error_message)
        print(errorHTML)
        quit() 
    return param

def getNumParameters():
    form = cgi.FieldStorage()
    count = sum(1 for key in form.keys() if key.startswith('p'))
    return count

def sanitizeUrl(url: str) -> str:
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Ensure the scheme is either http or https
        if parsed_url.scheme not in ["http", "https"]:
            raise ValueError("Invalid URL scheme. Only 'http' and 'https' are allowed.")

        # Normalize the netloc (domain)
        netloc = parsed_url.netloc.lower()

        # Encode path, parameters, and query to prevent injection attacks
        path = quote(unquote(parsed_url.path))
        query = quote(unquote(parsed_url.query), safe="=&")
        fragment = quote(unquote(parsed_url.fragment), safe="")

        # Rebuild the sanitized URL
        sanitized_url = urlunparse((parsed_url.scheme, netloc, path, parsed_url.params, query, fragment))

        # Validate the final URL format
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', sanitized_url):
            raise ValueError("Invalid URL format after sanitization.")

        return sanitized_url

    except Exception as e:
        raise ValueError(f"Invalid URL: {e}") from None