# HOBBY DEPOT – KATEGORIE-RUNTIME-API

Plugin:
`HD-004-KATEGORIE-KERN`

Vertrag:
`HOBBY_DEPOT_CATEGORY_REGISTRY_RUNTIME_V1`

## Read-only API für andere Plugins

```php
hd_category_registry_ready();
hd_category_registry_revision();
hd_category_registry_snapshot();
hd_category_registry_node($node_id);
hd_category_registry_children($parent_node_id, $pillar = null);
hd_category_registry_mapping($node_id);
hd_category_registry_resolve($node_id);
hd_category_registry_find_node_by_object($object_id, $object_type = '');
hd_category_registry_taxonomies();
hd_category_registry_stats();
```

## Harte Regel

Andere Hobby-Depot-Plugins sollen für Kategorien/Taxonomien/Parent-Zuordnung diesen neutralen Vertrag verwenden.

Sie sollen NICHT:
- DataForSEO als Strukturquelle verwenden;
- eigene Kategorie-Master führen;
- direkt von Admin-/Sync-Klassen des schweren HD-001 abhängen;
- zweite Taxonomien für dieselben Inhalte anlegen.

## Schreibzugriff

HD-004 ist absichtlich **read-only**.

Add / Rename / Move / Merge / Archive erfolgen weiterhin kontrolliert über HD-001 und dessen Delta-/Dry-Run-/Sync-/Readback-Prozess.

Nach erfolgreichem Sync liest HD-004 automatisch den neuen aktiven Snapshot.
