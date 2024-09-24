#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Dataset
df = pd.read_csv("hotel_booking.csv")

#Clean Data
df.drop(['company', 'agent', 'name','email','phone-number', 'credit_card'], axis=1, inplace=True)
df.dropna(inplace=True)
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
df = df[df['adr']<5000]

#Data Analysis and Visualization

#totall cancel and not cancel reservation 
cancelled_per = df['is_canceled'].value_counts(normalize=True)
print(cancelled_per)
plt.figure(figsize=(5,4))
plt.title('Reservation Status Count')
cancel_count = df['is_canceled'].value_counts()
bars = plt.bar(['Not Cancelled', 'Cancelled'],cancel_count, edgecolor='k' , width=0.7)
plt.show()


#count of cancelation in different hotel
plt.figure(figsize=(8,4))
ax1 = sns.countplot(x='hotel' , hue='is_canceled' , data=df , palette='Blues')
ax1.legend(title='Reservation Status', loc='upper right', bbox_to_anchor=(1,1))
plt.title('Reservation status in differnt hotel', size = 20)
plt.xlabel('hotel')
plt.ylabel('numbers of reservation')
plt.legend(['not canceled', 'canceled'])
plt.show()

# % of canceled and not-canceled reservation in resort and city hotels
resort_hotel = df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)

city_hotel = df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)

resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()

plt.figure(figsize=(20,8))
plt.title("Average daily rate in city adn resort hotel", fontsize=30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label='Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label='City Hotel')
plt.legend(fontsize=20)
plt.show()

#count of canceled & not canceled reservation in months
df['month']=df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1 = sns.countplot(x='month', hue='is_canceled' , data=df)
ax1.legend(loc='upper right', bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('month')
plt.ylabel('numbers of reservation')
plt.legend(['not canceled', 'canceled'])
plt.show()


#pie chart for canceled data

cancelled_data = df[df['is_canceled']==1]
top_10_countories = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title('Top 10 countories which reservation canceled')
plt.pie(top_10_countories, autopct='%.2f', labels=top_10_countories.index)
plt.show()