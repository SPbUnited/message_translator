import time
import zmq

if __name__ == "__main__":
    context = zmq.Context()

    time.sleep(2)
    s_telemetry = context.socket(zmq.PUB)
    s_telemetry.connect("ipc:///tmp/ether.telemetry.xsub")

    while True:
        datad = {
            "test_telemetry": "test telemetry value\nit is just a string, {time.time()%2}"
        }
        s_telemetry.send_json(datad)
        print("pupupu")
        time.sleep(0.005)
