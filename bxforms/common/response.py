"""Handle response-based functions."""
from bottle import HTTPResponse
from common.const import MALTEGO_PHRASE
from common.maltego import UIM_FATAL
from common.maltego import UIM_INFORM


def custom_exception(code, string):
    """Generate a custom Maltego exception for worst cases."""
    message = ''
    message += "<MaltegoMessage>"
    message += "<MaltegoTransformExceptionMessage>"
    message += "<Exceptions>"
    message += "<Exception code=\"%d\">%s</Exception>" % (code, string)
    message += "</Exceptions>"
    message += "</MaltegoTransformExceptionMessage>"
    message += "</MaltegoMessage>"
    return message


def format_error(response):
    """Format the error to be sent back to the user.

    :param response: API response back from Blockade
    """
    error = response.get('error', dict())
    message = ("Blockade: [HTTP %d] %s, %s" % (
        error.get('http_code', 500),
        error.get('message', 'Failed to grab message'),
        error.get('developer_message', 'Failed to grab message')
    ))

    return message


def maltego_response(trx, status_code=200, override=None):
    """Return a properly formatted Maltego response."""
    try:
        response = trx.returnOutput()
    except Exception as err:
        msg = "Encountered errors in Maltegos Python library: %s" % (err)
        override = custom_exception(681, msg)

    if override:
        response = override
    return HTTPResponse(status=status_code, body=response)


def error_response(trx, response):
    """Single output flow for returning an error."""
    trx.addUIMessage(format_error(response), UIM_FATAL)
    if response['message'].get('http_code', 500) == 401:
        # HTTP code for Maltego mis-matched authentication
        status_code = 200
        message = custom_exception(600, "API/Username invalid")
        # Needed in order to prompt the user -- Maltego fails any other way
        return maltego_response(trx, status_code, message)
    else:
        status_code = 500

    return maltego_response(trx, status_code=status_code)
