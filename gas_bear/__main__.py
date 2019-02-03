import logging
import bme680
import time
import csv

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)

    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    logger.info("Initial sensor config complete")

    while True:
        logger.info("Polling sensors")
        if sensor.get_sensor_data():
            logger.info("Sensor data collected")
            output = [
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity
                ]

            if sensor.data.heat_stable:
                logger.info("Gas sensor data collected")
                output.append(sensor.data.gas_resistance)

            else:
                logger.warning("Gas sensor data not heat stable")
                output.append(0)
        else:
            logger.warning("No data from sensors")
            output = [0, 0, 0, 0]

        output.insert(0, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

        with open('data.csv', mode='a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(output)
            f.close()

            logger.info("Waiting for a bit...")
            time.sleep(300)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("gas sensing has stopped")
