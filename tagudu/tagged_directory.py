"""外部参照用のモジュール"""

from pathlib import Path
import json
import re
import os
import shutil


class TaggedDirectory(object):
    """ディレクトリ内のファイルに対してタグ管理するためのクラス

    Attributes:
        path (pathlib.Path): 対象ディレクトリのパス
        json_path (pathlib.Path): jsonファイルのパス
        result_path (pathlib.Path): フィルター結果フォルダのパス
        data (dict[str, list[str]]): タグのデータ。キーがファイル名で、値がタグのリスト

    """

    def __init__(
        self,
        path: str | Path,
        *,
        json_filename: str = "tagudu.json",
        result_directory_name: str = "tagudu_result",
    ):
        """
        Args:
            path (str | pathlib.Path): 対象ディレクトリのパス
            json_filename (str, optional): タグのデータを格納するjsonファイルの名前
            result_directory_name (str, optional): フィルター結果フォルダの名前

        """

        self.path = Path(path)
        self.json_path = self.path / json_filename
        self.result_path = self.path / result_directory_name

        # 対象ディレクトリが存在しない場合、例外を送出
        if not self.path.is_dir():
            raise FileNotFoundError("存在しないディレクトリです")

        # jsonファイルを読み込み
        if self.json_path.is_file():
            with open(self.json_path, encoding="utf-8") as file:
                self.data = json.load(file)
        # jsonファイルが無い場合
        else:
            self.data = {}

    # データ操作関係

    def set_tags(self, filename: str, tags: list[str]):
        """ファイルに対してタグを設定

        Args:
            filename (str): ファイル名。未登録のものも指定可
            tags (list[str]): タグのリスト。設定済みのものも指定可

        """

        # tagsが空のリストの場合は何もしない
        if len(tags) == 0:
            return

        # 未登録のファイル名の場合
        if filename not in self.data:
            self.data[filename] = []

        # タグを設定
        file_tags = self.data[filename]
        new_tags = list(set(tags) - set(file_tags))
        file_tags += new_tags

    def remove_tags(self, filename: str, tags: list[str]):
        """ファイルからタグを解除

        Args:
            filename (str): ファイル名
            tags (list[str]): タグのリスト

        """

        # 指定ファイル名がデータに登録されていない場合は何もしない
        if filename not in self.data:
            return

        file_tags = self.data[filename]

        # タグを解除
        for tag in tags:
            if tag in file_tags:
                file_tags.remove(tag)

        # タグのリストが空になった場合、項目を削除
        if len(file_tags) == 0:
            del self.data[filename]

    def remove_all_tags(self, filename: str):
        """ファイルからすべてのタグを解除

        Args:
            filename (str): ファイル名

        """

        if filename in self.data:
            del self.data[filename]

    def autoremove(self):
        """タグが付けられているが実在しないファイルを削除"""

        nonexisting_file_list = self.get_nonexisting_file_list()

        for filename in nonexisting_file_list:
            self.remove_all_tags(filename)

    def save_json(self):
        """jsonファイルにデータを書き込む"""

        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    # データ取得関係

    def get_tag_list(self, filename: str) -> list[str]:
        """ファイルに設定されているタグのリストを取得

        Args:
            filename (str): ファイル名

        Returns:
            list[str]: タグのリスト

        """

        if filename in self.data:
            return self.data[filename]
        else:
            return []

    def get_file_list(self) -> list[str]:
        """タグがつけられているファイルのリストを取得

        Returns:
            list[str]: ファイルのリスト

        """

        return list(self.data.keys())

    def get_existing_file_list(self) -> list[str]:
        """タグ付け可能な実在するファイルのリストを取得

        Returns:
            list[str]: ファイルのリスト

        """

        file_list = [
            filename
            for filename in os.listdir(self.path)
            if (self.path / filename).is_file()
        ]

        if self.result_path.is_dir():
            file_list += [
                filename
                for filename in os.listdir(self.result_path)
                if (self.result_path / filename).is_file()
            ]

        return file_list

    def get_nonexisting_file_list(self) -> list[str]:
        """タグが付けられているが実在しないファイルのリストを取得

        Returns:
            list[str]: ファイルのリスト

        """

        file_list = self.get_file_list()
        existing_file_list = self.get_existing_file_list()

        return list(set(file_list) - set(existing_file_list))

    def get_unregistered_file_list(self) -> list[str]:
        """タグがつけられていないファイルのリストを取得

        Returns:
            list[str]: ファイルのリスト

        """

        file_list = self.get_file_list()
        existing_file_list = self.get_existing_file_list()

        return list(set(existing_file_list) - set(file_list))

    def count_tags(self, search_word: str = "") -> dict[str, int]:
        """タグ数を集計

        Args:
            search_word (str, optional): 検索ワード

        Returns:
            dict[str, int]: 集計結果

        """

        result = {}

        # 集計
        for tag_list in self.data.values():
            for tag in tag_list:
                if tag not in result:
                    result[tag] = 0
                result[tag] += 1

        sorted_result = {}

        # ソート
        for tag in sorted(result, key=lambda tag: result[tag], reverse=True):
            sorted_result[tag] = result[tag]

        search_result = {}

        # 検索
        for tag in filter(lambda tag: search_word in tag, sorted_result):
            search_result[tag] = sorted_result[tag]

        return search_result

    # フィルター関係

    def filter_by_tags(
        self, tags: list[str], *, mode: str = "or", file_operation: bool = True
    ) -> list[str]:
        """完全一致のタグによりファイルを絞り込み

        Args:
            tags (list[str]): タグのリスト
            mode (str, optional): 絞り込みモード。「or」か「and」。初期値は「or」
            file_operation (bool): 絞り込み結果を結果ディレクトリに反映させるか。初期値は「True」

        Returns:
            list[str]: 絞り込み結果

        """

        # モードの確認
        if mode not in ("or", "and"):
            raise ValueError("モードは「or」か「and」でなければなりません")

        def func(filename):
            file_tags = self.data[filename]
            count = 0
            for tag in tags:
                if tag in file_tags:
                    count += 1
            if mode == "or":
                return count >= 1
            if mode == "and":
                return count == len(tags)

        result = list(filter(func, self.data))

        # ファイル操作
        if file_operation:
            self.reset_directory_structure()
            self._apply_filter_result(result)

        return result

    def filter_by_regular_expression(
        self, pattern: str, *, file_operation: bool = True
    ) -> list[str]:
        """正規表現によりファイルを絞り込み

        Args:
            pattern (str): 正規表現
            file_operation (bool): 絞り込み結果を結果ディレクトリに反映させるか。初期値は「True」

        Returns:
            list[str]: 絞り込み結果

        """

        compiled_pattern = re.compile(pattern)

        def func(filename):
            file_tags = self.data[filename]
            for file_tag in file_tags:
                if compiled_pattern.match(file_tag):
                    return True
            return False

        result = list(filter(func, self.data))

        # ファイル操作
        if file_operation:
            self.reset_directory_structure()
            self._apply_filter_result(result)

        return result

    def filter_by_partial_tags(
        self, tags: list[str], *, file_operation: bool = True
    ) -> list[str]:
        """部分一致のタグによりファイルを絞り込み

        Args:
            tags (list[str]): タグのリスト
            file_operation (bool): 絞り込み結果を結果ディレクトリに反映させるか。初期値は「True」

        Returns:
            list[str]: 絞り込み結果

        """

        def func(filename):
            file_tags = self.data[filename]
            for file_tag in file_tags:
                for tag in tags:
                    if tag in file_tag:
                        return True
            return False

        result = list(filter(func, self.data))

        # ファイル操作
        if file_operation:
            self.reset_directory_structure()
            self._apply_filter_result(result)

        return result

    def reset_directory_structure(self):
        """ディレクトリ内のファイルの配置をリセットする"""

        # フィルター結果フォルダが無い場合は何もしない
        if not self.result_path.is_dir():
            return

        items = os.listdir(self.result_path)

        # 結果フォルダ内のファイルのみを外に移動、
        for item in items:
            item_path = self.result_path / item
            if item_path.is_file():
                shutil.move(item_path, self.path)

        # 結果フォルダ内が空であれば結果フォルダを削除
        try:
            os.rmdir(self.result_path)
        except OSError:
            pass

    def _apply_filter_result(self, files: list[str]):
        """指定されたファイルをフィルター結果ディレクトリに移動する

        Args:
            files (list[str]): ファイル名のリスト

        """

        os.makedirs(self.result_path, exist_ok=True)

        for filename in files:
            file_path = self.path / filename
            if file_path.is_file():
                shutil.move(file_path, self.result_path)
