"""
Comprehensive Rich Logging Demo - Combining basic and advanced rich library capabilities
"""
import logging
import time
import threading
import random
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
from rich.traceback import install
from rich.syntax import Syntax
from rich.pretty import pprint, install as pretty_install
from rich.live import Live
from rich.layout import Layout
from dataclasses import dataclass
from typing import List, Dict, Any

# Install rich traceback handler
install(show_locals=True)

# Configure rich logger
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

# Create main logger
log = logging.getLogger("rich_demo")

# Create loggers for different components (for advanced demos)
system_log = logging.getLogger("system")
network_log = logging.getLogger("network")
database_log = logging.getLogger("database")
auth_log = logging.getLogger("auth")

console = Console()

# Basic Demo Functions

def demo_basic_logging():
    """Demonstrate basic logging with Rich."""
    console.rule("Basic Logging Demo")
    log.info("This is a basic info message")
    log.warning("This is a warning message with [bold yellow]highlighted text[/]")
    log.error("This is an error message with %s", "dynamic content")
    log.debug("This debug message won't show with default settings")

    # Change the log level temporarily to show debug messages
    log.setLevel(logging.DEBUG)
    log.debug("Now you can see debug messages!")
    log.setLevel(logging.INFO)

    # Log exception with traceback
    try:
        1 / 0
    except Exception:
        log.exception("An exception occurred")

def demo_rich_progress():
    """Demonstrate Rich progress bars."""
    console.rule("Progress Bar Demo")

    console.print("Simple progress bar:")
    for step in track(range(50), description="Processing..."):
        time.sleep(0.02)  # Simulate work

    console.print("[green]Done![/green]")

