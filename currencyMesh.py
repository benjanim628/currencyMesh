## currency mesh
## benjamin janowski
## v1.01

import requests

def get_currency(base_list, symbols_list, date):
    
    ## api generic info:
    historical_url = 'http://data.fixer.io/api/'
    api_key = '?access_key=e258a802c4451300b7ec23dcbac7a738'
    currency_pairs = {}

    ## create currency request:
    base_string = ''
    symbols_string = ''
    for value in base_list:
        base_string += value +','
    for value in symbols_list:
        symbols_string += value +','
    historical_request_text = requests.get(historical_url + date + api_key + '&symbols=' + symbols_string + ',' + base_string).text

    ## calculate base value:
    for i in range(len(base_list)):

        #currency_pairs = {} # new dict to store results in

        if(base_list[i]=='EUR'):
            base_value = 1
        else:
            start = historical_request_text.find(base_list[i]) + 5
            end = start + 5
            base_value = float(historical_request_text[start:end])
        
        ## calculate symbol value for current base:
        for j in range(len(symbols_list)):
            if(symbols_list[j]=='EUR'):
                symbol_value = 1
            else:
                start = historical_request_text.find(symbols_list[j]) + 5
                end = start + 5
                symbol_value = float(historical_request_text[start:end])

            ## calculate symbol:base value:
            symbolbase_value = symbol_value/base_value
            # print(symbols_list[j] + ':' + base_list[i] + '=' + str(symbolbase_value))
            if (i == 0):
                currency_pairs[symbols_list[j]] = {base_list[i]:symbolbase_value}
            else:
                # currency_pairs['ZAR'].update({base_list[i]:symbolbase_value})
                currency_pairs[symbols_list[j]][base_list[i]] = symbolbase_value
            j += 1
        i += 1

    return currency_pairs

def get_date_range(beginning_date, end_date):
    ## declare variables:
    date_range_list = ()
    month_dependant_length = 0
    from_day = 0
    to_day = 0
    from_month = 0
    to_month = 0

    ## parse dates:
    beg_day = int(beginning_date[8:10])
    beg_month = int(beginning_date[5:7])
    beg_year = int(beginning_date[0:4])
    end_day = int(end_date[8:10])
    end_month = int(end_date[5:7])
    end_year = int(end_date[0:4])

    ## loop through all dates, starting with years:
    for current_year_int in range(beg_year, end_year + 1):

        ## get year interger to text
        current_year_string = str(current_year_int)

        ## set from_month and to_month depending on 4 situations:
        if(beg_year == end_year):
            from_month = beg_month
            to_month = end_month
        elif(beg_year != end_year and current_year_int == beg_year):
            from_month = beg_month
            to_month = 12
        elif(beg_year != end_year and current_year_int == end_year):
            from_month= 1
            to_month = end_month
        else:
            from_month = 1
            to_month = 12

        ## loop through all months of current year:
        for current_month_int in range(from_month, to_month + 1):
            
            ## get month integer to string:
            if(current_month_int in (10, 11, 12)):
                current_month_string = str(current_month_int)
            else:
                current_month_string = '0' + str(current_month_int)

            ## set month_dependant_length according to month type:
            if(current_month_int == 2 and current_year_int%4 == 0):
                month_dependant_length = 29
            elif(current_month_int == 2):
                month_dependant_length = 28
            elif(current_month_int in (4,6,9,11)):
                month_dependant_length = 30
            else:
                month_dependant_length = 31

            ## set from_day and to_day depending on 4 situations:
            if(beg_month == end_month and beg_year == end_year):
                from_day = beg_day
                to_day = end_day
            elif(current_month_int == beg_month and beg_year == current_year_int):
                from_day = beg_day
                to_day = month_dependant_length
            elif(current_month_int == end_month and current_year_int == end_year):
                from_day = 1
                to_day = end_day
            else:
                from_day = 1
                to_day = month_dependant_length

            ## loop through all days in current month:
            for current_day_int in range(from_day, to_day + 1):
                if(current_day_int<10):
                    current_day_string = '0' + str(current_day_int)
                else:
                    current_day_string = str(current_day_int)
                new_date = (current_year_string + '-' + current_month_string + '-' + current_day_string)
                date_range_list += (new_date,)
    return date_range_list

