from src.splunk.client import (
    connect,
    run_search,
)

def show_apps(service):
    print("\nConnected Sucessfully")
    print("-"*50)

    for app in service.apps:
        print(app.name)

def fetch_logs(service):
    print("\nFentching Logs...")
    print("-"*50)

    query = "search index = _internal | head 10"

    results = run_search(
        service,
        query
    )

    count = 0

    for result in results:
        print(result)
        count +=1

    print (f"\n Retrived {count} logs")

def main():
    try:
        service = connect()

        show_apps(service)

        fetch_logs(service)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()     
