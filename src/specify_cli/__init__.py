#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Spec Ops CLI - Setup tool for Spec Ops projects

Usage:
    uvx --from git+https://github.com/rHedBull/spec-ops.git specops init <project-name>
    uvx --from git+https://github.com/rHedBull/spec-ops.git specops init --here

Or install globally:
    uv tool install --from git+https://github.com/rHedBull/spec-ops.git spec-ops-cli
    specops init <project-name>
    specops init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import json
from pathlib import Path
from typing import Optional

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar

# Constants
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI"
}

# ASCII Art Banner
BANNER = """
███████╗██████╗ ███████╗ ██████╗     ██████╗ ██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔═══██╗██╔══██╗██╔════╝
███████╗██████╔╝█████╗  ██║         ██║   ██║██████╔╝███████╗
╚════██║██╔═══╝ ██╔══╝  ██║         ██║   ██║██╔═══╝ ╚════██║
███████║██║     ███████╗╚██████╗    ╚██████╔╝██║     ███████║
╚══════╝╚═╝     ╚══════╝ ╚═════╝     ╚═════╝ ╚═╝     ╚══════╝
"""

TAGLINE = "Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[bold cyan]{self.title}[/bold cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩ 
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()
    
    # Arrow keys
    if key == readchar.key.UP:
        return 'up'
    if key == readchar.key.DOWN:
        return 'down'
    
    # Enter/Return
    if key == readchar.key.ENTER:
        return 'enter'
    
    # Escape
    if key == readchar.key.ESC:
        return 'escape'
        
    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0
    
    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="bright_cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")
        
        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[bright_cyan]{key}: {options[key]}[/bright_cyan]")
            else:
                table.add_row(" ", f"[white]{key}: {options[key]}[/white]")
        
        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")
        
        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
    
    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)
                    
                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specops",
    help="Setup tool for Spec Ops spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors - orange to black
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_red", "red", "bright_yellow", "yellow", "bright_black", "black"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'specops --help' for usage information[/dim]"))
        console.print()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    if shutil.which(tool):
        return True
    else:
        console.print(f"[yellow]⚠️  {tool} not found[/yellow]")
        console.print(f"   Install with: [cyan]{install_hint}[/cyan]")
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Spec Ops template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True
        
    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def copy_local_templates(source_dir: Path, project_path: Path, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None):
    """Copy templates from local directory to project directory."""
    
    # Define which directories and files to copy
    items_to_copy = ["templates", "scripts", "memory"]
    
    if tracker:
        tracker.start("extract")
    
    try:
        if verbose and not tracker:
            console.print(f"[dim]Template source directory: {source_dir}[/dim]")
            console.print(f"[dim]Items to copy: {items_to_copy}[/dim]")
        
        for item_name in items_to_copy:
            source_item = source_dir / item_name
            if verbose and not tracker:
                console.print(f"[dim]Checking {source_item} - exists: {source_item.exists()}[/dim]")
            
            if source_item.exists():
                dest_item = project_path / item_name
                
                if verbose and not tracker:
                    if source_item.is_dir():
                        sub_items = list(source_item.rglob('*'))
                        console.print(f"[cyan]Copying directory {item_name} with {len(sub_items)} items[/cyan]")
                        # Show subdirectories specifically
                        subdirs = [item for item in source_item.iterdir() if item.is_dir()]
                        if subdirs:
                            console.print(f"[dim]  Subdirectories: {[d.name for d in subdirs]}[/dim]")
                    else:
                        console.print(f"[cyan]Copying file {item_name}[/cyan]")
                
                if source_item.is_dir():
                    if dest_item.exists():
                        if verbose and not tracker:
                            console.print(f"[yellow]Merging directory:[/yellow] {item_name}")
                        # Use shutil.copytree with dirs_exist_ok=True for proper merging
                        shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
                    else:
                        shutil.copytree(source_item, dest_item)
                else:
                    if dest_item.exists() and verbose and not tracker:
                        console.print(f"[yellow]Overwriting file:[/yellow] {item_name}")
                    shutil.copy2(source_item, dest_item)
                    
                if verbose and not tracker:
                    console.print(f"[green]✓[/green] Copied {item_name}")
                    # Show what was copied for directories
                    if source_item.is_dir():
                        sub_items = list(source_item.rglob('*'))
                        console.print(f"    [dim]Contains {len(sub_items)} items[/dim]")
        
        if tracker:
            tracker.complete("extract", f"copied {len(items_to_copy)} template directories")
        elif verbose:
            console.print("[green]✓[/green] Local templates copied successfully")
            
    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error copying local templates:[/red] {e}")
        raise


