import fire
from .folder import Folder


def main():
    fire.Fire(
        {
            "test": test,
        }
    )


def test():
    folder = Folder()
    print(folder.test())


if __name__ == "__main__":
    main()
