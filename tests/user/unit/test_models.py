async def test_table_exists(inspect_list_tables: list[str]):
    assert "users" in inspect_list_tables
