from common.utils import compress_image
from django import forms
from .models import User
from typing import Any


class UserImageCompressForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["photo"]

    def save(self, commit=True) -> Any:
        instance = super(UserImageCompressForm, self)
        if instance:
            instance = super(UserImageCompressForm, self).save(commit=False)
            if "photo" in self.changed_data:
                instance.photo = compress_image(
                    self.cleaned_data.get("photo"), is_small_thumbnail=True, quality=80
                )
                instance.save()
            return instance
