from .game import run_interactive

def main() -> None:
    # Start interactive loop if pygame available, otherwise placeholder fallback inside
    run_interactive()

if __name__ == "__main__":
    main()
