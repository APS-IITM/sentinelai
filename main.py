from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.utlis.formatter import pretty_json


def print_section(title, response):
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)

    print(f"Success: {response.get('success')}")
    print(f"Total Records: {response.get('count')}")
    
    if response.get("error"):
        print(f"Error: {response['error']}")
        return

    data = response.get("data", [])

    if data:
        print("\nSample Record:\n")
        print(pretty_json(data[0]))


def main():

   
    auth_tool = AuthTools()
    security_tool = SecurityTools()
    system_tool = SystemTools()

   
    auth_logs = auth_tool.get_auth_logs(limit=20)
    print_section("AUTH LOGS", auth_logs)

   
    error_logs = security_tool.get_security_logs(limit=20)
    print_section("ERROR LOGS", error_logs)

   
    system_logs = system_tool.get_system_logs(limit=20)
    print_section("SYSTEM LOGS", system_logs)

   
    search_logs = system_tool.search_logs("login", limit=10)
    print_section("SEARCH LOGS (login)", search_logs)

    login_trend = system_tool.login_trend()
    print_section("LOGIN TREND (ANOMALY INPUT)", login_trend)

    error_trend = system_tool.error_trend()
    print_section("ERROR TREND (ANOMALY INPUT)", error_trend)


if __name__ == "__main__":
    main()