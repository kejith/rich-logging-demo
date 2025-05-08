import logging
import random
import time
import threading
from dataclasses import dataclass
from typing import List, Optional
from datetime import date
from rich.console import Console, ConsoleOptions, RenderResult, Group, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.logging import RichHandler
from rich.text import Text
from rich.live import Live

# Set up rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")


@dataclass
class Address:
    """Represents a physical address."""

    street: str
    city: str
    state: str
    zip_code: str
    country: str
    address_type: str = "Home"  # Home, Work, Other

    def __str__(self) -> str:
        return (
            f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"
        )


class Person:
    """
    Person class with rich console rendering capabilities.
    Will display as a panel with embedded address table.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        email: str,
        phone: str,
        occupation: str = "",
        addresses: Optional[List[Address]] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone = phone
        self.occupation = occupation
        self.addresses = addresses or []

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def add_address(self, address: Address) -> None:
        """Add an address to this person."""
        self.addresses.append(address)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Custom rich rendering for the Person class."""
        # Create a table for the addresses
        address_table = Table(
            title="Addresses", show_header=True, header_style="bold magenta"
        )
        address_table.add_column("Type", style="dim")
        address_table.add_column("Street")
        address_table.add_column("City")
        address_table.add_column("State")
        address_table.add_column("Zip")
        address_table.add_column("Country")

        # Add rows for each address
        for addr in self.addresses:
            address_table.add_row(
                addr.address_type,
                addr.street,
                addr.city,
                addr.state,
                addr.zip_code,
                addr.country,
            )

        # Create basic info section
        basic_info = Text()
        basic_info.append(f"Name: ", style="bold")
        basic_info.append(f"{self.full_name}\n", style="cyan")
        basic_info.append(f"Age: ", style="bold")
        basic_info.append(f"{self.age}\n", style="cyan")
        basic_info.append(f"Birth Date: ", style="bold")
        basic_info.append(f"{self.birth_date.strftime('%B %d, %Y')}\n", style="cyan")
        basic_info.append(f"Email: ", style="bold")
        basic_info.append(f"{self.email}\n", style="cyan")
        basic_info.append(f"Phone: ", style="bold")
        basic_info.append(f"{self.phone}\n", style="cyan")

        if self.occupation:
            basic_info.append(f"Occupation: ", style="bold")
            basic_info.append(f"{self.occupation}\n", style="cyan")

        content = Group(basic_info, address_table)

        panel = Panel(
            content,
            title=f"[bold blue]{self.full_name}[/]",
            border_style="blue",
            padding=(1, 2),
        )
        yield panel

    def __str__(self) -> str:
        return self.full_name

    def rich_panel(self, border_style: str = "bright_blue") -> Panel:
        """Create a rich panel for this person with configurable border style."""
        # Create a table for the addresses
        address_table = Table(
            title="Addresses", show_header=True, header_style="bold magenta"
        )
        address_table.add_column("Type", style="dim")
        address_table.add_column("Street")
        address_table.add_column("City")
        address_table.add_column("State")
        address_table.add_column("Zip")
        address_table.add_column("Country")

        # Add rows for each address
        for addr in self.addresses:
            address_table.add_row(
                addr.address_type,
                addr.street,
                addr.city,
                addr.state,
                addr.zip_code,
                addr.country,
            )

        # Create basic info section
        basic_info = Text()
        basic_info.append(f"Name: ", style="bold")
        basic_info.append(f"{self.full_name}\n", style="cyan")
        basic_info.append(f"Age: ", style="bold")
        basic_info.append(f"{self.age}\n", style="cyan")
        basic_info.append(f"Birth Date: ", style="bold")
        basic_info.append(f"{self.birth_date.strftime('%B %d, %Y')}\n", style="cyan")
        basic_info.append(f"Email: ", style="bold")
        basic_info.append(f"{self.email}\n", style="cyan")
        basic_info.append(f"Phone: ", style="bold")
        basic_info.append(f"{self.phone}\n", style="cyan")

        if self.occupation:
            basic_info.append(f"Occupation: ", style="bold")
            basic_info.append(f"{self.occupation}\n", style="cyan")

        content = Group(basic_info, address_table)

        return Panel(
            content,
            title=f"[bold {border_style}]{self.full_name}[/bold {border_style}]",
            border_style=border_style,
            padding=(1, 2),
            expand=True
        )


