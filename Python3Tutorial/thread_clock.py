import threading
import time

state = False


def background_calculation():
    # set the time
    time.sleep(1)

    # Toggle and print state
    global state
    state = not state
    print(state)
    background_calculation()


def main():
    thread = threading.Thread(target=background_calculation)
    thread.start()


if __name__ == '__main__':
    main()
