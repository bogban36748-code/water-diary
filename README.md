# Дневник воды (Flet + Supabase)

Android-приложение: учёт выпитой воды за день. Клиент — Python/Flet, данные — Supabase (PostgreSQL) через supabase-py, APK собирается в GitHub Actions.

## Стек
Python 3.11 · Flet 0.28.3 · supabase-py · Supabase (RLS) · GitHub Actions · VS Code · DeepSeek

## Таблица `water_log`
| Поле | Тип | Описание |
|---|---|---|
| id | bigint (identity) | первичный ключ |
| amount | integer | объём, мл (1–5000) |
| date | date | день записи |
| created_at | timestamptz | время создания |

SQL и RLS-политики: `supabase_schema.sql`.

## Запуск на десктопе
1. `python -m venv .venv` и активировать
2. `pip install -r requirements.txt`
3. скопировать `config.example.py` → `config.py`, вписать URL и anon-ключ
4. `python main.py`

## Сборка APK
Push в `main` → вкладка Actions → артефакт `water-diary-apk`.
Нужные Secrets репозитория: `SUPABASE_URL`, `SUPABASE_KEY` (anon public).

## Лог промптов (заполнить по реальному диалогу с DeepSeek)
| № | Роль | Что просил | Что приложил | Ответ ИИ (кратко) | Сработало? | Что изменил дальше |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

## Разобранные проблемы
1. _(например: пустой список из-за RLS)_ — симптом / причина / решение
2. _(например: ошибка сборки в Actions)_ — симптом / причина / решение
3. _(например: ключи и Secrets)_ — симптом / причина / решение

## Что я понимаю и могу защитить
- _(своими словами: почему RLS, почему anon-ключ допустим в клиенте, как работает workflow)_
