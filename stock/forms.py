from django import forms

class SearchKeywordForm(forms.Form):
    search_keyword = forms.CharField(max_length=100)

    def clean_search_keyword(self):
        data = self.cleaned_data['search_keyword']
        #check data
        return data

