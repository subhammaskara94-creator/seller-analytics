from amazon.client import AmazonClient


def main():
    print("Connecting to Amazon...\n")

    client = AmazonClient()

    response = client.get_marketplaces()

    print(response.payload)


if __name__ == "__main__":
    main()