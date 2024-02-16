from django import forms

class BookForm(forms.Form):
    bookTitle = forms.CharField(label='Book Title', max_length=100)
    bookAuthor = forms.CharField(label='Book Author', max_length=100)
    ibsn = forms.CharField(label='IBSN', max_length=20, required=False)  # Assuming it's optional
    ibsn13 = forms.CharField(label='IBSN13', max_length=20, required=False)  # Assuming it's optional
    languageCode = forms.ChoiceField(label='Language', choices=[
        ('', 'Choose a language'),
        ('en', 'English (US)'),
        ('es', 'Spanish (Spain)'),
        ('fr', 'French (France)'),
        ('de', 'German (Germany)'),
    ])
    numPages = forms.IntegerField(label='Number of Pages')