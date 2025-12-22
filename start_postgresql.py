"""
PostgreSQL Service Starter
This script attempts to start PostgreSQL and verify the connection.
Note: Requires Administrator privileges to start services.
"""
import subprocess
import sys
import time

def start_postgresql_service():
    """Attempt to start PostgreSQL service"""
    service_name = "postgresql-x64-18"
    
    print("=" * 60)
    print("PostgreSQL Service Starter")
    print("=" * 60)
    print(f"\nAttempting to start service: {service_name}")
    print("\nNOTE: This requires Administrator privileges.")
    print("If this fails, run PowerShell as Administrator and use:")
    print(f"  net start {service_name}")
    print("\n" + "-" * 60)
    
    try:
        # Try to start the service
        result = subprocess.run(
            ['net', 'start', service_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"\n[SUCCESS] Service '{service_name}' started successfully!")
            print(result.stdout)
            return True
        else:
            print(f"\n[FAILED] Could not start service.")
            print("Error output:", result.stderr)
            print("\n[SOLUTION] Run PowerShell as Administrator:")
            print(f"  net start {service_name}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n[ERROR] Command timed out.")
        return False
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")
        print("\n[SOLUTION] Run PowerShell as Administrator:")
        print(f"  net start {service_name}")
        return False

def check_service_status(service_name):
    """Check if PostgreSQL service is running"""
    print("\n" + "-" * 60)
    print("Checking service status...")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             f'Get-Service -Name "{service_name}" | Select-Object Name, Status, DisplayName | Format-Table -AutoSize'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout.strip():
            print(result.stdout)
            if "Running" in result.stdout:
                return True
        return False
    except Exception as e:
        print(f"Could not check status: {e}")
        return False

def main():
    service_name = "postgresql-x64-18"
    
    # Check current status first
    print("\nChecking current PostgreSQL service status...")
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             f'Get-Service -Name "{service_name}" | Select-Object Name, Status | Format-Table -AutoSize'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout.strip():
            print(result.stdout)
            if "Running" in result.stdout:
                print("\n[INFO] PostgreSQL service is already running!")
                print("You can now run: python tes_save_call.py")
                return
    except:
        pass
    
    # Try to start
    success = start_postgresql_service()
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] PostgreSQL should now be running!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run: python check_postgresql.py")
        print("  2. Or test: python tes_save_call.py")
    else:
        print("\n" + "=" * 60)
        print("[ACTION REQUIRED]")
        print("=" * 60)
        print("\nTo start PostgreSQL manually:")
        print("  1. Right-click PowerShell -> Run as Administrator")
        print(f"  2. Run: net start {service_name}")
        print("\nOr use Services GUI:")
        print("  1. Press Win+R, type 'services.msc', press Enter")
        print(f"  2. Find '{service_name}'")
        print("  3. Right-click -> Start")
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

