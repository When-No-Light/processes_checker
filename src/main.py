from application.rename import ComputerMonitoringManager
from infrastructure.system.power_shell_adapter import PowerShellAdapter

if __name__ == "__main__":
    s = PowerShellAdapter()

    cmm = ComputerMonitoringManager()

    cmm.start_monitoring()
