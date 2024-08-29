import pandas as pd
import numpy as np
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException, region_code_for_number
import pycountry
from phonenumbers import carrier

def country_operator(vlr_number):
    try:
        # Parse the VLR number
        phone_number = phonenumbers.parse("+" + str(vlr_number))
        # Get the region code (ISO 3166-1 alpha-2) for the number
        country_code = region_code_for_number(phone_number)

        if not country_code:
            return "Country not found", "Operator not found"

        # Convert the ISO 3166-1 alpha-2 code to the full country name
        country = pycountry.countries.get(alpha_2=country_code)
        country_name = country.name if country else "Country not found"

        # Get the operator name
        operator_name = carrier.name_for_number(phone_number, "en")

        return country_name, operator_name

    except NumberParseException as e:
        print(f"Error parsing number: {e}")
        return "Country not found", "Operator not found"
def output_roaming_in(file_path):
    input_df = pd.read_csv(file_path, sep='\s+', skiprows=11, skipfooter=22, engine='python')
    input_df.columns = ["HLRADDR", "NSUB", "NSUBA"]


    # Lists to store the results
    country_names = []
    operators = []

    # Counters for missing data
    so = 0  # Missing operator name
    sc = 0  # Missing country name

    for hlraddr in input_df['HLRADDR']:
        hlr = hlraddr[2:]
        country_name, operator = country_operator(hlr)
        country_names.append(country_name)
        operators.append(operator)
        if not operator:
            so += 1
        if country_name == 'Country not found':
            sc += 1

    # Print the counters for missing data
    print('Number of entries with missing operator names: ', so)
    print('Number of entries with missing country names: ', sc)

    # Add the results to the DataFrame
    output_df = input_df.copy()
    output_df['Country Name'] = country_names
    output_df['Operator'] = operators
    output_df.rename(columns={'NSUB': 'Number of SUBS'}, inplace=True)

    # Print the output DataFrame
    print("Output DataFrame:\n", output_df)
    #output_df.to_csv('output.csv', index=False)
    return output_df

def output_roaming_out(file_path):
    input_df = pd.read_csv(file_path, skiprows=1)

    vlr_sum = input_df.groupby('VLR_NUMBER')['MSISDN'].count().reset_index()
    vlr_sum.columns = ['VLR NUMBER', 'Number of SUBS']

    vlr_sorted = vlr_sum.sort_values(by=['Number of SUBS', 'VLR NUMBER'], ascending=[False, True])

    total_general = pd.DataFrame(np.array([['Total général', len(input_df)]]), columns=['VLR NUMBER', 'Number of SUBS'])
    output_df = pd.concat([total_general, vlr_sorted], ignore_index=True)

    output_cleaned = output_df.drop(index=0)

    country_names = []
    operators = []

    for vlr_number in output_cleaned['VLR NUMBER']:
        country_name, operator = country_operator(vlr_number)
        country_names.append(country_name)
        operators.append(operator)

    output_cleaned['Country Name'] = country_names
    output_cleaned['Operator'] = operators

    return output_cleaned
