import subprocess
from pwnagotchi import plugins
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui import fonts
import logging


class CPUPower(plugins.Plugin):
    __author__ = "hashtagtodo"
    __version__ = "1.0.0"
    __license__ = "GPL3"
    __description__ = "Displays the CPU power in GHz on the Pwnagotchi UI."

    def __init__(self):
        self.cpu_power = "0.0"

    def on_loaded(self):
        logging.info("[cpu-power] plugin loaded")

    def get_cpu_power(self):
        try:
            result = subprocess.check_output(["lscpu"]).decode()
            for line in result.split("\n"):
                if "CPU max MHz" in line:
                    mhz_value = float(line.split()[-1])
                    self.cpu_power = f"{mhz_value / 1000:.1f}G"
                    # logging.info(f"[cpu-power] {self.cpu_power}") # Uncomment for CPU Power Logging (very annoyed)
                    break
        except Exception as e:
            logging.error(
                f"[cpu-power] error while reading CPU max frequency: {str(e)}"
            )
            self.cpu_power = "N/A"

    def on_ui_setup(self, ui):
        ui.add_element(
            "cpu-power",
            LabeledValue(
                color="BLACK",
                label="",
                value=f"{self.cpu_power}",
                position=(ui.width() // 2 + 5, 0),
                label_font=fonts.Bold,
                text_font=fonts.Medium,
            ),
        )

    def on_unload(self, ui):
        ui.remove_element("cpu-power")

    def on_ui_update(self, ui):
        self.get_cpu_power()
        ui.set("cpu-power", value=self.cpu_power)
