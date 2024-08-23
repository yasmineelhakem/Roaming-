import os
import pandas as pd
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import RoamingOutForm
from .models import RoamingOut
from .utils.roaming_out.output_processing import process_output
from django.utils.timezone import now

def home(request):
    if request.method == 'POST':
        if 'roaming_out_submit' in request.POST:
            form_out = RoamingOutForm(request.POST, request.FILES)
            if form_out.is_valid():
                # Save the form to create an instance of RoamingOut
                roaming_out_instance = form_out.save()

                # Get the input file path
                input_file_path = roaming_out_instance.input_file.path

                # Process the input file to generate the first output DataFrame
                output_df = process_output(input_file_path)

                # Save the first output DataFrame as a CSV file
                output_directory = os.path.join(settings.MEDIA_ROOT, 'roaming_out_files', 'outputs')
                os.makedirs(output_directory, exist_ok=True)
                #output_file_path = os.path.join(output_directory, 'first_output.csv')
                timestamp = now().strftime('%Y%m%d_%H%M%S')
                output_file_path = os.path.join(output_directory, f'output_{timestamp}.csv')
                output_df.to_csv(output_file_path, index=False)

                # Update the model instance with the path to the CSV file
                roaming_out_instance.output_file.name = os.path.relpath(output_file_path, settings.MEDIA_ROOT)
                roaming_out_instance.save()

                return redirect('home')
    else:
        form_out = RoamingOutForm()

    return render(request, 'home.html', {'form_out': form_out})
