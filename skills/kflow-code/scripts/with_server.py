#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Two modes:
  One-shot (default): Start servers, run command, auto-cleanup on exit.
  Daemon (--daemon):   Start servers persistently, write state to file, return immediately.
                        Use --status, --health, --stop-all for lifecycle management.

Usage:
    # One-shot: single server
    python skills/kflow-code/scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py

    # One-shot: multiple servers
    python skills/kflow-code/scripts/with_server.py \
      --server "cd backend && python server.py" --port 3000 \
      --server "cd frontend && npm run dev" --port 5173 \
      -- python test.py

    # Daemon: start persistent service
    python skills/kflow-code/scripts/with_server.py --daemon --server "mvn spring-boot:run" --port 8080 --state-file .service-state.json

    # Daemon: start frontend + backend
    python skills/kflow-code/scripts/with_server.py --daemon \
      --server "mvn spring-boot:run" --port 8080 \
      --server "npm run dev" --port 5173 \
      --state-file .service-state.json

    # Daemon: query status
    python skills/kflow-code/scripts/with_server.py --status --state-file .service-state.json

    # Daemon: health check
    python skills/kflow-code/scripts/with_server.py --health --state-file .service-state.json

    # Daemon: stop all services
    python skills/kflow-code/scripts/with_server.py --stop-all --state-file .service-state.json
"""

import subprocess
import socket
import time
import sys
import os
import json
import argparse
import signal
import platform
import urllib.request
import urllib.error

IS_WINDOWS = platform.system() == "Windows"

DEFAULT_STATE_FILE = ".service-state.json"
STATE_FORMAT_VERSION = "1.0.0"

SIGTERM_TIMEOUT = 30
SIGKILL_TIMEOUT = 10
STOP_CHECK_INTERVAL = 2


# ---------------------------------------------------------------------------
# Port & process utilities
# ---------------------------------------------------------------------------

def check_port_occupied(port):
    """Check if a port is occupied. Returns (bool, pid_or_None, process_name_or_None)."""
    if IS_WINDOWS:
        return _check_port_windows(port)
    else:
        return _check_port_unix(port)


def _check_port_windows(port):
    try:
        output = subprocess.check_output(
            f'netstat -ano -p TCP 2>nul | findstr ":{port} " | findstr "LISTENING"',
            shell=True, text=True, timeout=10
        )
        lines = output.strip().splitlines()
        if lines:
            parts = lines[0].split()
            pid = int(parts[-1])
            try:
                proc_output = subprocess.check_output(
                    f'tasklist /FI "PID eq {pid}" /FO CSV 2>nul',
                    shell=True, text=True, timeout=5
                )
                proc_name = proc_output.strip().splitlines()[-1].split(',')[0].strip('"')
            except Exception:
                proc_name = "unknown"
            return True, pid, proc_name
    except (subprocess.CalledProcessError, ValueError, IndexError):
        pass
    return False, None, None


def _check_port_unix(port):
    try:
        output = subprocess.check_output(
            f"lsof -i :{port} -sTCP:LISTEN -t 2>/dev/null",
            shell=True, text=True, timeout=10
        )
        pid_str = output.strip()
        if pid_str:
            pid = int(pid_str.splitlines()[0])
            try:
                proc_output = subprocess.check_output(
                    f"ps -p {pid} -o comm= 2>/dev/null",
                    shell=True, text=True, timeout=5
                )
                proc_name = proc_output.strip()
            except Exception:
                proc_name = "unknown"
            return True, pid, proc_name
    except subprocess.CalledProcessError:
        pass
    return False, None, None


def is_process_alive(pid):
    """Check if a process with given PID is still running."""
    if IS_WINDOWS:
        try:
            subprocess.check_output(
                f'tasklist /FI "PID eq {pid}" 2>nul | findstr "{pid}"',
                shell=True, text=True, timeout=5
            )
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def stop_process(pid, force=False):
    """Stop a process. Returns True if process terminated."""
    if not is_process_alive(pid):
        return True
    try:
        if IS_WINDOWS:
            if force:
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, timeout=15)
            else:
                subprocess.run(f"taskkill /PID {pid}", shell=True, timeout=15)
        else:
            if force:
                os.kill(pid, signal.SIGKILL)
            else:
                os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        return not is_process_alive(pid)
    except Exception:
        return not is_process_alive(pid)


def stop_process_with_timeout_chain(pid):
    """Execute the full stop timeout chain: SIGTERM(30s) → SIGKILL(10s) → ERROR.

    Returns (success: bool, message: str).
    """
    if not is_process_alive(pid):
        return True, "already stopped"

    # Phase 1: SIGTERM
    stop_process(pid, force=False)
    waited = 0
    while waited < SIGTERM_TIMEOUT:
        if not is_process_alive(pid):
            return True, "stopped (SIGTERM)"
        time.sleep(STOP_CHECK_INTERVAL)
        waited += STOP_CHECK_INTERVAL

    # Phase 2: SIGKILL
    stop_process(pid, force=True)
    waited = 0
    while waited < SIGKILL_TIMEOUT:
        if not is_process_alive(pid):
            return True, "stopped (SIGKILL, forced)"
        time.sleep(STOP_CHECK_INTERVAL)
        waited += STOP_CHECK_INTERVAL

    # Phase 3: ERROR — zombie process
    return False, f"zombie process: PID {pid} did not terminate after SIGTERM({SIGTERM_TIMEOUT}s) + SIGKILL({SIGKILL_TIMEOUT}s)"


def is_port_released(port, timeout=5):
    """Wait until a port is released. Returns True if released."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        occupied, _, _ = check_port_occupied(port)
        if not occupied:
            return True
        time.sleep(0.5)
    return False


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def health_check_endpoint(port, endpoint="/health", timeout=10):
    """Check an HTTP health endpoint. Returns (status_code, body)."""
    url = f"http://localhost:{port}{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode(errors='replace')[:500]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors='replace')[:500]
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# State file management
# ---------------------------------------------------------------------------

