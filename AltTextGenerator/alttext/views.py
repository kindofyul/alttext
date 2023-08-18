from django.shortcuts import render
from .forms import AltTextForm
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def alt_text_generator(request):
    if request.method == 'POST':
        form = AltTextForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            html_text = request.POST.get('html_text', '')  # Get HTML text from textarea
            
            # Process the uploaded Excel file to get image names and alt texts
            excel_data = get_excel_data(excel_file)  # Replace with your actual logic
            
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_text, 'html.parser')
            
            # Loop through Excel data and update HTML with alt attributes
            for excel_item in excel_data:
                excel_image_name = excel_item['이미지명']
                excel_alt_text = excel_item['이미지 해설']
                
                best_match_tag = None
                best_similarity = 0
                
                img_tags = soup.find_all('img')
                for img_tag in img_tags:
                    img_src = img_tag.get('src', '')
                    similarity = similar(excel_image_name, img_src)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match_tag = img_tag
                
                if best_match_tag:
                    best_match_tag['alt'] = excel_alt_text
            
            # Get the modified HTML
            modified_html = str(soup)
            
            return render(request, 'alt_text_generator.html', {'form': form, 'modified_html': modified_html})
    else:
        form = AltTextForm()
    return render(request, 'alt_text_generator.html', {'form': form})

def get_excel_data(excel_file):
    # Load Excel file using pandas
    df = pd.read_excel(excel_file)
    
    # Convert DataFrame to list of dictionaries
    excel_data = df.to_dict(orient='records')
    
    return excel_data
