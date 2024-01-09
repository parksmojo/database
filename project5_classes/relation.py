from .header import Header
from .row import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set = None) -> None:
        self.name: str = name
        self.header: Header = header
        if rows is None:
            rows = set()
        self.rows: set[Row] = rows
    
    def __str__(self) -> str:
        output_str: str = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue
            sep: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += self.header.values[i]
                output_str += "="
                output_str += row.values[i]
                sep = ", "
            output_str += "\n"
        return output_str
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError("Row and header must be the same length")
        #print(f"adding row: {row.values}")
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':
        if colIndex not in range(len(self.header.values)):
            raise ValueError("Index out of range in Select1")
        
        new_rows: list[Row] = []
        for row in self.rows:
            if row.values[colIndex] == value:
                new_rows.append(row)

        return Relation(self.name, self.header, new_rows)
    
    def select2(self, index1: int, index2: int) -> 'Relation':
        if index1 not in range(len(self.header.values)) or index2 not in range(len(self.header.values)):
            raise ValueError("Index out of range in Select2")
        
        new_rows: list[Row] = []
        for row in self.rows:
            if row.values[index1] == row.values[index2]:
                new_rows.append(row)

        return Relation(self.name, self.header, new_rows)
    
    def rename(self, new_header: Header) -> 'Relation':
        if len(new_header.values) != len(self.header.values):
            raise ValueError("Renamed header does not match size of old header")
        return Relation(self.name, new_header, self.rows)

    def project(self, col_indexes: list[int]) -> 'Relation':
        for index in col_indexes:
            if index not in range(len(self.header.values)):
                raise ValueError("Index out of range in project")
            
        new_header: list[str] = []
        new_rows: list[Row] = []
        for index in col_indexes:
            new_header.append(self.header.values[index])
        for row in self.rows:
            values: list[str] = []
            for index in col_indexes:
                values.append(row.values[index])

            is_unique = True
            for rowx in new_rows:
                if values == rowx.values:
                    is_unique = False
            if is_unique:
                new_rows.append(Row(values))

        
        return Relation(self.name, Header(new_header), new_rows)
    
    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x, y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
        return True
        
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        new_row_values: list[str] = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])
        new_row_values.extend(row2.values)
        return Row(new_row_values)
        
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        new_header_values: list[str] = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])
        new_header_values.extend(header2.values)
        return Header(new_header_values)
    
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        for x in range(len(r1.header.values)):
            is_unique = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)
                
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)

        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1, t2, overlap):
                    result_row = self.join_rows(t1, t2, unique_cols_1)
                    result.add_row(result_row)
        
        return result
    
    def union(self, other: 'Relation') -> str:
        r1: Relation = self
        r2: Relation = other
        new_row_str = ""

        for row in sorted(r2.rows):
            if row not in r1.rows:
                sep: str = ""
                new_row_str += "  "
                for i in range(len(self.header.values)):
                    new_row_str += sep
                    new_row_str += self.header.values[i]
                    new_row_str += "="
                    new_row_str += row.values[i]
                    sep = ", "
                new_row_str += "\n"

        r1.rows.update(r2.rows)
        return new_row_str
