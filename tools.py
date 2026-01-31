from colorama import Fore, Style
from simulator import env 

def reroute_traffic(target_gateway: str):
    print(f"{Fore.YELLOW}  TOOL EXECUTION: Rerouting all traffic to {target_gateway}...{Style.RESET_ALL}")
    env.active_route = target_gateway
    return f"Successfully rerouted to {target_gateway}."

def escalate_to_human(reason: str):
    print(f"{Fore.RED} TOOL EXECUTION: Paging Operations Team. Reason: {reason}{Style.RESET_ALL}")
    return "Ops team notified."

def no_action():
    return "Monitoring continues."