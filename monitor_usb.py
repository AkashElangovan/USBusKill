import wmi
import os
import datetime
import time

def log_event(event_type, drive_letter=None):
    with open("usb_log.txt", "a") as f:
        if drive_letter:
            f.write(f"{datetime.datetime.now()}: USB {drive_letter} {event_type}\n")
        else:
            f.write(f"{datetime.datetime.now()}: USB {event_type}\n")

def usb_removed(drive_letter):
    log_event("removed", drive_letter)
    print(f"USB {drive_letter} removed! Locking system...")
    os.system("rundll32.exe user32.dll,LockWorkStation")  # Lock the system

def usb_inserted(drive_letter):
    log_event("inserted", drive_letter)
    print(f"USB {drive_letter} inserted.")

def get_usb_drive_letter():
    # This function can be customized to detect the specific USB drive
    # For now, it returns the drive letter 'D:'
    return "D:"

def monitor_usb():
    c = wmi.WMI()
    drive_letter = get_usb_drive_letter()

    # Watch for USB insertion (EventType=2) and removal (EventType=3)
    insert_watcher = c.Win32_DeviceChangeEvent.watch_for(EventType=2)
    remove_watcher = c.Win32_DeviceChangeEvent.watch_for(EventType=3)

    print(f"Listening for USB events on drive {drive_letter}...")
    while True:
        try:
            # Check for USB insertion
            insert_watcher()
            usb_inserted(drive_letter)

            # Check for USB removal
            remove_watcher()
            usb_removed(drive_letter)
        except wmi.x_wmi_timed_out:
            # Timeout while waiting for events (normal behavior)
            pass
        except Exception as e:
            print(f"Error: {e}")
        finally:
            time.sleep(1)  # Reduce CPU usage

if __name__ == "__main__":
    try:
        monitor_usb()
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")