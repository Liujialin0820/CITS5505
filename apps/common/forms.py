#encoding: utf-8  # Ensures UTF-8 encoding is used for the file (important for non-ASCII characters)

from wtforms import Form  # Import the base Form class from WTForms

class BaseForm(Form):
    # Custom base form class that extends WTForms' Form
    # Provides a helper method for retrieving the first validation error message

    def get_error(self):
        # This method returns the first validation error message in the form
        # 'self.errors' is a dictionary where keys are field names and values are lists of error messages

        message = self.errors.popitem()[1][0]  # Take the first error message from the first field that has errors
        return message  # Return the message string
