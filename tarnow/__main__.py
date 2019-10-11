from tarnow import tarnow_app, tarnow_switch
import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        tarnow_app.main()
    else:
        tarnow_switch.main(sys.argv[1:])


if __name__ == "__main__":
    main()