def demo_rich_tables():
    """Demonstrate Rich tables."""
    console.rule("Tables Demo")

    table = Table(title="Rich Features Overview")

    table.add_column("Feature", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Example", style="magenta")

    table.add_row(
        "Logging",
        "Enhanced logging with colors and formatting",
        "log.info('Message')"
    )
    table.add_row(
        "Progress Bars",
        "Visual progress indicators",
        "track(range(100))"
    )
    table.add_row(
        "Tables",
        "Structured tabular data",
        "Table(title='Example')"
    )
    table.add_row(
        "Panels",
        "Boxed content with borders",
        "Panel('Content')"
    )
    table.add_row(
        "Markdown",
        "Render markdown content",
        "Markdown('# Title')"
    )

    console.print(table)

def demo_rich_panels():
    """Demonstrate Rich panels."""
    console.rule("Panels Demo")

    panel = Panel.fit(
        "[bold green]Rich[/] makes creating beautiful terminal output easy",
        title="About Rich",
        border_style="blue"
    )
    console.print(panel)

# Advanced Demo Functions

def demo_log_levels():
    """Demonstrate different log levels."""
    console.rule("Log Levels Demo")

    log = logging.getLogger("levels_demo")

    log.debug("This is a [blue]DEBUG[/blue] message (won't show with default settings)")
    log.info("This is an [green]INFO[/green] message")
    log.warning("This is a [yellow]WARNING[/yellow] message")
    log.error("This is a [red]ERROR[/red] message")
    log.critical("This is a [bold red]CRITICAL[/bold red] message")

    console.print()

    # Show debug messages by changing the log level
    console.print("[yellow]Changing log level to DEBUG to show all messages...[/yellow]")
    log.setLevel(logging.DEBUG)

    log.debug("Now you can see [blue]DEBUG[/blue] messages too!")

    # Reset log level
    log.setLevel(logging.INFO)

@dataclass
class User:
    """Example user class for pretty printing demo."""
    id: int
    username: str
    email: str
    active: bool
    permissions: List[str]


class Server:
    """Example server class for pretty printing demo."""
    def __init__(self, name: str, ip: str, ports: List[int], config: Dict[str, Any]):
        self.name = name
        self.ip = ip
        self.ports = ports
        self.config = config
        self.status = "running"
        self.uptime = "3d 12h 45m"

    def __repr__(self):
        return f"Server({self.name}, {self.ip})"


def demo_pretty_printing():
    """Demonstrate pretty printing of Python objects."""
    console.rule("Pretty Printing Demo")

    # Install rich pretty printing for all repr calls
    pretty_install()

    # Create some sample objects
    user1 = User(
        id=1001,
        username="alice_admin",
        email="alice@example.com",
        active=True,
        permissions=["read", "write", "admin"]
    )

    user2 = User(
        id=1002,
        username="bob_user",
        email="bob@example.com",
        active=False,
        permissions=["read"]
    )

    server = Server(
        name="prod-db-01",
        ip="192.168.1.100",
        ports=[22, 80, 443, 5432],
        config={
            "max_connections": 1000,
            "timeout": 30,
            "ssl_enabled": True,
            "backup": {
                "schedule": "daily",
                "retention": "7d"
            }
        }
    )

    # Pretty print the objects
    console.print("\n[bold blue]Pretty printing User object:[/]")
    console.print(user1)

    console.print("\n[bold blue]Pretty printing a list of User objects:[/]")
    console.print([user1, user2])

    console.print("\n[bold blue]Pretty printing Server object:[/]")
    console.print(server)

    # Create a complex nested structure
    complex_data = {
        "users": [user1, user2],
        "servers": [server, Server(
            name="prod-app-01",
            ip="192.168.1.101",
            ports=[22, 8080],
            config={
                "workers": 4,
                "debug": False,
                "env": "production"
            }
        )],
        "statistics": {
            "total_users": 2,
            "active_users": 1,
            "server_status": [("prod-db-01", "up"), ("prod-app-01", "up")],
            "performance": {
                "cpu": 0.35,
                "memory": 0.7,
                "disk": 0.5
            }
        }
    }

    console.print("\n[bold blue]Pretty printing complex nested structure:[/]")
    console.print(complex_data)

    # Using pprint function directly
    console.print("\n[bold blue]Using pprint function:[/]")
    pprint(complex_data["statistics"], expand_all=True)


def demo_side_by_side_panels():
    """Demonstrate pretty printed objects in side-by-side panels."""
    console.rule("Side-by-Side Panels Demo")
    console.print("[bold yellow]Displaying system information in side-by-side panels[/]")

    # Create sample data for panels
    system_stats = {
        "cpu_usage": 32.5,
        "memory_usage": 48.7,
        "disk_usage": 76.2,
        "network_throughput": "1.2 GB/s",
        "processes": 186,
        "uptime": "3d 12h 45m"
    }

    active_users = [
        {"username": "alice", "role": "admin", "session_time": "2h 15m"},
        {"username": "bob", "role": "user", "session_time": "45m"},
        {"username": "charlie", "role": "developer", "session_time": "5h 30m"},
        {"username": "dave", "role": "user", "session_time": "10m"}
    ]

    recent_errors = [
        {"time": "10:45:23", "service": "web-server", "message": "Connection timeout"},
        {"time": "11:02:15", "service": "database", "message": "Query execution error"},
        {"time": "11:15:07", "service": "auth", "message": "Failed login attempt"},
    ]

    # Create a layout with three equal columns
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower"),
    )

    # Split upper section into three columns
    layout["upper"].split_row(
        Layout(name="stats"),
        Layout(name="users"),
        Layout(name="errors"),
    )

    # Create string representations for the panels using rich's formatting
    stats_content = ""
    for key, value in system_stats.items():
        stats_content += f"[cyan]{key}[/cyan]: [yellow]{value}[/yellow]\n"

    users_content = ""
    for user in active_users:
        users_content += f"[bold]{user['username']}[/bold] ([green]{user['role']}[/green]): {user['session_time']}\n"

    errors_content = ""
    for error in recent_errors:
        errors_content += f"[dim]{error['time']}[/dim] - [bold red]{error['service']}[/bold red]: {error['message']}\n"

    # Create panels with formatted content
    stats_panel = Panel(
        stats_content,
        title="[bold blue]System Statistics[/]",
        border_style="blue"
    )

    users_panel = Panel(
        users_content,
        title="[bold green]Active Users[/]",
        border_style="green"
    )

    errors_panel = Panel(
        errors_content,
        title="[bold red]Recent Errors[/]",
        border_style="red"
    )

    # Add a code sample with syntax highlighting in the lower panel
    code = """
def update_dashboard():
    \"\"\"Update the dashboard with latest metrics.\"\"\"
    stats = get_system_stats()
    users = get_active_users()
    errors = get_recent_errors()

    display_panels(stats, users, errors)
    """

    code_panel = Panel(
        Syntax(code, "python", theme="monokai", line_numbers=True),
        title="[bold magenta]Dashboard Update Code[/]",
        border_style="magenta"
    )

    # Update layout with panels
    layout["stats"].update(stats_panel)
    layout["users"].update(users_panel)
    layout["errors"].update(errors_panel)
    layout["lower"].update(code_panel)

    # Display the layout
    console.print(layout)
    console.print()

