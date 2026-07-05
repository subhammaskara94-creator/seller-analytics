import time


MAX_RETRIES = 5

INITIAL_WAIT = 2


def retry_api_call(api_function):
    """
    Retry Amazon SP-API calls when throttled.
    """

    wait = INITIAL_WAIT

    for attempt in range(MAX_RETRIES):

        try:
            return api_function()

        except Exception as e:

            message = str(e)

            if "QuotaExceeded" not in message:
                raise

            print(
                f"Quota exceeded. Retry {attempt + 1}/{MAX_RETRIES} "
                f"in {wait} seconds..."
            )

            time.sleep(wait)

            wait *= 2

    raise Exception(
        "Maximum retries exceeded."
    )