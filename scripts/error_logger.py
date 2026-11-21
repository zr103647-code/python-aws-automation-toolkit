
import logging
import os
from datetime import datetime

LOG_FOLDER = "logs"

os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "automation_errors.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def run_test():
    logging.info("Automation started.")

    try:
        print("Testing error logging system...")

        # Simulate an error for testing
        result = 10 / 0

        print(result)

    except Exception:
        logging.exception("An error occurred during automation.")

    logging.info("Automation finished.")


if __name__ == "__main__":
    print("Starting Error Logging Automation...")

    run_test()

    print(f"\nLog file saved: {LOG_FILE}")

    print("\nError Logging Automation Completed!")
