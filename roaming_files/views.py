import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoamingInForm, RoamingOutForm
from roaming_files.utils.output_processing import output_roaming_out,output_roaming_in
from django.utils.timezone import now
from roaming_files.utils.graphs import roaming_in_dash, roaming_out_dash
from .models import RoamingOut, RoamingIn

def home(request):
    # Initialize the forms before checking the request method
    form_out = RoamingOutForm()
    form_in = RoamingInForm()

    if request.method == 'POST':
        if 'roaming_out_submit' in request.POST:
            form_out = RoamingOutForm(request.POST, request.FILES)
            if form_out.is_valid():

                # Save the form to create an instance of RoamingOut
                roaming_out_instance = form_out.save()

                # generate the output from the input entered
                input_file_path = roaming_out_instance.input_file.path
                output_df = output_roaming_out(input_file_path)

                # prepare the directory for the outputs
                output_directory = os.path.join(settings.MEDIA_ROOT, 'roaming_out_files', 'outputs')
                os.makedirs(output_directory, exist_ok=True)

                # outputs should have different file names
                timestamp = now().strftime('%Y%m%d_%H%M%S')
                output_file_path = os.path.join(output_directory, f'output_{timestamp}.csv')
                output_df.to_csv(output_file_path, index=False)

                # Update the model instance with the path to the CSV file
                roaming_out_instance.output_file.name = os.path.relpath(output_file_path, settings.MEDIA_ROOT)
                roaming_out_instance.save()

                # Redirect to the statistics page
                return redirect('roaming_out_stats', pk=roaming_out_instance.pk)

        elif 'roaming_in_submit' in request.POST:
            form_in = RoamingInForm(request.POST, request.FILES)
            if form_in.is_valid():
                roaming_in_instance = form_in.save()
                input_file_path = roaming_in_instance.input_file.path
                output_df = output_roaming_in(input_file_path)
                output_directory = os.path.join(settings.MEDIA_ROOT, 'roaming_in_files', 'outputs')
                os.makedirs(output_directory, exist_ok=True)
                timestamp = now().strftime('%Y%m%d_%H%M%S')
                output_file_path = os.path.join(output_directory, f'output_{timestamp}.csv')
                output_df.to_csv(output_file_path, index=False)
                roaming_in_instance.output_file.name = os.path.relpath(output_file_path, settings.MEDIA_ROOT)
                roaming_in_instance.save()

                #return redirect('home')
                return redirect('roaming_in_stats', pk=roaming_in_instance.pk)

    # Render the home page with both forms
    return render(request, 'home.html', {'form_out': form_out, 'form_in': form_in})

def roaming_in_stats(request, pk):
    # Get the instance of RoamingOut based on the primary key (pk)
    roaming_in_instance = get_object_or_404(RoamingIn, pk=pk)

    # Path to the output file
    output_file_path = os.path.join(settings.MEDIA_ROOT, roaming_in_instance.output_file.name)

    # Create the Dash app with the output file path
    roaming_in_dash(output_file_path)

    # Render the HTML template that includes the Dash app
    return render(request, 'roaming_in_statistics.html')

def roaming_out_stats(request, pk):

    roaming_out_instance = get_object_or_404(RoamingOut, pk=pk)
    output_file_path = os.path.join(settings.MEDIA_ROOT, roaming_out_instance.output_file.name)
    roaming_out_dash(output_file_path)

    return render(request, 'roaming_out_statistics.html')
