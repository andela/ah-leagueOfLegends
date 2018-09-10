import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    # allow_blank=True, to enable `" "` as a valid value for a password so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a password
    password = serializers.CharField(max_length=128, write_only=True,  allow_blank=True, allow_null=True)

    # Ensure emails are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a email so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a email
    email = serializers.EmailField(max_length=128, allow_blank=True, allow_null=True)

    # Ensure username are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a username so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a username
    username = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)

    def validate_email(self, data):
        """Validate the email address"""
        email = data
        if email == '':
            raise serializers.ValidationError('Email field is required.')
        elif User.objects.filter(email=email):
            raise serializers.ValidationError('This email is not available. Please try another.')
        return data

    def validate_username(self, data):
        """Validate the username"""
        username = data
        if username == '':
            raise serializers.ValidationError('Username field is required.')
        elif User.objects.filter(username=username):
            raise serializers.ValidationError('This username is not available. Please try another.')
        return data

    def validate_password(self, data):
        """Validate the password"""
        password = data
        # Ensure passwords are not empty.
        if password == "":
            raise serializers.ValidationError("Password field is required.")
        # Ensure passwords are longer than 8 characters.
        elif len(password) < 8:
            raise serializers.ValidationError(
                'Create a password at least 8 characters.')
        # Ensure passwords contain a number.
        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                'Create a password with at least one number.')
        # Ensure passwords contain an uppercase letter.
        elif not re.match(r"^(?=.*[A-Z])(?!.*\s).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one uppercase letter")
        # Ensure passwords contain a special character
        elif re.match(r"^[a-zA-Z0-9_]*$", password):
            raise serializers.ValidationError(
                "Create a password with at least one special character.")
        return data
    # password = serializers.CharField(
    #     max_length=128,
    #     min_length=8,
    #     write_only=True
    # )
    # token = serializers.CharField(max_length=255, read_only=True)

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token

        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and De-serialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'bio', 'image','profile')


        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)
        user_profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)


        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        for (key, value) in user_profile_data.items():
            setattr(instance.profile, key, value)
        
        instance.profile.save()

        return instance


class EmailSerializer(serializers.Serializer):
    '''
    Handles serialization of emails and returns a token generated \from the email
    '''
    email = serializers.EmailField(max_length=255)
    token = serializers.CharField(max_length=255, required=False)

    def validate(self, payload):
        check_user = User.objects.filter(email=payload.get('email', None))\
            .first()
        if not check_user:
            raise serializers.ValidationError('Email does not exist')
        token = default_token_generator.make_token(check_user)
        return{
                'email': payload['email'],
                'token': token
            }


class ResetUserPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    # uuid = serializers.CharField(max_length=30, required=False)
    token = serializers.CharField(max_length=255, required=False)
    confirm_password = serializers.CharField(
                min_length=6,
                max_length=80,
                write_only=True
            )
    new_password = serializers.CharField(
                min_length=6,
                max_length=80,
                write_only=True
            )

    def validate(self, validated_data):
        if validated_data['confirm_password'] != validated_data['new_password']:
            raise serializers.ValidationError(
                "Passwords Dont Match"
            )
        from django.contrib.auth.tokens import default_token_generator
        user_email = User.objects.filter(email=validated_data.get('email',
                                         None)).first()
        check_valid_token = default_token_generator.check_token(
                user_email, validated_data.get('token', None)
                )
        if not check_valid_token:
            raise serializers.ValidationError(
                    "Token expired or Invalid"
                )
        user_email.set_password(validated_data.get('new_password', None))
        user_email.save()
        return validated_data
class SocialAuthSerializer(serializers.Serializer):
    """Serializers social_auth requests"""
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=1024, required=True, trim_whitespace=True)
