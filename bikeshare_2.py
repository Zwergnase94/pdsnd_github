import time
import pandas as pd
import numpy as np

#Name = Name File
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Month
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

#Weekday
WEEKDAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    next = False
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while next == False:
        city = input('Enter a City name: ').lower()
        if city in CITY_DATA:
            break
        else:
            print('No city was found in the database for this entry.')

    # get user input for month (all, january, february, ... , june)
    while next == False:
        month = input('Enter a Month name: ').lower()
        if month in MONTH_DATA:
            break
        else:
            print("Input of the month was not recognized.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while next == False:
        day = input('Enter a Day name: ').lower()
        if day in WEEKDAY_DATA:
            break
        else:
            print("Input of the day was not recognized.\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df["month"].isin([month])]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = WEEKDAY_DATA.index(day)
        
        df = df[df["day_of_week"].isin([day])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most common month: ", MONTH_DATA[(df.groupby(['month'])['month'].count()).idxmax()-1])
    # display the most common day of week
    print("most common day of week: ", WEEKDAY_DATA[(df.groupby(['day_of_week'])['day_of_week'].count()).idxmax()])

    # display the most common start hour
    print("most common start hour: ", (df.groupby(['hour'])['hour'].count()).idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most commonly used start station: ", (df.groupby(['Start Station'])['Start Station'].count()).idxmax())

    # display most commonly used end station
    print("most commonly used end station: ", (df.groupby(['End Station'])['End Station'].count()).idxmax())

    # display most frequent combination of start station and end station trip
    print("most frequent combination of start station and end station trip: ", (df.groupby(['Start Station','End Station'])['Start Station'].count()).idxmax(), " frequent combination: ", (df.groupby(['Start Station','End Station'])['End Station'].count()).max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time', (np.subtract(df['End Time'], df['Start Time'])).sum())

    # display mean travel time
    print('mean travel time', (np.subtract(df['End Time'], df['Start Time'])).mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("counts of user types: \n", (df.groupby(['User Type'])['User Type'].count()))

    # Display counts of gender
    print("\ncounts of user types: \n", (df.groupby(['Gender'])['Gender'].count()))

    # Display earliest, most recent, and most common year of birth
    print("\nearliest, most recent, and most common year of birth: ", (int(df['Birth Year'].min())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def rawdata(df):
    """Ask the user if he wants to see the raw data for his query."""
    start = 0
    answer = input('would you like to see the raw data for your query? yes/no\n')

    while answer == 'yes':
        start += 5
        print(df.head(start))
        answer = input('would you like to see more raw data for your query? yes/no\n')
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
