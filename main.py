import time
from colorama import Fore, Style, init
import os

# CONFIG
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "Not an API Key"

# IMPORTS
from agent import app   
from simulator import env 

init(autoreset=True)

def run_simulation():
    print(f"{Fore.WHITE}--- STARTING MODULAR AGENT ---{Style.RESET_ALL}")
    state = {"history": []}
    
    for i in range(6):
        print(f"\n{Fore.WHITE}--- TICK {i+1} ---{Style.RESET_ALL}")
        
        if i == 2:
            print(f"{Fore.RED}>>> INJECTING FAULT <<<")
            env.set_status("DEGRADED")
            
        result = app.invoke(state)
        state = result
        time.sleep(2)

if __name__ == "__main__":
    run_simulation()