"""コマンドライン実行用のモジュール"""

import fire
from .tagged_directory import TaggedDirectory


def main():
    """コマンド定義"""

    fire.Fire(
        {
            "set": set,
            "remove": remove,
            "remove_all": remove_all,
            "autoremove": autoremove,
            "tags": tags,
            "list": list_,
            "existing_list": existing_list,
            "nonexisting_list": nonexisting_list,
            "unregistered_list": unregistered_list,
            "counts": counts,
            "filter": filter_,
            "filter_and": filter_and,
            "filter_re": filter_re,
            "filter_partial": filter_partial,
            "reset": reset,
        }
    )


def set(filename: str, *tags: str):
    """ファイルに対してタグを設定
    
    Args:
        filename (str): ファイル名。未登録のものも指定可
        tags (str): タグのリスト。設定済みのものも指定可

    """

    tagged_directory = TaggedDirectory("./")
    tagged_directory.set_tags(filename, list(tags))
    tagged_directory.save_json()


def remove(filename: str, *tags: str):
    """ファイルからタグを解除
    
    Args:
        filename (str): ファイル名
        tags (str): タグのリスト

    """

    tagged_directory = TaggedDirectory("./")
    tagged_directory.remove_tags(filename, list(tags))
    tagged_directory.save_json()


def remove_all(filename: str):
    """ファイルからすべてのタグを解除
    
    Args:
        filename (str): ファイル名

    """

    tagged_directory = TaggedDirectory("./")
    tagged_directory.remove_all_tags(filename)
    tagged_directory.save_json()


def autoremove():
    """タグが付けられているが実在しないファイルを削除"""

    tagged_directory = TaggedDirectory("./")
    tagged_directory.autoremove()
    tagged_directory.save_json()


def tags(filename: str):
    """ファイルに設定されているタグのリストを表示

    Args:
        filename (str): ファイル名
    
    """

    tagged_directory = TaggedDirectory("./")
    for tag in tagged_directory.get_tag_list(filename):
        print(tag)


def list_():
    """タグがつけられているファイルのリストを表示"""

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.get_file_list():
        print(filename)


def existing_list():
    """タグ付け可能な実在するファイルのリストを表示"""

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.get_existing_file_list():
        print(filename)


def nonexisting_list():
    """タグが付けられているが実在しないファイルのリストを表示"""

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.get_nonexisting_file_list():
        print(filename)


def unregistered_list():
    """タグがつけられていないファイルのリストを表示"""

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.get_unregistered_file_list():
        print(filename)


def counts(search_word: str = ""):
    """タグ数の集計を表示
    
    Args:
        search_word (str, optional): 検索ワード

    """

    tagged_directory = TaggedDirectory("./")
    for tag, num in tagged_directory.count_tags(search_word).items():
        print(f"{tag}: {num}")


def filter_(*tags: str):
    """ファイルを絞り込む。指定されたタグのいずれかを含むファイルを対象とする（ORモード）
    
    Args:
        tags (str): タグのリスト
    
    """

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_tags(list(tags)):
        print(filename)


def filter_and(*tags: str):
    """ファイルを絞り込む。指定されたタグをすべて含むファイルを対象とする（ANDモード）
    
    Args:
        tags (str): タグのリスト
    
    """
    
    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_tags(list(tags), mode="and"):
        print(filename)


def filter_re(pattern: str):
    """正規表現によりファイルを絞り込む

    Args:
        pattern (str): 正規表現
    
    """

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_regular_expression(pattern):
        print(filename)


def filter_partial(*tags: str):
    """ファイルを絞り込む。指定されたタグのいずれかが部分一致するファイルを対象とする

    Args:
        tags (str): タグのリスト
    
    """

    tagged_directory = TaggedDirectory("./")
    for filename in tagged_directory.filter_by_partial_tags(list(tags)):
        print(filename)


def reset():
    """ファイルの配置をリセットする"""

    tagged_directory = TaggedDirectory("./")
    tagged_directory.reset_directory_structure()


if __name__ == "__main__":
    main()