class RichGridLogger:
    """A rich logger that can display a grid of renderables."""

    def __init__(self):
        self.console = Console()
        self.items: List[RenderableType] = []
        self.running = False

    def add_item(self, item: RenderableType, name: Optional[str] = None) -> None:
        """
        Add a renderable item to the grid.

        Args:
            item: Any Rich renderable object
            name: Optional name for logging purposes (defaults to str(item))
        """
        self.items.append(item)
        item_name = name or str(item)
        log.info(f"Added {item_name} to the grid")

    def add_items(self, items: List[RenderableType], names: Optional[List[str]] = None) -> None:
        """
        Add multiple renderable items to the grid.

        Args:
            items: List of Rich renderable objects
            names: Optional list of names for logging (defaults to str(item) for each)
        """
        self.items.extend(items)
        log.info(f"Added {len(items)} items to the grid")

    # Keep for backward compatibility
    def add_person(self, person: Person) -> None:
        """Add a person to the grid (for backward compatibility)."""
        self.add_item(person, person.full_name)

    # Keep for backward compatibility
    def add_people(self, people: List[Person]) -> None:
        """Add multiple people to the grid (for backward compatibility)."""
        self.add_items(people)

    def display_grid(self, min_width: int) -> None:
        """Display the items in a grid layout with the specified number of columns."""
        grid = self._display_grid_with_highlight(min_width)
        self.console.print(grid)

    def _can_apply_rich_panel(self, item: RenderableType) -> bool:
        """Check if the item has a rich_panel method."""
        return hasattr(item, 'rich_panel') and callable(getattr(item, 'rich_panel'))

    def _get_item_panel(self, item: RenderableType, border_style: str) -> Panel:
        """Get a panel representation of the item with the specified border style."""
        if self._can_apply_rich_panel(item):
            return item.rich_panel(border_style)
        else:
            # Create a basic panel for items that don't have a rich_panel method
            return Panel(
                item,
                border_style=border_style,
                padding=(1, 2),
                expand=True
            )

    def _display_grid_with_highlight(self, min_width: int, highlight_idx: Optional[int] = None) -> Table:
        """Display the items in a grid layout with the specified item highlighted."""
        if not self.items:
            log.warning("No items to display")
            return None

        console_width = self.console.width
        columns = max(1, console_width // min_width)  # Calculate number of columns based on console width

        # Calculate how many rows we need
        total_items = len(self.items)
        rows = (total_items + columns - 1) // columns  # Ceiling division

        grid = Table.grid(expand=True)

        # Add the columns
        for _ in range(columns):
            grid.add_column(ratio=1)

        # Add the rows
        for row_idx in range(rows):
            row_cells = []
            for col_idx in range(columns):
                item_idx = row_idx * columns + col_idx
                if item_idx < total_items:
                    # If this is the highlighted item, use yellow border
                    border_style = "bright_yellow" if item_idx == highlight_idx else "bright_blue"
                    row_cells.append(self._get_item_panel(self.items[item_idx], border_style))

            grid.add_row(*row_cells)

        return grid

    def cycle_highlight(self, min_width: int) -> None:
        """Continuously cycle through highlighting each item in the grid."""
        if not self.items:
            log.warning("No items to highlight")
            return

        self.running = True
        log.info("Starting highlight cycle animation")

        with Live(self._display_grid_with_highlight(min_width), refresh_per_second=4) as live:
            current_idx = 0
            total_items = len(self.items)

            while self.running:
                # Update the display with current highlighted item
                live.update(self._display_grid_with_highlight(min_width, current_idx))

                # Log which item is currently highlighted
                item_name = getattr(self.items[current_idx], "full_name", str(self.items[current_idx]))
                log.info(f"Highlighting {item_name}")

                time.sleep(1)

                # Move to next item
                current_idx = (current_idx + 1) % total_items

    def stop_cycle(self) -> None:
        """Stop the highlighting cycle."""
        self.running = False
        log.info("Stopping highlight cycle animation")

    def log_info(self, message: str) -> None:
        """Log an info message."""
        log.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        log.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        log.error(message)


def generate_random_people(count: int = 12) -> List[Person]:
    """Generate a list of random people with addresses for demonstration purposes."""
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                  "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                  "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Lisa", "Matthew", "Nancy"]

    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
                 "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee"]

    occupations = ["Engineer", "Doctor", "Teacher", "Designer", "Developer", "Scientist", "Writer",
                  "Artist", "Lawyer", "Accountant", "Manager", "Chef", "Nurse", "Architect", "Analyst",
                  "Consultant", "Researcher", "Therapist", "Technician", "Specialist"]

    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "example.com", "company.com"]

    streets = ["Main St", "Oak Ave", "Maple Rd", "Washington Blvd", "Park Lane", "Broadway",
              "First Ave", "Second St", "Highland Dr", "Lake View Rd", "Forest Ave", "Cedar St"]

    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
             "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Boston"]

    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "GA", "NC", "WA", "CO"]

    address_types = ["Home", "Work", "Other", "Vacation", "Business"]

    people = []
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        year = random.randint(1960, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Simplified to avoid date validation issues
        birth_date = date(year, month, day)

        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        occupation = random.choice(occupations)

        person = Person(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            email=email,
            phone=phone,
            occupation=occupation
        )

        # Add 1-3 addresses
        num_addresses = random.randint(1, 3)
        for _ in range(num_addresses):
            addr_type = random.choice(address_types)
            street_num = random.randint(1, 9999)
            street = f"{street_num} {random.choice(streets)}"
            city = random.choice(cities)
            state = random.choice(states)
            zip_code = f"{random.randint(10000, 99999)}"

            address = Address(
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                country="USA",
                address_type=addr_type
            )
            person.add_address(address)

        people.append(person)

    return people


def main():
    grid_logger = RichGridLogger()

    # Generate random people with addresses
    people = generate_random_people(6)

    # Add them to the grid using the new generalized method
    grid_logger.add_items(people)
    grid_logger.log_info("Starting demo of rich logging with grid layout")

    try:
        # Start cycling through the items with highlighting
        grid_logger.cycle_highlight(min_width=80)
    except KeyboardInterrupt:
        # Handle graceful exit when user presses Ctrl+C
        grid_logger.stop_cycle()
        grid_logger.log_info("Demo stopped by user")
    finally:
        grid_logger.log_info("Demo completed")


if __name__ == "__main__":
    main()
