#backend/api/validations.py

from django.core.exceptions import ValidationError

class UserValidator:
    concern_keys = ["email", "password", "username", "first_name", "last_name"]

    @staticmethod
    def validate_email(email):
        # Replace this with actual email validation logic
        if "@" in email:
            return True, email
        return False, "Invalid email"

    @staticmethod
    def validate_password(password):
        # Replace this with actual password validation logic
        if len(password) >= 6:
            return True, password
        return False, "Invalid password"

    @staticmethod
    def validate_username(username):
        # Replace this with actual username validation logic
        if username.isalnum():
            return True, username
        return False, "Invalid username"

    @staticmethod
    def validate_first_name(first_name):
        # Replace this with actual first name validation logic
        if first_name.isalpha():
            return True, first_name
        return False, "Invalid first name"

    @staticmethod
    def validate_last_name(last_name):
        # Replace this with actual last name validation logic
        if last_name.isalpha():
            return True, last_name
        return False, "Invalid last name"

    def all(self, data_object, all_required=True):
        """
        Validate all the keys in the data_object.

        :param data_object: A dictionary containing the keys and values to validate.
        :type data_object: dict
        :param all_required: A boolean indicating whether all concern_keys must be present in data_object.
        :type all_required: bool
        :return: A tuple containing a boolean indicating success or failure and either a dictionary of validated data or an error message.
        :rtype: tuple
        """

        missing_keys = [key for key in self.concern_keys if key not in data_object]
        invalid_keys = [key for key in data_object if key not in self.concern_keys]

        if all_required and missing_keys:
            return False, f"{missing_keys} are missing"
        if invalid_keys:
            return False, f"Invalid keys: {invalid_keys}"

        clean_data = {}
        invalid_values = []

        for key, value in data_object.items():
            validate_method = getattr(self, f"validate_{key}", None)
            if validate_method:
                valid, result = validate_method(value)
                if valid:
                    clean_data[key] = result
                else:
                    invalid_values.append(result)

        if invalid_values:
            return False, f"Invalid values: {invalid_values}"

        return True, clean_data
class PostValidator:
    concern_keys = ["content", "image", "type"]

    @staticmethod
    def validate_content(content):
        if isinstance(content, str) and content.strip():
            return content
        return False

    @staticmethod
    def validate_image(image):
        # Add your image validation logic here, for now, assuming it's always valid
        return image

    @staticmethod
    def validate_type(post_type):
        if post_type in ["meme", "info"]:
            return post_type
        return False

    @classmethod
    def all(cls, data_obj, all_required=True):
        invalid_keys = [key for key in data_obj if key not in cls.concern_keys]
        if invalid_keys:
            return (False, f"Invalid keys: {', '.join(invalid_keys)}")

        if all_required:
            missing_keys = [key for key in cls.concern_keys if key not in data_obj]
            if missing_keys:
                return (False, f"Missing keys: {', '.join(missing_keys)}")

        clean_data = {}
        for key in data_obj:
            validate_method = getattr(cls, f"validate_{key}", None)
            if validate_method:
                valid_value = validate_method(data_obj[key])
                if not valid_value:
                    return (False, f"Invalid value for {key}")
                clean_data[key] = valid_value

        return (True, clean_data)
class CommentValidator:
    concern_keys = ["content"]

    @staticmethod
    def validate_content(content):
        if isinstance(content, str) and content.strip():
            return content
        return False

    @classmethod
    def all(cls, data_obj, all_required=True):
        invalid_keys = [key for key in data_obj if key not in cls.concern_keys]
        if invalid_keys:
            return (False, f"Invalid keys: {', '.join(invalid_keys)}")

        if all_required:
            missing_keys = [key for key in cls.concern_keys if key not in data_obj]
            if missing_keys:
                return (False, f"Missing keys: {', '.join(missing_keys)}")

        clean_data = {}
        for key in data_obj:
            validate_method = getattr(cls, f"validate_{key}", None)
            if validate_method:
                valid_value = validate_method(data_obj[key])
                if not valid_value:
                    return (False, f"Invalid value for {key}")
                clean_data[key] = valid_value

        return (True, clean_data)


def custom_validation(data):
    from .models import Users

    email = data["email"].strip()
    username = data["username"].strip()
    password = data["password"].strip()
    ##
    if not email or Users.objects.filter(email=email).exists():
        raise ValidationError("choose another email")
    ##
    if not username or Users.objects.filter(username=username).exists():
        raise ValidationError("choose another username")
    ##

    if not password or len(password) < 8:
        raise ValidationError("choose another password, min 8 characters")
    ##
    if not username:
        raise ValidationError("choose another username")
    return data


def validate_email(data):
    email = data["email"].strip()
    if not email:
        raise ValidationError("an email is needed")
    return True


def validate_username(data):
    username = data["username"].strip()
    if not username:
        raise ValidationError("choose another username")
    return True


def validate_password(data):
    password = data["password"].strip()
    if not password:
        raise ValidationError("a password is needed")
    return True