def get_currency_for_range(base_list, symbols_list, beginning_date, end_date):

    ## create base variables:
    all_date_currencies_list = []
    date_range_list = get_date_range(beginning_date, end_date)

    for current_date in date_range_list:
        current_date_currencies = get_currency(base_list, symbols_list, current_date)
        all_date_currencies_list.append(current_date_currencies)
    
    return all_date_currencies_list

## do calculations with currency values
## Investing Stratergy 1:

def get_symbol_average_for_range(base_list, symbols_list, beginning_date, end_date):

    ## create return variables:
    all_averages_dict = {}

    ## loop through get_currency_for_range() data and add it's values to above defined variables: 
    currency_pairs_date_range = get_currency_for_range(base_list, symbols_list, beginning_date, end_date)

    ## calculate for each symbol:
    for current_symbol in symbols_list:
        all_averages_dict[current_symbol] = {}
    
        ## calculate for each base in current symbol:
        for base in base_list:

            ## create variables:
            total_value = 0
            average_value = 0
            counter = 0

            ## loop through all values:
            for date in currency_pairs_date_range:
                total_value += date[current_symbol][base]
                counter += 1

            average_value = total_value/counter
            all_averages_dict[current_symbol][base] = average_value 

    return all_averages_dict

def find_all_trends(base_list, symbols_list, beginning_date, end_date):

    ## create return value:
    all_trends_dict = {}

    ## get return value of get_symbol_average_for_range()
    all_averages_dict = get_symbol_average_for_range(base_list, symbols_list, beginning_date, end_date)

    ## loop though all symbols:
    for current_symbol in symbols_list:
        all_trends_dict[current_symbol] = {}

        for current_base in base_list:
            current_base_average_value = all_averages_dict[current_symbol][current_base]

            ## create base and symbol list from string:
            current_base_list = [current_base]
            current_symbol_list = [current_symbol]

            end_date_dict = get_currency(current_base_list, current_symbol_list, end_date)
            end_date_base_value = end_date_dict[current_symbol][current_base]

            ## calculate end_date_base_value / current_base_average_value to create float > 1 for upward trend:
            trend = end_date_base_value / current_base_average_value

            ## add trend to all_trends_dict:
            all_trends_dict[current_symbol][current_base] = trend
            
    return all_trends_dict

def find_all_trends_averages(base_list, symbols_list, beginning_date, end_date):

    ## create return variable:
    trend_averages = {}
    
    ## get find_all_trends() return value:
    find_all_trends_dict = find_all_trends(base_list, symbols_list, beginning_date, end_date)

    ## add all values of the same base and then get average; do this for each base and add each 
    ## base-value pair to the return dictionary:
    for current_base in base_list:

        ## create required variables:
        averages_total = 0
        averages_average = 0
        counter = 0

        for current_symbol in symbols_list:
            current_base_value = find_all_trends_dict[current_symbol][current_base]
            averages_total += current_base_value
            counter += 1

        averages_average = averages_total / counter

        trend_averages[current_base] = averages_average
    
    return trend_averages
      
def find_top_trend(base_list, symbols_list, beginning_date, end_date):

    ## create required variable:
    top_trend_dict = {}
    top_trend_value = 2

    ## get find_top_trend-averages() return variable:
    top_trends_averages_dict = find_all_trends_averages(base_list, symbols_list, beginning_date, end_date)

    ## find largest variable:
    for key in top_trends_averages_dict:
        if(top_trends_averages_dict[key] < top_trend_value):
            top_trend_value = top_trends_averages_dict[key]
            top_trend_dict['Top trend is'] = {key:top_trend_value}

    return top_trend_dict

## get next date fubctions:

