"""Дневник воды — Flet + Supabase (CRUD: добавить, показать, изменить, удалить)."""
import os
from datetime import date

import flet as ft
from supabase import create_client

try:
    from config import SUPABASE_URL, SUPABASE_KEY  # создаётся в Actions / локально
except ImportError:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

TABLE = "water_log"
GOAL_ML = 2000  # дневная норма для прогресс-бара


def main(page: ft.Page):
    page.title = "Дневник воды"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    total_text = ft.Text(size=28, weight=ft.FontWeight.BOLD)
    progress = ft.ProgressBar(value=0, height=12)
    records = ft.Column(spacing=4)
    custom_amount = ft.TextField(
        label="Свой объём, мл", keyboard_type=ft.KeyboardType.NUMBER, expand=True
    )

    def notify(text: str):
        page.open(ft.SnackBar(ft.Text(text)))

    # --- подключение к Supabase ---
    if not SUPABASE_URL or not SUPABASE_KEY:
        page.add(ft.Text("Не заданы SUPABASE_URL / SUPABASE_KEY", color=ft.Colors.RED))
        return
    db = create_client(SUPABASE_URL, SUPABASE_KEY)

    # --- READ ---
    def load():
        try:
            rows = (
                db.table(TABLE)
                .select("*")
                .eq("date", date.today().isoformat())
                .order("created_at", desc=True)
                .execute()
                .data
            )
        except Exception as ex:
            notify(f"Ошибка чтения: {ex}")
            return
        total = sum(r["amount"] for r in rows)
        total_text.value = f"{total} мл из {GOAL_ML}"
        progress.value = min(total / GOAL_ML, 1)
        records.controls = [row_view(r) for r in rows]
        page.update()

    # --- CREATE ---
    def add(amount: int):
        try:
            db.table(TABLE).insert(
                {"amount": amount, "date": date.today().isoformat()}
            ).execute()
        except Exception as ex:
            notify(f"Ошибка записи: {ex}")
            return
        load()

    def add_custom(e):
        try:
            value = int(custom_amount.value)
            if not 0 < value <= 5000:
                raise ValueError
        except (TypeError, ValueError):
            notify("Введите число от 1 до 5000")
            return
        custom_amount.value = ""
        add(value)

    # --- DELETE ---
    def delete(row_id: int):
        try:
            db.table(TABLE).delete().eq("id", row_id).execute()
        except Exception as ex:
            notify(f"Ошибка удаления: {ex}")
            return
        load()

    # --- UPDATE ---
    def edit(row: dict):
        field = ft.TextField(
            value=str(row["amount"]), keyboard_type=ft.KeyboardType.NUMBER
        )

        def save(e):
            try:
                value = int(field.value)
                if not 0 < value <= 5000:
                    raise ValueError
                db.table(TABLE).update({"amount": value}).eq("id", row["id"]).execute()
            except ValueError:
                notify("Введите число от 1 до 5000")
                return
            except Exception as ex:
                notify(f"Ошибка обновления: {ex}")
                return
            page.close(dialog)
            load()

        dialog = ft.AlertDialog(
            title=ft.Text("Изменить объём, мл"),
            content=field,
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(dialog)),
                ft.TextButton("Сохранить", on_click=save),
            ],
        )
        page.open(dialog)

    def row_view(row: dict) -> ft.Control:
        return ft.ListTile(
            leading=ft.Icon(ft.Icons.WATER_DROP),
            title=ft.Text(f"{row['amount']} мл"),
            trailing=ft.Row(
                [
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, r=row: edit(r)),
                    ft.IconButton(
                        ft.Icons.DELETE, on_click=lambda e, r=row: delete(r["id"])
                    ),
                ],
                tight=True,
            ),
        )

    page.add(
        ft.Text("Сегодня выпито", size=16),
        total_text,
        progress,
        ft.Row(
            [
                ft.ElevatedButton("+ 250 мл", on_click=lambda e: add(250)),
                ft.ElevatedButton("+ 500 мл", on_click=lambda e: add(500)),
            ]
        ),
        ft.Row([custom_amount, ft.ElevatedButton("Добавить", on_click=add_custom)]),
        ft.Divider(),
        records,
    )
    load()


ft.app(target=main)
