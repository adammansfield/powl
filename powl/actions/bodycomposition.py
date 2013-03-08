"Action to process a body composition consisting of weight and bodyfat."""
import re
from powl.actions.fileaction import FileAction

class BodyComposition(FileAction):

    def _parse_message(self, data):
        """Parse body composition data into mass and body fat percentage."""
        mass = ''
        fat = ''
        params = re.split('-', data)
        for param in params:
            if re.match('^m', param):
                mass = re.sub('^m', '', param)
            elif re.match('^f', param):
                fat = re.sub('^f', '', param)
        mass = mass.strip()
        fat = fat.strip()
        return mass, fat

    # PROCESSING
    def process(self):
        """Process the data into the proper output format."""
        mass, fat = self._parse_message(self._input_data)
        self._output_data = "{0}, {1}".format(mass, fat)
