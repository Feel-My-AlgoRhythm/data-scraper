import argparse

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--debug", "-d",
        default=False,
        action="store_true",
        help="Run in debug mode.",
    )
    arg_parser.add_argument(
        "--task", "-t",
        type=str,
        required=True,
        choices=["datalab", "naverplace", "review"],
        help="Task for scraping information.",
    )

    args = arg_parser.parse_args()
    if args.task == "review":
        from src.poi import POIParser
        parser = POIParser()
        result = parser.load_reviews()
