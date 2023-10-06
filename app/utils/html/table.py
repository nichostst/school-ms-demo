from typing import List, Dict


class Tabulator:
    def __init__(self):
        self.row_point = 0
        self.col_point = 0
        self.alias = None
        self.data = None

    def _add_attributes(self, line: str):
        if '<tr>' in line:
            tag = '<tr>'
            identifier = f'{self.alias}-row'
            aliased = f'<tr class="{identifier}" id="{identifier}-{self.row_point}">'
        elif '<th>' in line:
            tag = '<th>'
            identifier = f'{self.alias}-header'
            aliased = f'<th class="{identifier}" id="{identifier}-{self.col_point}">'
        elif '<td>' in line:
            tag = '<td>'
            identifier = f'{self.alias}-data'
            aliased = f'<td class="{identifier}" id="{identifier}-{self.row_point}-{self.col_point}">'
        else:
            raise ValueError('Element <th>, <td>, or <tr> not found.')

        return line.replace(tag, aliased)

    def tr(self, entries: Dict, header: bool) -> str:
        if not header:
            self.row_point += 1

        lines = [self._add_attributes('<tr>')]

        if header:
            for c in self.col_labels:
                self.col_point += 1
                lines.append(self._add_attributes(f'<th>{c}</th>'))
        else:
            for c in self.cols:
                self.col_point += 1
                lines.append(self._add_attributes(f'<td>{entries[c]}</td>'))

        lines.append('</tr>')
        # Reset column
        self.col_point = 0

        return '\n'.join(lines)

    def body(self):
        rows = []
        for row in self.data:
            rows.append(self.tr(entries=row, header=False))

        return '\n'.join(rows)

    def tabulate(self, data: List[Dict], cols: List[str], col_labels: List[str], alias: str, styles: List) -> str:
        self.data = data
        self.cols = cols
        self.col_labels = col_labels
        self.alias = alias
        styles = ' '.join(styles)

        components = [f'<table class="{self.alias}-table {styles}" id="{self.alias}-table">']
        header = self.tr(entries=None, header=True)
        rows = self.body()

        components.append('<thead>')
        components.append(header)
        components.append('</thead>')

        components.append('<tbody>')
        components.append(rows)
        components.append('</tbody>')

        components.append('</table>')

        return '\n'.join(components)