def get_final_date_loop(current_day, current_month, current_year):

    if(current_day > 28):
        
        ## get month_dependant_length:
        month_dependant_length = get_month_dependant_length(current_month, current_year)

        ## calculate what new month date should be:
        if(current_day > month_dependant_length):
            current_day = current_day - month_dependant_length

        current_month += 1

        ## if current_month is bigger than 12 then the year must be incremented and current_month = 1:
        if(current_month == 13):
            current_year += 1
            current_month = 1

        ## if current_day is still bigger than month_dependant_length, repeat function:
        if(current_day > get_month_dependant_length(current_month, current_year)):
            return get_final_date_loop(current_day, current_month, current_year)

        ## otherwise return final date:
        else:
            ## add preceding 0 if month or day value is smaller than 10:
            if(current_day < 10):
                current_day_string = '0' + str(current_day)
            else:
                current_day_string = str(current_day)
            if(current_month < 10):
                current_month_string = '0' + str(current_month)
            else:
                current_month_string = str(current_month)

            ## create final date string and return it:
            new_date = str(current_year) + '-' + current_month_string + '-' + current_day_string 
            return new_date


    else:
        ## add preceding 0 if month or day value is smaller than 10:
        if(current_day < 10):
            current_day_string = '0' + str(current_day)
        else:
            current_day_string = str(current_day)
        if(current_month < 10):
            current_month_string = '0' + str(current_month)
        else:
            current_month_string = str(current_month)

        ## create final date string and return it:
        new_date = str(current_year) + '-' + current_month_string + '-' + current_day_string
        return new_date

## function - return month_dependant_length based on month and year:
def get_month_dependant_length(current_month, current_year):
    month_dependant_length = 0
    if(current_month == 2 and current_year%4 == 0):
        month_dependant_length = 29
    elif(current_month == 2):
        month_dependant_length = 28
    elif(current_month in (4,6,9,11)):
        month_dependant_length = 30
    else:
        month_dependant_length = 31
    
    return month_dependant_length

def increment_date(date, increment):

    ## parse dates:
    beg_day = int(date[8:10])
    beg_month = int(date[5:7])
    beg_year = int(date[0:4])

    ## set current values:
    current_day = beg_day + increment
    current_month = beg_month
    current_year = beg_year

    return get_final_date_loop(current_day, current_month, current_year)
## end of get next date functions.

def invest_based_on_top_trend(base_list, symbols_list, beginning_date, end_date):

    ## start off with $1000 and invest in top trend currency, update currency holding every 5 days based 
    ## on trend:
    current_holdings = 1000
    current_currency = 'USD'

    ## calculate number of investment periods:
    all_dates_list = get_date_range(beginning_date, end_date)
    investment_periods = round(len(all_dates_list) / 5) ## denominator = one investment period

    current_date = beginning_date
    increment = 5

    for i in range(investment_periods):
        increment_date_value = increment_date(current_date, increment)

        ## top trend return value:
        top_trend_dict = find_top_trend(base_list, symbols_list, current_date, increment_date_value)
        for key in top_trend_dict['Top trend is']:
            final_key = key
        top_trend_symbol = final_key

        ## get top trend current trading value:
        top_trend_currency_value_dict = get_currency([current_currency], [top_trend_symbol], increment_date_value)
        top_trend_currency_value = top_trend_currency_value_dict[top_trend_symbol][current_currency]

        ## convert current holdings to top trend currency:
        current_holdings = current_holdings * top_trend_currency_value
        current_currency = top_trend_symbol

        ## update current_date value:
        current_date = increment_date_value

    ## calculate equivilent USD holdings:
    USD_as_symbol_value_dict = get_currency([current_currency], ['USD'], end_date)
    USD_as_symbol_value = USD_as_symbol_value_dict['USD'][current_currency]
    USD_holdings = current_holdings * USD_as_symbol_value

    return 'Your final holdings are ' + current_currency + ': ' + str(current_holdings) + 'which is equivilent to ' + 'USD: ' + str(USD_holdings)

print(invest_based_on_top_trend(['ZAR', 'CNY', 'CAD'], ['USD', 'EUR', 'GBP'], '2015-03-03', '2015-03-15'))













