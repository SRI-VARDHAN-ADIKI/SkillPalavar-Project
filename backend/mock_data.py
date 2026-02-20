MOCK_IT_DOCUMENTS = [
    """
    Document: ThinkPad T14s Gen 3 - Screen Flickering Fix
    Model: Lenovo ThinkPad T14s Gen 3
    Issue: Screen flickering, display artifacts, intermittent black screen
    Category: Display / Hardware

    Symptoms:
    - Screen flickers rapidly especially during scrolling or video playback
    - Display shows horizontal or vertical lines
    - Screen goes black intermittently and comes back
    - Issue worsens when laptop is moved or flexed

    Root Causes:
    1. Loose or damaged eDP (Embedded DisplayPort) cable connecting the motherboard to the display panel
    2. Outdated or corrupt Intel/AMD display drivers
    3. Faulty display panel backlight
    4. Incompatible refresh rate settings
    5. Hardware acceleration conflicts in the GPU settings

    Step-by-Step Troubleshooting:
    Step 1 - Software Check:
      - Press Win + R, type "devmgmt.msc", and open Device Manager.
      - Expand "Display adapters", right-click the GPU (Intel Iris Xe or AMD Radeon), and select "Update driver".
      - Choose "Search automatically for drivers". Restart the laptop after updating.

    Step 2 - Check Refresh Rate:
      - Right-click the desktop, go to Display Settings > Advanced Display Settings.
      - Ensure the refresh rate is set to 60Hz or 120Hz (matching your panel spec).
      - Change it and apply to see if flickering stops.

    Step 3 - Disable Hardware Acceleration:
      - In Chrome: Settings > System > Disable "Use hardware acceleration when available".
      - In Windows: Settings > System > Display > Graphics Settings > Disable hardware-accelerated GPU scheduling.

    Step 4 - Physical Cable Inspection (Requires Technician):
      - Power off the laptop completely and remove the battery.
      - Use a T5 Torx screwdriver to remove the display bezel clips.
      - Locate the eDP cable running from the bottom hinge to the display panel.
      - Reseat the cable connectors on both the motherboard end and the panel end.
      - If the cable shows visible damage (cuts, kinks), replace it with Lenovo FRU Part #5C10S30404.

    Step 5 - BIOS Update:
      - Visit Lenovo Support (support.lenovo.com), search for "T14s Gen 3".
      - Download the latest BIOS update and run the installer with administrator rights.

    Escalation: If flickering persists after all steps, replace the display panel using Lenovo FRU #5D11C12165. Contact Tier 2 for panel replacement authorization.
    Warranty Note: Screen defects on T14s Gen 3 are covered under the standard 3-year Lenovo Premier Support warranty if reported within warranty period.
    """,

    """
    Document: Dell XPS 15 9530 - Severe Battery Drain Diagnostics
    Model: Dell XPS 15 9530
    Issue: Rapid battery drain, battery not charging, battery health degraded
    Category: Power Management / Battery

    Symptoms:
    - Battery drains from 100% to 0% in under 2 hours under light use
    - Battery percentage drops rapidly even when plugged in
    - Windows reports "Consider replacing your battery"
    - Laptop shuts down unexpectedly at 20-30% charge
    - Battery Health check shows capacity below 60% of design capacity

    Root Causes:
    1. Degraded lithium-ion battery cells (common after 300+ charge cycles)
    2. BIOS power management bug in firmware versions prior to 1.12.0
    3. Background processes with high CPU/GPU draw (cryptomining malware, runaway processes)
    4. Dell Power Manager not configured for battery preservation
    5. Faulty 130W USB-C charger or charging port

    Step-by-Step Troubleshooting:
    Step 1 - Check Battery Health Report:
      - Open Command Prompt as Administrator.
      - Run: powercfg /batteryreport /output "C:\battery_report.html"
      - Open the report in a browser and check "Design Capacity" vs "Full Charge Capacity".
      - If Full Charge Capacity is less than 50% of Design Capacity, the battery needs replacement.

    Step 2 - Identify Power-Hungry Processes:
      - Press Ctrl + Shift + Esc to open Task Manager.
      - Click "Power usage" column to sort by power consumption.
      - Terminate any non-essential processes consuming High or Very High power.
      - Run a full antivirus scan using Windows Defender to rule out malware.

    Step 3 - Update BIOS and Drivers:
      - Open Dell SupportAssist application (pre-installed on Dell systems).
      - Run a full scan and apply all recommended BIOS and driver updates.
      - Alternatively, visit dell.com/support, enter Service Tag, and download BIOS 1.12.0 or later.
      - CRITICAL: Ensure laptop is plugged in during BIOS update.

    Step 4 - Configure Dell Power Manager:
      - Open Dell Power Manager (install from Microsoft Store if missing).
      - Go to Battery > Battery Settings.
      - Set "Battery Charge Type" to "Primarily AC" or "Custom" with upper limit of 80%.
      - Enable "Advanced Charge Mode" to reduce long-term degradation.

    Step 5 - Test the Charger:
      - Try a known-good Dell 130W USB-C charger.
      - Check the charging port for bent pins or debris using a flashlight.
      - Run Dell's built-in battery diagnostics: Power on, press F12, select Diagnostics > Battery Test.

    Battery Replacement Procedure (Technician):
      - Model uses a 6-cell 86Whr battery, Dell Part #MV0R6.
      - Remove 8x Torx T5 screws from base panel.
      - Disconnect battery connector before any other component.
      - Replace battery and re-run calibration: fully discharge then charge to 100%.

    Escalation: If battery health is below 40% within warranty period, initiate express replacement via Dell Premier Support. Ticket SLA: 4-hour response, next-business-day part delivery.
    """,

    """
    Document: MacBook Pro 14-inch M2 Pro - Boot Loop Recovery
    Model: Apple MacBook Pro 14-inch (2023), M2 Pro / M2 Max Chip
    Issue: Continuous boot loop, stuck on Apple logo, won't boot to macOS
    Category: OS Recovery / Boot Failure

    Symptoms:
    - MacBook shows Apple logo with loading bar, then restarts repeatedly
    - System stalls at specific percentage of loading bar (common at 100%)
    - Screen goes black after Apple logo and cycles again
    - macOS appeared to update or install before the issue started

    Root Causes:
    1. Corrupted macOS system files from interrupted update
    2. Incompatible third-party kernel extension (kext) installed prior to reboot
    3. Startup disk errors in APFS volume
    4. T2 / Apple Silicon Secure Boot policy conflict
    5. Low disk space causing incomplete macOS installation

    Step-by-Step Troubleshooting:
    Step 1 - Force Restart and Safe Mode Boot:
      - Hold the Power button for 10 seconds to force shutdown.
      - Press and hold the Power button until "Loading startup options" appears.
      - Select your startup disk, then hold the Shift key and click "Continue in Safe Mode".
      - If Safe Mode boots successfully, a third-party extension is likely the cause.
      - In Safe Mode, go to System Settings > Privacy & Security and remove recently added extensions.

    Step 2 - Run First Aid on Startup Disk (macOS Recovery):
      - Shut down completely (hold Power button for 10 seconds).
      - Press and hold Power button until Options icon appears, click it and select Continue.
      - You are now in macOS Recovery (recoveryOS).
      - Open Disk Utility from the utilities menu.
      - Select "Macintosh HD" in the sidebar and click "First Aid", then "Run".
      - Wait for completion and check for errors. If errors are repaired, restart normally.

    Step 3 - Reinstall macOS (Non-Destructive):
      - If First Aid finds unrepairable errors, proceed with reinstall.
      - In macOS Recovery, select "Reinstall macOS Ventura/Sonoma" from the main menu.
      - Connect to a Wi-Fi network when prompted.
      - Select the startup disk (Macintosh HD) and continue.
      - This reinstalls the OS without deleting personal data. Takes 30-60 minutes.

    Step 4 - Erase and Reinstall (Data Loss - Last Resort):
      - In macOS Recovery, open Disk Utility.
      - Select "Macintosh HD - Data" and click the minus (-) button to delete the Data volume.
      - Then select "Macintosh HD" and click "Erase". Format: APFS, Scheme: GUID Partition Map.
      - Exit Disk Utility, select "Reinstall macOS" from the main menu.
      - Follow prompts. System will download and install a fresh copy of macOS.

    Step 5 - Apple Configurator 2 DFU Restore (Technician Only):
      - If all above steps fail, use Apple Configurator 2 on a secondary Mac.
      - Connect the affected MacBook via USB-C cable to the secondary Mac.
      - Put the affected MacBook into DFU mode: while connected, hold Right Shift + Left Option + Left Control for 3 seconds, then add the Power button for 10 more seconds.
      - On the secondary Mac, open Apple Configurator 2, select the device, and choose Actions > Revive Device.

    Escalation: If DFU restore fails, the logic board may have SSD or Memory failure. Book Genius Bar appointment or contact Apple Enterprise Support with device serial number.
    Warranty Note: MacBook Pro M2 covered under AppleCare+ for Enterprise (3 years). Hardware failures qualify for same-unit replacement within SLA.
    """,

    """
    Document: HP EliteBook 840 G9 - Wi-Fi Disconnection and Network Issues
    Model: HP EliteBook 840 G9
    Issue: Frequent Wi-Fi drops, cannot connect to 5GHz network, slow wireless speeds
    Category: Networking / Wireless

    Symptoms:
    - Wi-Fi disconnects every few minutes and reconnects automatically
    - 5GHz network not visible in available networks list
    - Wi-Fi speeds significantly lower than expected (below 50 Mbps on AC network)
    - Yellow exclamation mark on network adapter in Device Manager
    - Event Viewer shows "Intel Wi-Fi 6E AX211 driver stopped responding" errors

    Root Causes:
    1. Outdated Intel Wi-Fi 6E AX211 driver (version prior to 22.230.0)
    2. Power management settings causing the adapter to sleep aggressively
    3. Windows updates disabling or overwriting the OEM Wi-Fi driver
    4. Physical antenna cable loose inside lid
    5. Router channel congestion on 2.4GHz band

    Step-by-Step Troubleshooting:
    Step 1 - Update Wi-Fi Driver:
      - Go to HP Support (support.hp.com) and enter your product number (found under the laptop).
      - Download the Intel Wi-Fi 6E AX211 driver package (version 22.230.0 or later) for Windows 11.
      - Run the installer and restart the laptop.
      - Alternatively, use HP Support Assistant app to auto-detect and install the update.

    Step 2 - Disable Wi-Fi Power Management:
      - Open Device Manager, expand "Network Adapters".
      - Right-click "Intel(R) Wi-Fi 6E AX211 160MHz" > Properties > Power Management tab.
      - Uncheck "Allow the computer to turn off this device to save power". Click OK.
      - Also go to Control Panel > Power Options > Change plan settings > Change advanced power settings.
      - Find "Wireless Adapter Settings" > "Power Saving Mode" > Set to "Maximum Performance".

    Step 3 - Reset Network Stack:
      - Open Command Prompt as Administrator and run the following commands in order:
        netsh winsock reset
        netsh int ip reset
        ipconfig /release
        ipconfig /flushdns
        ipconfig /renew
      - Restart the laptop after running all commands.

    Step 4 - Configure Router Band (Infrastructure):
      - Log into your router admin page (usually 192.168.1.1 or 192.168.0.1).
      - Ensure 5GHz band is enabled and broadcasting.
      - Set 5GHz channel to a non-overlapping channel (36, 40, 44, or 48 for North America).
      - Enable WPA3 security if available; if device won't connect, temporarily switch to WPA2.

    Step 5 - Antenna Cable Check (Technician):
      - Open the laptop base cover (6x Torx T5 screws).
      - Locate the M.2 Wi-Fi card (Intel AX211) near the center-top of the motherboard.
      - Check that both antenna cables (black = main, white = auxiliary) are firmly seated on the card's connectors.
      - If cables are loose, press them firmly until they click into place.

    Escalation: If Wi-Fi adapter shows hardware failure in diagnostics, replace the Intel AX211 M.2 card (HP Spare Part #M74830-001). Contact Tier 2 for hardware procurement.
    """,

    """
    Document: Microsoft Surface Pro 9 - Touchscreen Unresponsive or Erratic
    Model: Microsoft Surface Pro 9 (Intel i5/i7 or SQ3)
    Issue: Touchscreen not responding, ghost touches, inaccurate touch registration
    Category: Display / Touch Input

    Symptoms:
    - Touch inputs not registered or registering in wrong locations
    - Screen shows random taps without user touching it (ghost touches)
    - Touch works in some areas but not others
    - Touch completely stops working after wake from sleep
    - Surface Pen works but finger touch does not

    Root Causes:
    1. Corrupted HID (Human Interface Device) touch driver
    2. Electrostatic discharge causing temporary controller fault
    3. Screen protector interference with capacitive sensor
    4. Windows firmware update bug (common in 22H2 build 22621.1265)
    5. Physical damage to digitizer layer under glass

    Step-by-Step Troubleshooting:
    Step 1 - Restart and Drain Static:
      - Shut down the Surface completely (not sleep).
      - With the Surface powered off, hold the Volume Up and Power button together for 15 seconds.
      - Release both buttons; the screen will flash the Surface logo a few times. This runs a firmware self-check.
      - Power on normally and test the touchscreen.

    Step 2 - Remove Screen Protector:
      - If a third-party screen protector is installed, carefully remove it.
      - Clean the screen with a microfiber cloth.
      - Test touch responsiveness directly on the glass. Many non-Surface-certified protectors cause interference.

    Step 3 - Reinstall Touch HID Driver:
      - Open Device Manager (Win + X > Device Manager).
      - Expand "Human Interface Devices".
      - Right-click "HID-compliant touch screen" and select "Uninstall device". Check "Delete driver software" and confirm.
      - Restart the Surface. Windows will automatically reinstall the driver on next boot.
      - Test the touchscreen after restart.

    Step 4 - Run Windows Update and Surface Firmware Update:
      - Go to Settings > Windows Update > Check for Updates. Install all pending updates.
      - Download and install the Surface Pro 9 firmware update from microsoft.com/en-us/surface/support.
      - Restart after all updates are applied.

    Step 5 - Calibrate the Touch Display:
      - Search "Calibrate the screen for pen or touch input" in the Start menu.
      - Select "Reset" to clear existing calibration data.
      - Follow on-screen prompts to re-calibrate the touch digitizer.

    Step 6 - Factory Reset (Last Resort):
      - Go to Settings > System > Recovery > Reset this PC.
      - Choose "Remove everything" for a clean reset.
      - Ensure data is backed up to OneDrive or external storage before proceeding.

    Escalation: If ghost touches persist after factory reset, the digitizer layer is physically damaged. Contact Microsoft Surface Support (1-800-642-7676) to initiate a device exchange under warranty. Surface Pro 9 has a 2-year hardware warranty with Microsoft Complete optional extension.
    """,

    """
    Document: Lenovo IdeaPad 5 Pro - Overheating and Thermal Throttling
    Model: Lenovo IdeaPad 5 Pro 16 (AMD Ryzen 7 6800H)
    Issue: Laptop overheating, fan running at max speed, CPU throttling under load
    Category: Thermal Management / Performance

    Symptoms:
    - CPU temperature exceeds 95°C during moderate tasks
    - Fan spins loudly at maximum RPM continuously
    - System performance drops significantly (thermal throttling detected in HWiNFO64)
    - Laptop surface is hot to touch, especially around keyboard and exhaust vents
    - System shuts down unexpectedly due to thermal protection

    Root Causes:
    1. Dried or depleted thermal paste on CPU/GPU die (common after 2+ years)
    2. Dust accumulation in heat sink fins and fan blades blocking airflow
    3. Lenovo Vantage power mode set to "Performance" without adequate cooling
    4. Background processes causing sustained high CPU usage
    5. Blocked ventilation from soft surfaces (fabric, bed) under the laptop

    Step-by-Step Troubleshooting:
    Step 1 - Monitor Temperatures:
      - Download and install HWiNFO64 (free utility at hwinfo.com).
      - Run a sensor-only scan and monitor "CPU Package" and "GPU Temperature" under load.
      - If idle temps exceed 60°C or load temps exceed 95°C consistently, thermal intervention is needed.

    Step 2 - Change Power Mode:
      - Open Lenovo Vantage app (install from Microsoft Store if missing).
      - Go to Device > My Device Settings > Thermal Mode.
      - Switch from "Performance" to "Balanced" or "Quiet" mode.
      - This adjusts the fan curve and power limits to reduce heat output.

    Step 3 - Kill Background Processes:
      - Open Task Manager (Ctrl + Shift + Esc).
      - Sort by CPU usage. Identify and end any non-essential processes above 10% usage.
      - Disable startup programs: Task Manager > Startup tab > Disable unnecessary items.

    Step 4 - Clean Cooling System (Technician):
      - Power off laptop and remove all power sources.
      - Remove base panel (typically 9x Phillips PH000 screws).
      - Use compressed air (in short bursts) to blow dust from the fan blades and heat sink fins. Hold the fan still with a finger while blowing to prevent over-spinning the fan motor.
      - If dust is heavy/matted, use a soft brush to loosen it first.

    Step 5 - Replace Thermal Paste (Technician):
      - Remove the heat sink assembly (4x spring-loaded screws on CPU, 2x on GPU - remove in reverse order from numbering).
      - Clean old thermal paste from CPU/GPU die and heat sink contact plate using 99% isopropyl alcohol and lint-free swabs.
      - Apply a small pea-sized amount of high-quality thermal compound (e.g., Thermal Grizzly Kryonaut) to the center of each die.
      - Reinstall heat sink in numbered order, tightening to 2-3 kgf·cm torque.
      - Re-test temperatures after reassembly.

    Escalation: If temperatures remain above 90°C after thermal paste replacement and cleaning, the heat sink may be warped or have insufficient contact pressure. Escalate to Tier 2 for heat sink replacement (Lenovo Part #5H40S20947).
    """,

    """
    Document: Dell Latitude 5540 - Blue Screen of Death (BSOD) DRIVER_IRQL Errors
    Model: Dell Latitude 5540 (Intel Core i7-1365U)
    Issue: Frequent BSOD crashes with DRIVER_IRQL_NOT_LESS_OR_EQUAL or SYSTEM_SERVICE_EXCEPTION
    Category: OS Stability / Driver Conflicts

    Symptoms:
    - Windows 11 crashes with blue screen showing DRIVER_IRQL_NOT_LESS_OR_EQUAL
    - BSOD occurs randomly, especially during network activity or USB device connection
    - System dumps a memory file and restarts automatically
    - Event Viewer shows critical errors pointing to ntoskrnl.exe or specific driver files
    - System has been recently updated or new software/hardware was added

    Root Causes:
    1. Faulty or incompatible network adapter driver (common culprit: Realtek or Intel NIC driver)
    2. Corrupted system files after Windows Update
    3. Defective RAM module causing memory access violations
    4. Incompatible third-party antivirus kernel driver
    5. Corrupted Windows pagefile

    Step-by-Step Troubleshooting:
    Step 1 - Analyze the Minidump File:
      - Navigate to C:\Windows\Minidump\ and note the most recent .dmp file.
      - Download WinDbg from the Microsoft Store.
      - Open WinDbg, go to File > Open crash dump, select the .dmp file.
      - In the command window, type: !analyze -v and press Enter.
      - Note the MODULE_NAME and FAULTING_MODULE fields - this identifies the problematic driver.

    Step 2 - Update or Rollback the Identified Driver:
      - Open Device Manager and locate the device corresponding to the identified driver.
      - Right-click > Properties > Driver tab.
      - If recently updated: click "Roll Back Driver".
      - If outdated: click "Update Driver" or download from Dell Support site.

    Step 3 - Run System File Checker (SFC) and DISM:
      - Open Command Prompt as Administrator.
      - Run: sfc /scannow — wait for completion (may take 15-20 minutes).
      - Then run: DISM /Online /Cleanup-Image /RestoreHealth
      - Restart after both complete successfully.

    Step 4 - Test RAM Modules:
      - Press Win + R, type "mdsched.exe", choose "Restart now and check for problems".
      - The Windows Memory Diagnostic will run on next boot (takes 10-20 minutes).
      - If errors are found, reseat the RAM stick (remove base panel, press tabs outward to release SODIMM).
      - If error persists with one stick, replace the faulty SODIMM (8GB or 16GB DDR4-3200).

    Step 5 - Disable Third-Party Antivirus:
      - Temporarily uninstall third-party antivirus software (e.g., McAfee, Norton, Kaspersky).
      - Use only Windows Defender and monitor for BSODs.
      - If BSODs stop, the antivirus kernel driver was the cause. Contact vendor for an updated version.

    Step 6 - Recreate Windows Pagefile:
      - Right-click This PC > Properties > Advanced System Settings > Advanced > Performance Settings.
      - Click Advanced > Virtual Memory > Change.
      - Uncheck "Automatically manage paging file size". Select "No paging file" and OK.
      - Restart. Then go back and set "System managed size" and restart again.

    Escalation: If BSODs persist after all driver and software fixes, and RAM tests clean, suspect a logic board issue. Submit a Tier 2 ticket with the full WinDbg output attached. Dell Latitude 5540 qualifies for ProSupport next-business-day on-site hardware repair.
    """,

    """
    Document: ASUS ZenBook 14 OLED - Black Screen After Lid Open / Wake from Sleep
    Model: ASUS ZenBook 14 OLED (UX3402, Intel Evo Platform)
    Issue: Display remains black after opening lid or resuming from sleep/hibernate
    Category: Power Management / Display

    Symptoms:
    - Opening the laptop lid results in a completely black screen (keyboard backlight works)
    - Pressing power button or any key does not wake the display
    - System appears to be running (HDD LED active, fans spinning)
    - Closing and reopening the lid sometimes fixes it temporarily
    - Issue appeared after a Windows 11 update

    Root Causes:
    1. Intel Display Driver bug with Modern Standby (S0 idle state)
    2. ASUS System Control Interface driver conflict with power management
    3. Hibernate file corruption causing resume failure
    4. BIOS setting for Panel Self Refresh (PSR) causing OLED driver mismatch
    5. Fast Startup feature causing incomplete resume sequence

    Step-by-Step Troubleshooting:
    Step 1 - Disable Fast Startup:
      - Go to Control Panel > Hardware and Sound > Power Options > Choose what the power buttons do.
      - Click "Change settings that are currently unavailable".
      - Uncheck "Turn on fast startup (recommended)" and save changes.
      - Restart the laptop and test wake behavior.

    Step 2 - Update Intel Graphics Driver:
      - Go to intel.com/download-center or use Intel Driver & Support Assistant.
      - Download the latest Intel Iris Xe Graphics driver.
      - During installation, choose "Clean Install" option to remove old driver files.
      - Restart and test.

    Step 3 - Update ASUS System Control Interface:
      - Open the MyASUS application.
      - Check for system driver updates, specifically "ASUS System Control Interface V3".
      - Install updates and restart.
      - Also update the BIOS through MyASUS > Customer Support > Live Update.

    Step 4 - Disable Panel Self Refresh (PSR) via Registry:
      - Open Registry Editor (Win + R > regedit).
      - Navigate to: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers
      - Right-click in the right pane > New > DWORD (32-bit) Value. Name it: TdrDelay
      - Set its value to 60 (decimal).
      - Also create another DWORD: DisablePSR and set it to 1.
      - Restart the laptop.

    Step 5 - Reset Power Plan and Sleep Settings:
      - Open Command Prompt as Administrator.
      - Run: powercfg /restoredefaultschemes
      - Go to Power Options > Change plan settings > Change advanced power settings.
      - Under "Sleep > Hibernate after", set to "Never" and test.

    Escalation: If the display consistently fails to wake and OS-level fixes are exhausted, the OLED panel's PSR controller or the Intel PCH may have a silicon bug requiring BIOS patch. File a support ticket with ASUS Enterprise Support and include the BIOS version and Windows build number. Hardware replacement (lid assembly) covered under ASUS Commercial Warranty if within 2 years.
    """,
]
