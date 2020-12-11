# extract_ticker() extracts ticker symbols from "./data/xxxx_data.txt" and returns a text object.
import re

# Compile re method
ext_ticker = re.compile(r'\$[A-Z]{1,4} ')
del_etfs = re.compile(r'\$SPX |\$SPY |\$QQQ |\$VIX |\$DIA |\$IWM |\$IGV |\$SQQQ |\$FDN |\$ARKG |\$ARKK |\$ARKW |\$BTC |\$OIL |\$SLV |\$DAX |\$MJ |\$NDX |\$XLF |\$XLC |\$XLE |\$XLU |\$XBI |\$GBTC |\$UVXY |\$TDD ')

def extract_ticker(user_type):
    print('==============================================')
    # Read data file
    with open('./data/' + user_type + '_data.txt', encoding='utf-8') as f:
        lines = f.readlines()
        # Add dummy data for the last user process
        lines.append(' @hogehogehogehoge@ ')
    # Read lines and extract tickers
    pre_user = 'extract_ticker started'
    temp = ''
    output = ''
    for line in lines:
        # Get user name
        start_index = line.find(' @') + 1
        end_index = line.find('@ ')
        current_user = line[start_index:end_index]

        if pre_user == current_user:
            pre_user = current_user
            temp = temp + line
        else:
            print(pre_user)
            # Extract tickers
            temp_list = ext_ticker.findall(temp)
            # Remove duplicates
            temp = ''
            temp_set = set(temp_list)
            for i_str in temp_set:
                temp = temp + i_str
            print(temp)
            print('----------------------------------------------')
            # Write output
            output = output + temp
            pre_user = current_user
            temp = line
    # Eliminate ETFs
    output = del_etfs.sub('', output)
    print('\nextract_ticker completed!')
    return output
