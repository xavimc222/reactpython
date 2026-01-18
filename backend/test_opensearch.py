#!/usr/bin/env python3
"""
Standalone OpenSearch connectivity test script.
Run from CLI: python backend/test_opensearch.py

This script tests connectivity to OpenSearch using the default query
example from the frontend application.
"""

import logging
import json
from utils.readopense import readopense

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_opensearch_connection():
    """
    Test OpenSearch connectivity with the default query from frontend.
    
    This uses the same query structure shown in the frontend App.tsx
    to verify OpenSearch is reachable and responding correctly.
    """
    logger.info("Testing OpenSearch connectivity...")
    
    # Default query payload from frontend example
    payload = {
        "payload": {
            "size": 1,
            "query": {
                "bool": {
                    "must": [
                        # Uncomment to add specific filters:
                        # {"match": {"item": "500007300 D133"}},
                    ],
                    "must_not": [
                        # Uncomment to exclude specific values:
                        # {"match": {"rule": "None"}}
                    ],
                }
            },
            "_source": {
                "includes": [
                    # Uncomment to specify which fields to return:
                    # "children",
                    # "parents",
                ]
            },
            "sort": [
                # Uncomment to add sorting:
                # {"inventoryDate": {"order": "desc"}}
            ]
        },
        "index": "ai-research-shell-bom-3",
    }
    
    try:
        logger.info(f"Querying index: {payload['index']}")
        logger.info(f"Query size: {payload['payload']['size']}")
        
        # Execute the query
        response: list[dict] = readopense(payload)
        
        # Display results
        logger.info("=" * 60)
        logger.info("OpenSearch Connection: SUCCESS ✓")
        logger.info("=" * 60)
        logger.info(f"Documents returned: {len(response)}")
        logger.info(f"Index: {payload['index']}")
        
        if response:
            logger.info("\nFirst document:")
            print(json.dumps(response[0], indent=2))
        else:
            logger.info("\nNo documents found matching the query.")
        
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("OpenSearch Connection: FAILED ✗")
        logger.error("=" * 60)
        logger.error(f"Error: {str(e)}")
        logger.error("\nPlease check:")
        logger.error("1. AWS credentials are configured (aws configure)")
        logger.error("2. OpenSearch domain is accessible")
        logger.error("3. IAM permissions allow OpenSearch access")
        logger.error("4. Network connectivity to the domain")
        logger.error("=" * 60)
        return False


def main():
    """Main entry point for CLI execution."""
    print("\n" + "=" * 60)
    print("OpenSearch Connectivity Test")
    print("=" * 60 + "\n")
    
    success = test_opensearch_connection()
    
    exit_code = 0 if success else 1
    exit(exit_code)


if __name__ == "__main__":
    main()
