from __future__ import annotations

from asyncpg import Connection
from packaging.version import parse

from pylav.constants.config import DEFAULT_PLAYER_VOLUME
from pylav.constants.versions import VERSION_1_15_7
from pylav.storage.migrations.logging import LOGGER


async def low_level_v_1_15_7_migration(con: Connection) -> None:
    """Run the low level migration for PyLav 1.10.6."""
    await low_level_v_1_15_7_queries(con)


async def low_level_v_1_15_7_queries(con: Connection) -> None:
    """Run the queries migration for PyLav 1.10.6."""
    await run_queries_migration_v_1_15_7(con)


async def run_queries_migration_v_1_15_7(con: Connection) -> None:
    """
    Add the info and pluginInfo columns to the query table.
    """
    has_column = """
        SELECT EXISTS (SELECT 1
        FROM information_schema.columns
        WHERE table_name='version' AND column_name='version')
        """
    has_version_column = await con.fetchval(has_column)
    if not has_version_column:
        return

    version = await con.fetchval("SELECT version from version;")
    if version is None:
        return

    version_parsed = parse(version)
    if version_parsed >= VERSION_1_15_7:
        return

    migrated = False
    has_column = """
        SELECT EXISTS (SELECT 1
        FROM information_schema.columns
        WHERE table_name='player_state' AND column_name='volume')
        """
    has_volume_column = await con.fetchval(has_column)
    if has_volume_column:
        alter_table = f"""
        ALTER TABLE player_state ALTER COLUMN volume SET DEFAULT {DEFAULT_PLAYER_VOLUME};
                """
        await con.execute(alter_table)
        migrated = True

    has_column = """
            SELECT EXISTS (SELECT 1
            FROM information_schema.columns
            WHERE table_name='player' AND column_name='volume')
            """
    has_column_response = await con.fetchval(has_column)
    if has_column_response:
        alter_table = f"""
        ALTER TABLE player ALTER COLUMN volume SET DEFAULT {DEFAULT_PLAYER_VOLUME};
        """
        await con.execute(alter_table)
        migrated = True

    if migrated:
        LOGGER.info("----------- Migrating table player to PyLav 1.15.7 ---------")
