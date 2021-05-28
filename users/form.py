from django.contrib.auth.forms import UserCreationForm

# Obtiene el modelo de datos de usuraio para crear nuevos usuarios.
class CustomUserCreationForm(UserCreationForm):

    # Con la clase meta nos servirá para añadir un campos que nos falta Email.
    class Meta(UserCreationForm.Meta):
        # agregamos el campo Email.
        fields = UserCreationForm.Meta.fields + ("email",)