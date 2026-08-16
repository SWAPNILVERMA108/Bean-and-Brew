from django.db import migrations


def rename_legacy_coffee_table(apps, schema_editor):
    """Repair databases created before CoffeeVariety was renamed correctly."""
    old_table = "coffee_coffeevarity"
    new_table = "coffee_coffeevariety"
    tables = set(schema_editor.connection.introspection.table_names())

    if old_table in tables and new_table not in tables:
        schema_editor.execute(
            f"ALTER TABLE {schema_editor.quote_name(old_table)} "
            f"RENAME TO {schema_editor.quote_name(new_table)}"
        )


def restore_legacy_coffee_table(apps, schema_editor):
    old_table = "coffee_coffeevarity"
    new_table = "coffee_coffeevariety"
    tables = set(schema_editor.connection.introspection.table_names())

    if new_table in tables and old_table not in tables:
        schema_editor.execute(
            f"ALTER TABLE {schema_editor.quote_name(new_table)} "
            f"RENAME TO {schema_editor.quote_name(old_table)}"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("coffee", "0003_coffeecertificate_coffeereview_store"),
    ]

    operations = [
        migrations.RunPython(rename_legacy_coffee_table, restore_legacy_coffee_table),
    ]
