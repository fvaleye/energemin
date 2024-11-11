import asyncio
import logging
import os

from typing import AsyncGenerator

from gemini_llm import call_vertex_ai_gemini
from location import get_location
from machine_stats import get_battery_information
from machine_stats import get_cpu_information
from machine_stats import get_disk_information
from machine_stats import get_list_of_running_processes
from machine_stats import get_machine_information
from machine_stats import get_memory_information
from machine_stats import get_network_information
from machine_stats import get_stats_sensors

from langchain.prompts import load_prompt

logging.basicConfig(level=logging.INFO)


async def start_audit(prompt_file_path: str | None = None,
                      messages: list[str] | None = None,
                      location: dict[str, str] | None = None) -> AsyncGenerator[str, None]:

    try:
        if not location:
            location = get_location()

        if not prompt_file_path:
            prompt_file_path = os.path.join(os.path.dirname(__file__), "prompts", "prompt.yaml")

        metric_functions = {
            'sensors': get_stats_sensors,
            'cpu': get_cpu_information,
            'disk': get_disk_information,
            'network': get_network_information,
            'memory': get_memory_information,
            'battery': get_battery_information,
            'system': get_machine_information,
            'processes': get_list_of_running_processes
        }

        metrics = {}
        for name, func in metric_functions.items():
            try:
                metrics.update(func())
            except Exception as e:
                logging.warning(f"Failed to collect {name} metrics: {e!s}")

        prompt_template = load_prompt(path=prompt_file_path)
        prompt = prompt_template.format(location=location, metrics=metrics, messages=messages)

        async for response in call_vertex_ai_gemini(prompt):
            yield response

    except Exception as e:
        logging.error(f"An error occurred: {e!s}")
        raise e

def start_audit_sync():
    async def run():
        async for response in start_audit():
            logging.info(response)

    return asyncio.run(run())

if __name__ == "__main__":
    start_audit_sync()
