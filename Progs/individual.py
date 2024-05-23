#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path


# Необходимо реализовать в программе из прошлой лабораторной работы
# интерфейс командной строки (CLI)


def add_route(routes, first, second):
    # Запись данных маршрута
    routes.append(
        {
            'first': first,
            'second': second,
        }
    )


def export_to_json(file, routes_list):
    with open(file, 'w', encoding='utf-8') as fileout:
        json.dump(routes_list, fileout, ensure_ascii=False, indent=4)


def import_json(file):
    with open(file, 'r', encoding='utf-8') as filein:
        return json.load(filein)


def list_of_routes(roadway):
    if roadway:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 14,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^5} | {:^20} | {:^20} |'.format(
                "Номер маршрута",
                "Место отправки",
                "Место прибытия"
            )
        )
        print(line)
        # Вывод данных о маршрутах
        for number, route in enumerate(roadway, 1):
            print(
                '| {:<14} | {:<20} | {:<20} |'.format(
                    number,
                    route.get('first', ''),
                    route.get('second', '')
                )
            )
            print(line)
    else:
        print("Список маршрутов пуст")


def help():
    print('\nСписок команд:')
    print('help - Вывести этот список')
    print('add - Добавить маршрут')
    print('list - Показать список маршрутов')
    print('exit - Выйти из программы')
    print('export - Экспортировать данные в JSON-файл')
    print('import (имя файла) - Импортировать данные')


def main(command_line=None):
    # Родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="Имя файла с данными"
    )

    # Основной парсер командной строки.
    parser = argparse.ArgumentParser("routes")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Субпарсер для добавления маршрута.
    add_parser = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавить новый маршрут"
    )
    add_parser.add_argument(
        "--first",
        action="store",
        required=True,
        help="Место отправки"
    )
    add_parser.add_argument(
        "--second",
        action="store",
        required=True,
        help="Место прибытия"
    )

    # Субпарсер для отображения всех маршрутов.
    display_parser = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Показать список маршрутов"
    )

    # Субпарсер для экспорта маршрутов.
    export_parser = subparsers.add_parser(
        "export",
        parents=[file_parser],
        help="Экспортировать маршруты в JSON-файл"
    )
    export_parser.add_argument(
        "export_file",
        action="store",
        help="Имя файла для экспорта"
    )

    # Субпарсер для импорта маршрутов.
    import_parser = subparsers.add_parser(
        "import",
        parents=[file_parser],
        help="Импортировать маршруты из JSON-файла"
    )
    import_parser.add_argument(
        "import_file",
        action="store",
        help="Имя файла для импорта"
    )

    # Разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Список маршрутов
    routes = []

    # Загрузить маршруты из файла, если файл существует.
    if os.path.exists(args.filename):
        routes = import_json(args.filename)

    elif args.command != "import":
        # Создать пустой файл, если он не существует при любой команде, кроме "import"
        with open(args.filename, 'w', encoding='utf-8') as file:
            json.dump([], file)

    # Добавить маршрут.
    if args.command == "add":
        add_route(routes, args.first, args.second)
        export_to_json(args.filename, routes)

    # Показать список маршрутов.
    elif args.command == "list":
        list_of_routes(routes)

    # Экспортировать маршруты в файл.
    elif args.command == "export":
        export_to_json(args.export_file, routes)

    # Импортировать маршруты из файла.
    elif args.command == "import":
        routes = import_json(args.import_file)
        export_to_json(args.filename, routes)


if __name__ == '__main__':
    main()
