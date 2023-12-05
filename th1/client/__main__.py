import sys
import datetime
import argparse
import getpass
import time

import th1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="th1.client", description="Somfy th1 api client"
    )
    parser.add_argument("-l", "--login", action="store_true")
    parser.add_argument("-t", "--thermostat", help="the thermostat ID")
    parser.add_argument("-s", "--smartphone", help="the smartphone ID")
    args = parser.parse_args()

    client = th1.Client()
    if args.login:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        client.login(username, password)

    if not args.thermostat:
        thermostsats = client.get_thermostats()
        print("Please select a thermostat:")
        for t in thermostsats.results:
            print(f"* {t.id}")
        return -1

    if not args.smartphone:
        smartphones = client.get_smartphones(args.thermostat)
        print("Please select a smartphones:")
        for s in smartphones:
            print(f"* {s.vendor_id} ({s.name})")
        return -1

    while True:
        info = client.get_thermostat_info(args.thermostat, args.smartphone)

        # Deal with derogation
        consigne = info.temperature_consigne
        mode = info.mode
        if info.latest_derogation is not None:
            is_in_derogation = (
                info.latest_derogation.finish_at > datetime.datetime.now(tz=datetime.timezone.utc)
                and info.latest_derogation.started_at <= datetime.datetime.now(tz=datetime.timezone.utc)
            )
            if is_in_derogation:
                consigne = info.latest_derogation.temperature
                mode = info.latest_derogation.heating_mode

        print("----")
        print(f"consigne: {consigne}")
        print(f"mode: {mode}")
        print(f"temperature: {info.temperature}")
        print(f"humidity: {info.humidity}")
        print(f"battery: {info.battery}")
        
        time.sleep(5)

    return 0


if __name__ == "__main__":
    sys.exit(main())