def simulate_system_activity():
    """Simulate system activity with logs."""
    activities = [
        "Starting system services",
        "Checking disk space",
        "Monitoring CPU usage",
        "Running scheduled tasks",
        "Cleaning temporary files"
    ]

    for _ in range(10):
        system_log.info(random.choice(activities))
        time.sleep(random.uniform(0.5, 1.5))

    if random.random() < 0.3:
        system_log.warning("High memory usage detected")

def simulate_network_activity():
    """Simulate network activity with logs."""
    for _ in range(8):
        if random.random() < 0.7:
            network_log.info(f"Connection from IP: 192.168.1.{random.randint(2, 254)}")
        else:
            network_log.warning(f"Failed connection attempt from IP: 10.0.0.{random.randint(2, 254)}")
        time.sleep(random.uniform(0.3, 1.0))

    if random.random() < 0.2:
        network_log.error("Network interface down")

def simulate_database_activity():
    """Simulate database activity with logs."""
    tables = ["users", "products", "orders", "inventory", "payments"]
    operations = ["SELECT", "INSERT", "UPDATE", "DELETE"]

    for _ in range(12):
        table = random.choice(tables)
        operation = random.choice(operations)

        if random.random() < 0.8:
            database_log.info(f"[blue]{operation}[/blue] operation on [green]{table}[/green] table")
        else:
            database_log.warning(f"Slow query detected: [blue]{operation}[/blue] on [green]{table}[/green]")

        time.sleep(random.uniform(0.2, 0.8))

    if random.random() < 0.15:
        database_log.error("Database connection timeout")

def simulate_auth_activity():
    """Simulate authentication activity with logs."""
    users = ["alice", "bob", "charlie", "dave", "eve", "frank"]

    for _ in range(6):
        user = random.choice(users)

        if random.random() < 0.85:
            auth_log.info(f"User '{user}' logged in successfully")
        else:
            auth_log.warning(f"Failed login attempt for user '{user}'")

            # Sometimes generate a critical error
            if random.random() < 0.3:
                auth_log.critical(f"[bold red]Multiple failed login attempts for '{user}'[/bold red]")

        time.sleep(random.uniform(0.5, 2.0))

def demo_simulated_activity():
    """Run all simulated activity demonstrations."""
    console.rule("Simulated System Activity")
    console.print("[yellow]Starting simulated system activity...[/]")

    # Start each activity simulation in a separate thread
    threads = [
        threading.Thread(target=simulate_system_activity),
        threading.Thread(target=simulate_network_activity),
        threading.Thread(target=simulate_database_activity),
        threading.Thread(target=simulate_auth_activity)
    ]

    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    console.print()
    console.print("[bold green]Simulation completed![/]")

def show_rich_logging_example():
    """Show a code example with syntax highlighting for rich logging setup."""
    code = '''
import logging
from rich.logging import RichHandler

# Configure rich logger
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("example")
log.info("Rich logging is [bold green]awesome![/]")
'''

    console.print(Panel(
        Syntax(code, "python", theme="monokai", line_numbers=True),
        title="How to Set Up Rich Logging",
        border_style="green"
    ))

def main():
    """Run the comprehensive rich logging demo."""
    console.clear()
    console.print("[bold blue]Comprehensive Rich Logging Demo[/]")
    console.print("[yellow]Showing both basic and advanced features of the Rich library[/yellow]")
    console.print()

    # Basic demos
    console.rule("[bold cyan]Basic Rich Features[/]")
    demo_basic_logging()
    console.print()

    demo_rich_progress()
    console.print()

    demo_rich_tables()
    console.print()

    demo_rich_panels()
    console.print()

    # Advanced demos
    console.rule("[bold magenta]Advanced Rich Features[/]")
    demo_log_levels()
    console.print()

    demo_pretty_printing()
    console.print()

    demo_side_by_side_panels()
    console.print()

    demo_simulated_activity()
    console.print()

    # Show example code
    show_rich_logging_example()

    console.rule()
    console.print("[bold green]Comprehensive Rich logging demo completed![/]")

if __name__ == "__main__":
    main()
