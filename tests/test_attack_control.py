from src.simulator.attack_control import AttackControlSystem


def main():

    system = AttackControlSystem()

    print("\nLaunching Brute Force Attack")
    print(system.launch("brute_force"))

    print("\nLaunching Port Scan Attack")
    print(system.launch("port_scan"))

    print("\nCurrent Status")
    print(system.status())


if __name__ == "__main__":
    main()