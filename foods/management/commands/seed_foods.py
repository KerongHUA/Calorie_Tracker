import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from foods.models import FoodCatalogue


class Command(BaseCommand):
    help = "Seed FoodCatalogue from foods/seed_foods.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="",
            help="Optional path to a JSON file containing seed foods.",
        )

    def handle(self, *args, **options):
        path = options["path"].strip()
        if path:
            data_path = Path(path)
        else:
            data_path = Path(__file__).resolve().parent.parent.parent / "seed_foods.json"

        if not data_path.exists():
            self.stderr.write(self.style.ERROR(f"Seed file not found: {data_path}"))
            return

        try:
            with data_path.open("r", encoding="utf-8") as handle:
                items = json.load(handle)
        except json.JSONDecodeError as exc:
            self.stderr.write(self.style.ERROR(f"Invalid JSON: {exc}"))
            return

        if not isinstance(items, list):
            self.stderr.write(self.style.ERROR("Seed JSON must be a list of foods."))
            return

        created = 0
        updated = 0
        with transaction.atomic():
            for item in items:
                if not isinstance(item, dict):
                    continue

                name = item.get("name")
                if not name:
                    continue

                defaults = {
                    "calories_per_100g": item.get("calories_per_100g"),
                    "protein_per_100g": item.get("protein_per_100g"),
                    "carbs_per_100g": item.get("carbs_per_100g"),
                    "fat_per_100g": item.get("fat_per_100g"),
                }

                obj, was_created = FoodCatalogue.objects.update_or_create(
                    name=name, defaults=defaults
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Created: {created}, Updated: {updated}."
            )
        )
