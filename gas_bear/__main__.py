
import logging
import bme680
import time

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)

    sensor = bme680.BME680()

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
            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)

            if sensor.data.heat_stable:
                logger.info("Gas sensor data collected")
                print('{0},{1} Ohms'.format(
                    output,
                    sensor.data.gas_resistance))

            else:
                logger.warning("Gas sensor data not heat stable")
                print(output)
        else:
            logger.warning("No data from sensors")

        logger.info("Waiting for a bit...")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("gas sensing has stopped")
