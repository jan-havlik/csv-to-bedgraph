import os

try:
    import pandas as pd
except ImportError:
    print("Please install the 'pandas' library.")


def main():
    # List to hold data from each CSV file
    dataframes = {}

    if not os.listdir('src/'):
        print("Please copy files you want to convert into 'src/' directory.")
        exit()

    for filename in os.listdir('src/'):
        # only csv files
        if filename.endswith('.csv'):
            df = pd.read_csv('src/' + filename)

            # chromosome name is the filename without the extension
            chr_name = filename.split('.')[0]
            dataframes[chr_name] = df


    for chr, dataframe in dataframes.items():
        
        with open(f"dst/{chr}.bg", "w") as bg_file:
            bg_file.write( 
                f"browser hide all\n" + 
                f"browser pack refGene encodeRegions\n" +
                f"browser full altGraph\n" + 
                f'track type=bedGraph name="{chr} palindrome finder" description="BedGraph format of palindrome finder results" visibility=full color=200,100,0 altColor=0,100,200 priority=20\n'
            )
            for row in dataframe.iterrows():
                row = row[1]
                end = int(row["Position"]) + int(row["Spacer length"]) + int(row["Length"]) * 2
                bg_file.write(f"{chr} {int(row['Position'])} {end} {row['Length']} {row['Spacer length']} {row['Mismatch count']}\n")


if __name__ == "__main__":
    main()