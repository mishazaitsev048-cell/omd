import csv


def report_1(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    if not isinstance(rows, list):
        raise ValueError('Отчет принимает список')
    commands: dict[str, set[str]]
    commands = {}
    for row in rows:
        commands[row['Департамент']] = commands.get(row['Департамент'], set())
        commands[row['Департамент']].add(row['Отдел'])
    return commands


def report_2(rows: list[dict[str, str]]) -> list[dict[str, str | int | float]]:
    if not isinstance(rows, list):
        raise ValueError('Отчет принимает список')
    dep_stats: dict[str, list[int]]
    dep_stats = {}
    for row in rows:
        try:
            salary = int(row['Оклад'])
        except ValueError:
            raise ValueError(f'в окладе проблемы: {row["Оклад"]} '
                             'он не переводится в int')
        if row['Департамент'] not in dep_stats:
            dep_stats[row['Департамент']] = [1, salary, salary, salary]
            # количество сотрудников, минимальная, максимальная и сумма зарплат
        else:
            dep_stats[row['Департамент']][0] += 1
            current_min = dep_stats[row['Департамент']][1]
            current_max = dep_stats[row['Департамент']][2]
            dep_stats[row['Департамент']][1] = min(current_min, salary)
            dep_stats[row['Департамент']][2] = max(current_max, salary)
            dep_stats[row['Департамент']][3] += salary
    dep_summaries: list[dict[str, str | int | float]]
    dep_summaries = []
    for dep, stats in dep_stats.items():
        mean_salary = round(stats[-1] / stats[0], 2)
        dep_summary: dict[str, str | int | float]
        dep_summary = {
            'Департамент': dep,
            'численность': stats[0],
            'минимальная зарплата': stats[1],
            'максимальная зарплата': stats[2],
            'средняя зарплата': mean_salary
            }
        dep_summaries.append(dep_summary)
    return dep_summaries


def report_3(rows: list[dict[str, str]],
             output_file_name: str = 'homework_report.csv') -> None:
    if not isinstance(rows, list):
        raise ValueError('Отчет принимает список')
    summaries = report_2(rows)
    with open(output_file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
                                f,
                                fieldnames=summaries[0].keys(),
                                delimiter=';'
                                )
        writer.writeheader()
        writer.writerows(summaries)
    print(f'Отчет записан в файл {output_file_name}')


def reader(file_name: str) -> list[dict[str, str]]:
    with open(file_name, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        if csv_reader.fieldnames is None:
            raise ValueError('Пустой csv, нет шапки')
        required_columns = {'ФИО полностью',
                            'Департамент',
                            'Отдел',
                            'Должность',
                            'Оценка',
                            'Оклад'
                            }
        missing_col = required_columns - set(csv_reader.fieldnames)
        if missing_col:
            raise ValueError('В CSV-файле нет колонок: '
                             f'{", ".join(missing_col)}')
        rows = list(csv_reader)
        if len(rows) == 0:
            raise ValueError('Пустой csv, нет строк')
    return rows


def main(report_number: int,
         file_name: str = 'Corp_Summary.csv',
         output_file_name: str | None = None) -> None:
    if isinstance(report_number, bool) or not isinstance(report_number, int):
        raise ValueError('Номер отчета должен быть числом')
    if not isinstance(file_name, str):
        raise ValueError('Название входного файла должно быть строкой')
    if output_file_name is not None and not isinstance(output_file_name, str):
        raise ValueError('Название выходного файла '
                         'должно быть строкой')
    if report_number > 3 or report_number < 1:
        raise ValueError('Введите номер отчета от 1 до 3')
    rows = reader(file_name)
    if report_number == 1:
        hierarchy = report_1(rows)
        for dep, teams in hierarchy.items():
            print(dep, ': ', ', '.join(teams), sep='')
    elif report_number == 2:
        summary = report_2(rows)
        print(*summary, sep='\n')
    elif report_number == 3:
        if output_file_name is None:
            report_3(rows)
        else:
            report_3(rows, output_file_name)
