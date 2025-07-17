import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import print as rprint
from local_ai.model import MODELS
from local_ai.core import AutonomousLocalAIManager, ServiceStartError, ModelNotFoundError
    
from local_ai import __version__
from local_ai.download import download_model_from_hf

def print_banner():
    """Display a beautiful banner for the CLI"""
    console = Console()
    banner_text = """
 █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ ██████╗ ██╗   ██╗███████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗  ██║██╔═══██╗████╗ ████║██╔═══██╗██║   ██║██╔════╝
███████║██║   ██║   ██║   ██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║██║   ██║███████╗
██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║██║   ██║╚════██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝

██╗      ██████╗  ██████╗ █████╗ ██╗       █████╗ ██╗
██║     ██╔═══██╗██╔════╝██╔══██╗██║      ██╔══██╗██║
██║     ██║   ██║██║     ███████║██║      ███████║██║
██║     ██║   ██║██║     ██╔══██║██║      ██╔══██║██║
███████╗╚██████╔╝╚██████╗██║  ██║███████╗ ██║  ██║██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝╚═╝
        """
        
    panel = Panel(
        Text(banner_text, style="bold cyan", justify="center"),
        title=f"[bold green]AutonomousLocalAI CLI v{__version__}[/bold green]",
        subtitle="[italic]Local AI Model Management[/italic]",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(panel)

def print_success(message):
    """Print success message with styling"""
    rprint(f"[bold green]✅ {message}[/bold green]")

def print_error(message):
    """Print error message with styling"""
    rprint(f"[bold red]❌ {message}[/bold red]")

def print_info(message):
    """Print info message with styling"""
    rprint(f"[bold blue]ℹ️  {message}[/bold blue]")

def print_warning(message):
    """Print warning message with styling"""
    rprint(f"[bold yellow]⚠️  {message}[/bold yellow]")

def show_available_models():
    """Display available models in a beautiful table"""
    console = Console()
    table = Table(title="🤖 Available Preserved Models", border_style="cyan")
    table.add_column("Model Name", style="bold magenta", justify="left")
    table.add_column("Hash", style="dim", justify="left")
    
    for model_name, model_hash in MODELS.items():
        table.add_row(model_name, model_hash[:16] + "...")
        
    console.print(table)

class CustomHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter for better styling"""
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        default = super()._format_action_invocation(action)
        return f"[bold cyan]{default}[/bold cyan]"

def parse_args():
    """Parse command line arguments with beautiful help formatting"""
    parser = argparse.ArgumentParser(
        description="🚀 AutonomousLocalAI - Local AI Model Management Tool",
        formatter_class=CustomHelpFormatter,
        epilog="💡 For more information, visit: https://github.com/JamesAuto1234/autonomous-local-ai"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"Autonomous Local AI v{__version__} 🥳"
    )
    
    subparsers = parser.add_subparsers(
        dest='command', 
        help="🛠️  Available commands for managing AI models",
        metavar="COMMAND"
    )
    
    # Model command group
    model_command = subparsers.add_parser(
        "model", 
        help="🤖 Model management operations",
        description="Manage your decentralized AI models"
    )
    model_subparsers = model_command.add_subparsers(
        dest='model_command', 
        help="Model operations",
        metavar="OPERATION"
    )

    # Add a subparser for the "download" command
    download_parser = model_subparsers.add_parser(
        "download",
        help="Download a model from the Hugging Face Hub",
        description="Download a model from the Hugging Face Hub"
    )
    # it should be qwen3-4b, qwen3-7b, qwen3-14b, qwen3-32b, qwen3-7b-instruct, qwen3-14b-instruct, qwen3-32b-instruct
    download_parser.add_argument(
        "model_name",
        help="The name of the model to download",
        choices=MODELS.keys()
    )
    
    # Add a subparser for the "run" command
    run_parser = model_subparsers.add_parser(
        "run",
        help="Run AI models with multi-model support",
        description="Start the AutonomousLocalAI service with one or more models"
    )
    run_parser.add_argument(
        "models",
        help="Comma-separated list of model names (e.g., 'qwen3-4b,qwen3-1.7b')"
    )
    run_parser.add_argument(
        "--port",
        type=int,
        help="Port number for the service (default from config)"
    )
    run_parser.add_argument(
        "--host",
        help="Host address for the service (default from config)"
    )
    run_parser.add_argument(
        "--context-length",
        type=int,
        help="Context length for the model (default from config)"
    )
    
    return parser.parse_known_args()

def handle_download(args):
    """Handle model download with beautiful output"""
    print_info(f"Starting download for model: {args.model_name}")
    try:
        download_model_from_hf(args.model_name)
        print_success("Model downloaded successfully!")
    except Exception as e:
        print_error(f"Download failed: {str(e)}")
        sys.exit(1)

def handle_run(args):
    """Handle model run command with beautiful output"""
    print_info(f"Starting AutonomousLocalAI service with models: {args.models}")
    
    # Validate that model names exist in the MODELS dict
    model_list = [m.strip() for m in args.models.split(',') if m.strip()]
    validated_models = []
    
    for model in model_list:
        if model in MODELS:
            validated_models.append(model)
            print_info(f"Found model '{model}' in registry")
        else:
            print_error(f"Model '{model}' not found in registry")
            print_info("Available models: " + ", ".join(MODELS.keys()))
            sys.exit(1)
    
    models_str = ",".join(validated_models)
    
    try:
        manager = AutonomousLocalAIManager()
        success = manager.start(
            models=models_str,
            port=args.port,
            host=args.host,
            context_length=args.context_length
        )
        
        if success:
            print_success("AutonomousLocalAI service started successfully!")
            print_info("Service is now running and ready to accept requests")
        else:
            print_error("Failed to start AutonomousLocalAI service")
            sys.exit(1)
            
    except ValueError as e:
        print_error(f"Invalid input: {str(e)}")
        sys.exit(1)
    except ModelNotFoundError as e:
        print_error(f"Model not found: {str(e)}")
        sys.exit(1)
    except ServiceStartError as e:
        print_error(f"Service start error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

def main():
    """Main CLI entry point with enhanced error handling"""
    # Show banner
    print_banner()
    
    known_args, unknown_args = parse_args()
    
    # Handle unknown arguments
    if unknown_args:
        for arg in unknown_args:
            print_error(f'Unknown command or argument: {arg}')
        print_info("Use --help for available commands and options")
        sys.exit(2)

    # Handle commands
    if known_args.command == "model":
        if known_args.model_command == "download":
            handle_download(known_args)
        elif known_args.model_command == "run":
            handle_run(known_args)
        else:
            print_error(f"Unknown model command: {known_args.model_command}")
            print_info("Available model commands: run, download")
            sys.exit(2)
    else:
        print_error(f"Unknown command: {known_args.command}")
        print_info("Available commands: model")
        print_info("Use --help for more information")
        sys.exit(2)


if __name__ == "__main__":
    main()