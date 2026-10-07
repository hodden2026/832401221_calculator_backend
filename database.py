import os
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = (
    Path(__file__).resolve().parent
    / "calculator.db"
)


DATABASE_PATH = Path(
    os.environ.get(
        "DATABASE_PATH",
        str(DEFAULT_DATABASE_PATH),
    )
)


def get_connection():
    """创建 SQLite 数据库连接。"""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


def init_database():
    """初始化数据库。"""

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def add_history(
    expression,
    result,
):
    """保存一条计算历史。"""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO calculation_history (
                expression,
                result
            )
            VALUES (?, ?)
            """,
            (
                expression,
                str(result),
            ),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_history():
    """获取全部计算历史。"""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                expression,
                result,
                created_at
            FROM calculation_history
            ORDER BY id DESC
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def delete_history(
    history_id,
):
    """删除指定 ID 的计算历史。"""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM calculation_history
            WHERE id = ?
            """,
            (
                history_id,
            ),
        )

        connection.commit()

        return (
            cursor.rowcount > 0
        )

    finally:
        connection.close()


def clear_history():
    """清空全部计算历史。"""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM calculation_history
            """
        )

        deleted_count = (
            cursor.rowcount
        )

        connection.commit()

        return deleted_count

    finally:
        connection.close()