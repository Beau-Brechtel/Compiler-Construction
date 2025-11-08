class AssemblyInstruction:

    def __init__(self, operation=None, destination=None, source=None, label=None):
        self.operation = operation
        self.destination = destination
        self.source1 = source
        self.label = label

    def __str__(self):
        if self.label:
            return f"{self.label}:"
        elif self.source1 is None and self.destination is None:
            return f"\t{self.operation}"
        elif self.source1 is None:
            return f"\t{self.operation}\t{self.destination}"
        elif self.destination is None:
            return f"\t{self.operation}\t{self.source1}"
        else:
            return f"\t{self.operation}\t{self.destination}, {self.source1}"

