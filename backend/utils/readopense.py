import logging
import json
from boto3 import Session, set_stream_logger
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

set_stream_logger(name="botocore.credentials", level=logging.ERROR)


def readopense(
    event: dict,
    domain_name: str = "search-common-arnlsjpb2fr2jisljvaoxzlizq.eu-west-2.es.amazonaws.com",
    response_key: str = "hits",
    verbose: bool = False,
) -> list[dict]:

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
    response = client_opensearch.search(index=index_name, body=payload)
    print(
        response.keys()
    )  # returns: dict_keys(['took', 'timed_out', '_shards', 'hits', 'aggregations'])

    # curate response
    if verbose:
        print(json.dumps(response, indent=2))
    if response_key == "hits":
        response = response.get("hits", {}).get("hits", [])
    elif response_key == "aggregations":
        logging.info(f"[readopense] aggregations hits: {response['hits']['total']}")
        response = [response.get("aggregations", {})]
    else:
        logging.error(f"[readopense] Invalid response key: {response_key}")
        raise Exception(f"[readopense] Invalid response key: {response_key}")

    # return
    return response