def download_and_extract_template(project_path: Path, ai_assistant: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    # Find the spec-ops repository root - try multiple locations in order of preference
    current_dir = Path.cwd()
    file_dir = Path(__file__).parent.parent.parent.resolve()
    package_dir = Path(__file__).parent
    
    # Check locations in order of preference:
    # 1. Current working directory (development mode)
    # 2. Package directory (bundled templates from pyproject.toml)
    # 3. File directory (fallback for other installations)
    locations_to_check = [
        (current_dir, "current working directory", lambda: (current_dir / "templates").exists() and (current_dir / "pyproject.toml").exists()),
        (package_dir, "package resources", lambda: (package_dir / "templates").exists()),
        (file_dir, "package directory", lambda: (file_dir / "templates").exists()),
    ]
    
    local_templates_dir = None
    location_description = None
    
    for location, description, check_func in locations_to_check:
        if check_func():
            local_templates_dir = location
            location_description = description
            break
    
    if local_templates_dir is None:
        # Fallback: Download from GitHub
        if verbose and not tracker:
            console.print("[yellow]Local templates not found, downloading from GitHub...[/yellow]")
        if tracker:
            tracker.start("fetch", "downloading from GitHub")
        
        return download_from_github(project_path, ai_assistant, is_current_dir, verbose=verbose, tracker=tracker)
    
    if verbose and not tracker:
        console.print(f"[dim]Using templates from {location_description}[/dim]")
    
    if tracker:
        tracker.start("fetch", "using local templates")
        tracker.complete("fetch", f"local directory: {local_templates_dir}")
        tracker.add("extract", "Copy local templates")
    elif verbose:
        console.print(f"[cyan]Using local templates from:[/cyan] {local_templates_dir}")
        console.print(f"[cyan]Copying to project directory:[/cyan] {project_path}")
    
    # Copy templates directly from local directory
    copy_local_templates(local_templates_dir, project_path, is_current_dir, verbose=verbose, tracker=tracker)
    return project_path


def download_from_github(project_path: Path, ai_assistant: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    """Download templates from GitHub when not found locally."""
    github_repo = "rHedBull/spec-ops"
    
    if tracker:
        tracker.start("download", "fetching release info")
    elif verbose:
        console.print("[cyan]Fetching latest release from GitHub...[/cyan]")
    
    try:
        # Get the latest release
        response = httpx.get(f"https://api.github.com/repos/{github_repo}/releases/latest", timeout=10, follow_redirects=True)
        response.raise_for_status()
        release_data = response.json()
        
        # Download the source code archive
        archive_url = release_data["zipball_url"]
        if tracker:
            tracker.complete("download", "downloading archive")
        elif verbose:
            console.print(f"[cyan]Downloading archive from:[/cyan] {archive_url}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            zip_path = temp_path / "source.zip"
            
            # Download the zip file
            with httpx.stream("GET", archive_url, timeout=60, follow_redirects=True) as response:
                response.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
            
            # Extract the zip file
            extract_path = temp_path / "extracted"
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Find the extracted directory (GitHub creates a directory with repo name and commit hash)
            extracted_dirs = [d for d in extract_path.iterdir() if d.is_dir()]
            if not extracted_dirs:
                raise FileNotFoundError("No directories found in downloaded archive")
            
            source_dir = extracted_dirs[0]  # Should be the only directory
            
            if tracker:
                tracker.complete("download", "archive extracted")
                tracker.add("extract", "Copy templates from archive")
            
            # Copy templates from the extracted source
            copy_local_templates(source_dir, project_path, is_current_dir, verbose=verbose, tracker=tracker)
    
    except httpx.RequestError as e:
        error_msg = f"Failed to download from GitHub: {e}"
        if tracker:
            tracker.error("download", error_msg)
        else:
            console.print(f"[red]Error:[/red] {error_msg}")
        raise
    except Exception as e:
        error_msg = f"Failed to extract templates: {e}"
        if tracker:
            tracker.error("extract", error_msg)
        else:
            console.print(f"[red]Error:[/red] {error_msg}")
        raise
    
    return project_path
@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, or copilot"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
):
    """
    Initialize a new Spec Ops project from the latest template.
    
    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, or GitHub Copilot)
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands
    
    Examples:
        specops init my-project
        specops init my-project --ai claude
        specops init my-project --ai gemini
        specops init my-project --ai copilot --no-git
        specops init --ignore-agent-tools my-project
        specops init --here --ai claude
        specops init --here
    """
    # Show banner first
    show_banner()
    
    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name or use --here flag")
        raise typer.Exit(1)
    
    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
        
        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            
            # Ask for confirmation
            response = typer.confirm("Do you want to continue?")
            if not response:
                console.print("[yellow]Operation cancelled[/yellow]")
                raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            console.print(f"[red]Error:[/red] Directory '{project_name}' already exists")
            raise typer.Exit(1)
    
    console.print(Panel.fit(
        "[bold cyan]Spec Ops Project Setup[/bold cyan]\n"
        f"{'Initializing in current directory:' if here else 'Creating new project:'} [green]{project_path.name}[/green]"
        + (f"\n[dim]Path: {project_path}[/dim]" if here else ""),
        border_style="cyan"
    ))
    
    # Check git only if we might need it (not --no-git)
    git_available = True
    if not no_git:
        git_available = check_tool("git", "https://git-scm.com/downloads")
        if not git_available:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            AI_CHOICES, 
            "Choose your AI assistant:", 
            "copilot"
        )
    
    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        if selected_ai == "claude":
            if not check_tool("claude", "Install from: https://docs.anthropic.com/en/docs/claude-code/setup"):
                console.print("[red]Error:[/red] Claude CLI is required for Claude Code projects")
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "Install from: https://github.com/google-gemini/gemini-cli"):
                console.print("[red]Error:[/red] Gemini CLI is required for Gemini projects")
                agent_tool_missing = True
        # GitHub Copilot check is not needed as it's typically available in supported IDEs
        
        if agent_tool_missing:
            console.print("\n[red]Required AI tool is missing![/red]")
            console.print("[yellow]Tip:[/yellow] Use --ignore-agent-tools to skip this check")
            raise typer.Exit(1)
    
    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Spec Ops Project")
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            download_and_extract_template(project_path, selected_ai, here, verbose=False, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif git_available:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(f"\n[red]Error:[/red] {str(e)}")
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")
    
    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. [bold green]cd {project_name}[/bold green]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    if selected_ai == "claude":
        steps_lines.append(f"{step_num}. Open in Visual Studio Code and start using / commands with Claude Code")
        steps_lines.append("   - Type / in any file to see available commands")
        steps_lines.append("   - Use /specify to create specifications")
        steps_lines.append("   - Use /plan to create implementation plans")
        steps_lines.append("   - Use /tasks to generate tasks")
    elif selected_ai == "gemini":
        steps_lines.append(f"{step_num}. Use / commands with Gemini CLI")
        steps_lines.append("   - Run gemini /specify to create specifications")
        steps_lines.append("   - Run gemini /plan to create implementation plans")
        steps_lines.append("   - See GEMINI.md for all available commands")
    elif selected_ai == "copilot":
        steps_lines.append(f"{step_num}. Open in Visual Studio Code and use [bold cyan]/specify[/], [bold cyan]/plan[/], [bold cyan]/tasks[/] commands with GitHub Copilot")

    step_num += 1
    steps_lines.append(f"{step_num}. Update [bold magenta]CONSTITUTION.md[/bold magenta] with your project's non-negotiable principles")

    steps_panel = Panel("\n".join(steps_lines), title="Next steps", border_style="cyan", padding=(1,2))
    console.print()  # blank line
    console.print(steps_panel)
    
    # Removed farewell line per user request


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking Spec Ops requirements...[/bold]\n")
    
    # Check if we have internet connectivity by trying to reach GitHub API
    console.print("[cyan]Checking internet connectivity...[/cyan]")
    try:
        response = httpx.get("https://api.github.com", timeout=5, follow_redirects=True)
        console.print("[green]✓[/green] Internet connection available")
    except httpx.RequestError:
        console.print("[red]✗[/red] No internet connection - required for downloading templates")
        console.print("[yellow]Please check your internet connection[/yellow]")
    
    console.print("\n[cyan]Optional tools:[/cyan]")
    git_ok = check_tool("git", "https://git-scm.com/downloads")
    
    console.print("\n[cyan]Optional AI tools:[/cyan]")
    claude_ok = check_tool("claude", "Install from: https://docs.anthropic.com/en/docs/claude-code/setup")
    gemini_ok = check_tool("gemini", "Install from: https://github.com/google-gemini/gemini-cli")
    
    console.print("\n[green]✓ Spec Ops CLI is ready to use![/green]")
    if not git_ok:
        console.print("[yellow]Consider installing git for repository management[/yellow]")
    if not (claude_ok or gemini_ok):
        console.print("[yellow]Consider installing an AI assistant for the best experience[/yellow]")


def main():
    app()


if __name__ == "__main__":
    main()
