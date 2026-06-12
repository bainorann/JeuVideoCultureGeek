import sys
import importlib


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <test_name>")
        print("       python run_tests.py list")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "list":
        print("Available tests:")
        for i in range(1, 9):
            print(f"  test{i}")
        return

    module_name = f"tests.{arg}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Unknown test: {arg}")
        print("Run 'python run_tests.py list' to see available tests.")
        sys.exit(1)

    module.run()


if __name__ == "__main__":
    main()
