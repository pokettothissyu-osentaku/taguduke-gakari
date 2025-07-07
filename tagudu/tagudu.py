"""コマンドライン実行用のモジュール"""

import fire
from .tagged_directory import TaggedDirectory


def main():
    fire.Fire(
        {
            "set": set,
            "remove": remove,
            "tags": tags,
            "counts": counts,
            "filter": filter_,
            "filter_and": filter_and,
            "filter_re": filter_re,
            "reset": reset,
        }
    )


def set(filename, *tags):
    tagged_directory = TaggedDirectory("./")
    tagged_directory.set_tags(filename, list(tags))
    tagged_directory.save_json()


def remove(filename, *tags):
    tagged_directory = TaggedDirectory("./")
    tagged_directory.remove_tags(filename, list(tags))
    tagged_directory.save_json()


def tags(filename):
    tagged_directory = TaggedDirectory("./")
    for tag in tagged_directory.get_tag_list(filename):
        print(tag)


def counts():
    tagged_directory = TaggedDirectory("./")
    for tag, num in tagged_directory.count_tags().items():
        print(f"{tag}: {num}")


def filter_(*tags):
    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_tags(list(tags)):
        print(filename)


def filter_and(*tags):
    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_tags(list(tags), mode="and"):
        print(filename)


def filter_re(pattern):
    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_regular_expression(pattern):
        print(filename)


def reset():
    tagged_directory = TaggedDirectory("./")
    tagged_directory.reset_directory_structure()


if __name__ == "__main__":
    main()
