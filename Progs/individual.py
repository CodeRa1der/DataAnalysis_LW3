#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
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
    return routes


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

    list_parser = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Показать данные из JSON-файла"
    )

    # Разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить маршруты, если файл существует
    fill = False
    if os.path.exists(args.filename):
        routes = import_json(args.filename)
    else:
        routes = []

    # Добавить маршрут.
    if args.command == "add":
        add_route(routes, args.first, args.second)
        fill = True

    if args.command == "list":
        import_json(args.filename)

    if fill:
        export_to_json(args.filename, routes)

    # Показать список маршрутов.
    elif args.command == "list":
        list_of_routes(routes)


if __name__ == '__main__':
    main()
