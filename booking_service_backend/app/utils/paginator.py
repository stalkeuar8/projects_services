from app.models.hotel import Rooms


class ResultsPaginator:
    def __init__(self, results: list[Rooms], results_per_page: int = 5):
        self.current_group = -1
        self.groups = [results[i : i + results_per_page] for i in range(0, len(results), results_per_page)]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current_group > len(self.groups) - 2:
            self.current_group += 1
            next_group = self.groups[self.current_group]
            return next_group
        else:
            raise StopIteration("You are on the last page, there is no next pages")

    def previous(self):
        if self.current_group == 0:
            raise StopIteration("You are on the first page, there is no previous page.")

        if self.current_group == -1:
            raise StopIteration("Pages were never printed.")

        self.current_group -= 1
        previous_group = self.groups[self.current_group]
        return previous_group