def load_state_file(state_path):
    """Load the service state JSON file."""
    if not os.path.exists(state_path):
        return None
    with open(state_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state_file(state_path, data):
    """Save the service state JSON file."""
    data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_state_entry(service_id, service_type, pid, port, start_command,
                       health_endpoint="/health", db_health_endpoint=None):
    """Create a new state file entry."""
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    entry = {
        "id": service_id,
        "type": service_type,
        "pid": pid,
        "port": port,
        "start_command": start_command,
        "start_time": now,
        "health_endpoint": health_endpoint,
        "health_status": "starting",
        "last_health_check": now
    }
    if db_health_endpoint:
        entry["db_health_endpoint"] = db_health_endpoint
    return entry


# ---------------------------------------------------------------------------
# Daemon commands
# ---------------------------------------------------------------------------

def cmd_status(args):
    """Handle --status command."""
    state = load_state_file(args.state_file)
    if not state or not state.get("services"):
        print("No services found in state file.")
        return 1

    print(f"{'ID':<20} {'PID':<8} {'PORT':<6} {'STATUS':<12} {'START_TIME':<20} {'HEALTH':<10}")
    print("-" * 80)
    for svc in state["services"]:
        alive = "running" if is_process_alive(svc["pid"]) else "dead"
        print(f"{svc['id']:<20} {svc['pid']:<8} {svc['port']:<6} {alive:<12} {svc['start_time']:<20} {svc.get('health_status', 'unknown'):<10}")
    return 0


def cmd_health(args):
    """Handle --health command."""
    state = load_state_file(args.state_file)
    if not state or not state.get("services"):
        print("No services found in state file.")
        return 1

    all_healthy = True
    for svc in state["services"]:
        if not is_process_alive(svc["pid"]):
            print(f"[UNHEALTHY] {svc['id']} (PID {svc['pid']}): process not running")
            svc["health_status"] = "unhealthy"
            all_healthy = False
            continue

        status_code, body = health_check_endpoint(svc["port"], svc.get("health_endpoint", "/health"))
        if status_code == 200:
            svc["health_status"] = "healthy"
            print(f"[HEALTHY]   {svc['id']} (port {svc['port']}): HTTP {status_code}")
        else:
            svc["health_status"] = "unhealthy"
            print(f"[UNHEALTHY] {svc['id']} (port {svc['port']}): HTTP {status_code}, body: {body[:100]}")
            all_healthy = False

        svc["last_health_check"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")

        # Also check /db-health for backend services
        db_endpoint = svc.get("db_health_endpoint")
        if db_endpoint:
            db_code, db_body = health_check_endpoint(svc["port"], db_endpoint)
            if db_code == 200:
                print(f"  [DB-OK]    {svc['id']}: HTTP {db_code}")
            else:
                print(f"  [DB-FAIL]  {svc['id']}: HTTP {db_code}, body: {db_body[:100]}")
                all_healthy = False

    save_state_file(args.state_file, state)
    return 0 if all_healthy else 1


def cmd_stop_all(args):
    """Handle --stop-all command."""
    state = load_state_file(args.state_file)
    if not state or not state.get("services"):
        print("No services found in state file.")
        return 0

    all_stopped = True
    # Stop in reverse order (last started first stopped)
    for svc in reversed(state["services"]):
        print(f"Stopping {svc['id']} (PID {svc['pid']}, port {svc['port']})...")
        success, msg = stop_process_with_timeout_chain(svc["pid"])
        if success:
            print(f"  {msg}")
            svc["health_status"] = "stopped"
        else:
            print(f"  ERROR: {msg}")
            all_stopped = False

    # Verify ports are released
    for svc in state["services"]:
        if not is_port_released(svc["port"]):
            occupied, pid, proc_name = check_port_occupied(svc["port"])
            if occupied:
                print(f"  ERROR: Port {svc['port']} still occupied by PID {pid} ({proc_name})")
                all_stopped = False

    if all_stopped:
        # Remove state file
        try:
            os.remove(args.state_file)
            print(f"State file {args.state_file} removed.")
        except OSError:
            pass
        return 0
    else:
        save_state_file(args.state_file, state)
        print("Some services could not be stopped. State file preserved.")
        return 1


# ---------------------------------------------------------------------------
# One-shot mode (original behavior, enhanced)
# ---------------------------------------------------------------------------

def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def run_one_shot(args):
    """Original one-shot mode: start servers, run command, cleanup."""
    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    servers = _parse_servers(args)

    server_processes = []
    try:
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}")
            process = subprocess.Popen(
                server['cmd'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            server_processes.append((process, server['port']))

            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(
                    f"Server failed to start on port {server['port']} within {args.timeout}s"
                )
            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, (process, port) in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} (port {port}) stopped")
        print("All servers stopped")


# ---------------------------------------------------------------------------
# Daemon mode
# ---------------------------------------------------------------------------

def run_daemon(args):
    """Daemon mode: start servers persistently, write state file, return."""
    servers = _parse_servers(args)

    # Load or create state file
    state = load_state_file(args.state_file)
    if not state:
        state = {
            "version": STATE_FORMAT_VERSION,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "services": []
        }

    existing_ports = {svc["port"] for svc in state["services"] if svc.get("health_status") != "stopped"}

    new_services = []
    for server in servers:
        port = server['port']
        service_id = server.get('id', f"service-{port}")

        # Port conflict detection
        occupied, occ_pid, occ_name = check_port_occupied(port)
        if occupied:
            # Check if this is a previously recorded service
            known_pids = {svc["pid"] for svc in state["services"]}
            if occ_pid in known_pids:
                print(f"Port {port}: occupied by known service (PID {occ_pid}), stopping stale process...")
                success, msg = stop_process_with_timeout_chain(occ_pid)
                if not success:
                    print(f"ERROR: Failed to stop stale process on port {port}: {msg}")
                    sys.exit(1)
                print(f"  Stale process stopped: {msg}")
            else:
                # Not our process — block
                print(f"ERROR: Port {port} is occupied by an unexpected process:")
                print(f"  PID: {occ_pid}")
                print(f"  Process: {occ_name}")
                print(f"  Action: Please stop this process manually before starting services.")
                print(f"  To stop: {'taskkill /PID ' + str(occ_pid) if IS_WINDOWS else 'kill ' + str(occ_pid)}")
                sys.exit(1)

        # Start service
        print(f"Starting service '{service_id}': {server['cmd']}")
        process = subprocess.Popen(
            server['cmd'],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            # On Windows, CREATE_NEW_PROCESS_GROUP to avoid inheriting CTRL+C
            **(dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) if IS_WINDOWS else {})
        )

        # Wait for port readiness
        print(f"Waiting for service on port {port}...")
        if not is_server_ready(port, timeout=args.timeout):
            print(f"ERROR: Service failed to start on port {port} within {args.timeout}s")
            stop_process_with_timeout_chain(process.pid)
            sys.exit(1)

        # Health check
        health_endpoint = server.get('health_endpoint', '/health')
        db_health_endpoint = server.get('db_health_endpoint')
        print(f"Health check on port {port}{health_endpoint}...")
        status_code, body = health_check_endpoint(port, health_endpoint)
        if status_code != 200:
            print(f"WARNING: Health check returned HTTP {status_code}: {body[:100]}")
        else:
            print(f"  Health check: HTTP {status_code}")

        svc_type = server.get('type', 'backend' if db_health_endpoint else 'frontend')
        entry = create_state_entry(
            service_id=service_id,
            service_type=svc_type,
            pid=process.pid,
            port=port,
            start_command=server['cmd'],
            health_endpoint=health_endpoint,
            db_health_endpoint=db_health_endpoint
        )
        entry["health_status"] = "healthy" if status_code == 200 else "starting"
        new_services.append(entry)
        print(f"Service '{service_id}' started (PID {process.pid}, port {port})")

    # Update state file
    state["services"].extend(new_services)
    save_state_file(args.state_file, state)
    print(f"\n{len(new_services)} service(s) started. State saved to {args.state_file}.")


# ---------------------------------------------------------------------------
# Argument parsing & dispatch
# ---------------------------------------------------------------------------

def _parse_servers(args):
    """Parse --server/--port args into a list of server dicts."""
    if not args.servers or not args.ports:
        print("Error: --server and --port are required")
        sys.exit(1)
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    servers = []
    for i, (cmd, port) in enumerate(zip(args.servers, args.ports)):
        svc = {'cmd': cmd, 'port': port, 'id': f"service-{port}"}
        # Attach optional per-server args if provided
        if hasattr(args, 'service_ids') and args.service_ids and i < len(args.service_ids):
            svc['id'] = args.service_ids[i]
        if hasattr(args, 'health_endpoints') and args.health_endpoints and i < len(args.health_endpoints):
            svc['health_endpoint'] = args.health_endpoints[i]
        if hasattr(args, 'db_health_endpoints') and args.db_health_endpoints and i < len(args.db_health_endpoints):
            svc['db_health_endpoint'] = args.db_health_endpoints[i]
        if hasattr(args, 'service_types') and args.service_types and i < len(args.service_types):
            svc['type'] = args.service_types[i]
        servers.append(svc)
    return servers


def main():
    parser = argparse.ArgumentParser(
        description='Run command with one or more servers (one-shot or daemon mode)'
    )

    # Mode selection
    parser.add_argument('--daemon', action='store_true',
                        help='Start servers in daemon (persistent) mode')
    parser.add_argument('--status', action='store_true',
                        help='Query status of all services in state file')
    parser.add_argument('--health', action='store_true',
                        help='Health check all services in state file')
    parser.add_argument('--stop-all', action='store_true',
                        help='Stop all services in state file with timeout chain')

    # General options
    parser.add_argument('--server', action='append', dest='servers',
                        help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int,
                        help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=60,
                        help='Timeout in seconds per server (default: 60)')
    parser.add_argument('--state-file', default=DEFAULT_STATE_FILE,
                        help=f'State file path (default: {DEFAULT_STATE_FILE})')

    # Per-server options (daemon mode)
    parser.add_argument('--service-id', action='append', dest='service_ids',
                        help='Service ID for each server (can be repeated)')
    parser.add_argument('--health-endpoint', action='append', dest='health_endpoints',
                        help='Health endpoint path for each server (default: /health)')
    parser.add_argument('--db-health-endpoint', action='append', dest='db_health_endpoints',
                        help='DB health endpoint path for each server')
    parser.add_argument('--service-type', action='append', dest='service_types',
                        help='Service type: backend or frontend')

    # Remaining args go to command (one-shot mode only)
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help='Command to run after server(s) ready (one-shot mode)')

    args = parser.parse_args()

    # Dispatch to the appropriate handler
    if args.status:
        sys.exit(cmd_status(args))

    if args.health:
        sys.exit(cmd_health(args))

    if args.stop_all:
        sys.exit(cmd_stop_all(args))

    if args.daemon:
        if not args.servers:
            print("Error: --daemon mode requires --server and --port arguments")
            sys.exit(1)
        run_daemon(args)
        return

    # One-shot mode (original behavior)
    if not args.servers:
        print("Error: --server and --port are required (or use --status/--health/--stop-all/--daemon)")
        sys.exit(1)

    # Strip '--' separator
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]
    if not args.command:
        print("Error: No command specified to run (use --daemon for persistent mode)")
        sys.exit(1)

    run_one_shot(args)


if __name__ == '__main__':
    main()
