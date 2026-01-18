import logging
from boto3 import Session, set_stream_logger
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

set_stream_logger(name="botocore.credentials", level=logging.ERROR)

def countopense(
    event,
    domain_name: str = "search-common-arnlsjpb2fr2jisljvaoxzlizq.eu-west-2.es.amazonaws.com",
    verbose: bool = False,
) -> int:
    """
    Returns the count of documents in an OpenSearch index.

    Parameters:
    event (dict): The event containing payload and index information. Expected keys: 'payload' and 'index'.
    context (dict): AWS Lambda context parameter, not used in this function.

    Returns:
    int: Total number of documents matching the query.

    Raises:
    Exception: If the 'index' or 'payload' are missing in the event.
    """

    # inits
    payload = event.get("payload")
    index_name = event.get("index")
    region = event.get("region", "eu-west-2")

    # verify inputs
    if not index_name or not payload:
        raise Exception("Missing index or payload")

    # get opensearch client
    credentials = Session().get_credentials()
    auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        "es",
        session_token=credentials.token,
    )
    client_opensearch = OpenSearch(
        hosts=[{"host": domain_name, "port": 443}],
        timeout=20,
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        http_compress=True,
        connection_class=RequestsHttpConnection,
    )
    logging.getLogger("opensearch").setLevel(logging.WARNING)

    # query
    response = client_opensearch.count(index=index_name, body=payload)

    # return
    if verbose:
        print(f"Count for index {index_name}: {response['count']}")
    return response["count"]
