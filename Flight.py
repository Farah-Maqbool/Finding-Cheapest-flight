from datetime import datetime, timedelta
#input flexibility days,budget,destination
destination=input("Destination: ").lower()
budget=int(input("Budget: ").replace("$",""))
prefer_air=list(input("stopover cities if desired : ").lower())
pre_date= input("Enter Prefer date (YYYY-MM-DD): ")
user_date = datetime.strptime(pre_date, "%Y-%m-%d")
flexibility_days=int(input("Flexibility days: "))
print("Bali flights for two weeks next summer (2025/06/02 to 2025/06-16)")
#Airlines dictionaries
preferred_airline={
        "garuda indonesia":{
            "Baggage Allowance":"35kg",
            "Price":2000,
            "Layover Duration":"1hr 45 mint",
            "Flight rating":"****",
            "Flight Dates":"2025-06-02"
        },
        "singapore airlines":{
            "Baggage Allowance":"25kg",
            "Price":1300,
            "Layover Duration":"1hr 5 mint",
            "Flight rating":"*****",
            "Flight Dates":"2025-06-14"

        }
    }
common_airline={
        "emirates":{
            "Baggage Allowance":"30kg",
            "Price":1500,
            "Layover Duration":"59 mint",
            "Flight rating":"*****",
            "Flight Dates":"2025-06-04"

        },
        "qatar airways":{
            "Baggage Allowance":"23kg",
            "Price":1400,
            "Layover Duration":"45 mint",
            "Flight rating":"****",
            "Flight Dates":"2025-06-12"

        },
        "cathay pacific":{
            "Baggage Allowance":"30kg",
            "Price":2600,
            "Layover Duration":"40 mint",
            "Flight rating":"*****",
            "Flight Dates":"2025-06-06"

        },
        "thai airways":{
            "Baggage Allowance":"35kg",
            "Price":2400,
            "Layover Duration":"1hr 30 mint",
            "Flight rating":"***",
            "Flight Dates":"2025-06-10"

        },
        "air asia":{
            "Baggage Allowance":"20kg",
            "Price":2300,
            "Layover Duration":"50 mint",
            "Flight rating":"*****",
            "Flight Dates":"2025-06-08"

        }
    }
# make flexible range
def flexibility_range(user_date,flexibility_days):
    early = user_date - timedelta(days=flexibility_days)
    latest = user_date + timedelta(days=flexibility_days)
    # Calculate the date range
    date_range = []
    # Calculate the duration between 'early' and 'latest'
    duration = latest - early
    # Iterate over each day in the duration and add it to 'early'
    for x in range(duration.days + 1):
        date_val=early + timedelta(days=x)
        date_str=date_val.strftime("%Y-%m-%d") 
        date_range.append(date_str)

    return date_range

# check dates in preferred_airline and common_airline
def check_date(preferred_airline,common_airline):
    dict_date={}
    for i in preferred_airline:
        for key, values in preferred_airline[i].items():
            if key=="Flight Dates":
                dict_date[i]=values
    for i in common_airline:
        for key, values in common_airline[i].items():
            if key=="Flight Dates":
                dict_date[i]=values
    
    return dict_date
    
# check flight dates which are in flexible range
def check_flight_date_in_flexible_range(preferred_airline,common_airline):
    list_date=flexibility_range(user_date,flexibility_days)
    dict_date=check_date(preferred_airline,common_airline)
    airline_range={}
    for key,values in dict_date.items():
        for i in list_date:
            if i==values:
                airline_range[key]=values

    preferred_airline_price={}
    common_airline_price={}
    # for preferred airline
    for i in preferred_airline:
        for key1 in airline_range.keys():
                if i==key1:
                    for key2, values2 in preferred_airline[i].items():
                        if key2=="Price":
                            preferred_airline_price[i]=values2
    # for common airline
    for i in common_airline:
        for key1 in airline_range.keys():
                if i==key1:
                    for key2, values2 in common_airline[i].items():
                        if key2=="Price":
                            common_airline_price[i]=values2
                        
    return preferred_airline_price,common_airline_price

# function for checking budget in common airlines
def budget_common(budget,common_airline):
    preferred_budget,common_budget=check_flight_date_in_flexible_range(preferred_airline,common_airline)
    if common_budget!={}:
            commmon_prefer_cheap=0
            common_cheap=0
            common_name=""
            for key, values in common_budget.items():
                common_cheap=values
                common_name=key
                break
            for key, values in common_budget.items():
                    if values<common_cheap:
                        common_cheap=values
                        common_name=key
                        
            if common_cheap<budget or common_cheap==budget:
                for i in common_airline:
                    if i==common_name:
                        commmon_prefer_cheap=common_cheap
                        common_dict={}
                        for key, values in common_airline[i].items():
                            common_dict[key]=values
                            
                        return i,common_dict,commmon_prefer_cheap
                        
                    
            else:
                return "Not any flight found in your budget","in common airline","also in prefer airline"
    else:
        return "Sorry there are no flights on this date","in common airline","also in prefer airline"

# function for checking budget in preferred airlines 
def budget_prefer(budget,preferred_airline):
    preferred_budget,common_budget=check_flight_date_in_flexible_range(preferred_airline,common_airline)
    prefer_cheap=0
    prefer_name=""
    if preferred_budget!={}:
        
        for key, values in preferred_budget.items():
            prefer_cheap=values
            prefer_name=key
            break
        # Preferred budget check
        for key, values in preferred_budget.items():
            if values<prefer_cheap:
                prefer_cheap=values
                prefer_name=key
        if prefer_cheap<budget or prefer_cheap==budget:
            result1,result2,result3=budget_common(budget,common_airline)
            if prefer_cheap<result3:
                for i in preferred_airline:
                    if i==prefer_name:
                        prefer_dict={}
                        for key, values in preferred_airline[i].items():
                            prefer_dict[key]=values
                        return i,prefer_dict,result3
            else:
                print("I prefer you cheapest flight because your prefer flights are not cheapest") 
                result1,result2,result3=budget_common(budget,common_airline)
                return result1,result2,result3
                    
        else:
            print("Preferred Flights not match with your budget let me check if there any other flight in range") 
            result1,result2,result3=budget_common(budget,common_airline)
            return result1,result2,result3
    else:
        
        print("Not any Your preferred flight found on given date range, but I can help you,\
I check if there is another flight in the same date")
        result1,result2,result3=budget_common(budget,common_airline)
        return result1,result2,result3
        

#calling function    
result1,result2,result3=budget_prefer(budget,preferred_airline)
if type(result2) is dict:
    print("The cheapest flight match with your budget and your flexibility range")
    print(result1)
    for key,values in result2.items():
        print(f"{key}:{values}")
elif type(result1) and type(result2) and type(result3 ) is str:
    print(f"{result1} {result2} {result3}")
print("Top 3 cheapest flight")
# showing top 3 cheapest flights

common_airline.update(preferred_airline)
val=1
cheap=""
val_cheap={}
for i in common_airline:
        for key, values in common_airline[i].items():
            if key=="Price":
                val_cheap[i]=values

for key,values in val_cheap.items():
        if values>val:
            val=values


me_dict=val_cheap.copy()
for i in range(3):
    for i in me_dict.keys():
        for key1, values in me_dict.items():
            if values<val:
                val=values
                cheap=key1
                for i in common_airline:
                    if key1==i:
                        print(i)
                        for key2, values2 in common_airline[i].items():
                                print(key2,values2)       
                        if key1 in me_dict.keys():
                            del val_cheap[key1]
                            
                        
   




   











